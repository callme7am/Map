from sqlalchemy import select, func
from sqlalchemy.orm import Session
from shapely.geometry import Polygon, mapping
import pyproj
import rasterio
from typing import Any, List, Dict, Union, Tuple
from geoalchemy2.shape import from_shape
from models.maps import ZU
import shapefile


def process_detection_results(
    session: Session,
    track_results: Any,
    names: List[str],
    transform: rasterio.transform.Affine,
    coordinates: str,
    start: int = 1,
) -> Union[List[Dict], List[None]]:
    buildings = []
    field_types = {}

    parcels_crs = pyproj.CRS.from_epsg(
        4326
    )  # Предполагаем, что CRS таблицы ZU - EPSG:4326
    buildings_crs = pyproj.CRS.from_string(coordinates)

    transformer = (
        pyproj.Transformer.from_crs(buildings_crs, parcels_crs, always_xy=True)
        if buildings_crs != parcels_crs
        else None
    )

    # Определение типов полей из модели ZU
    for column in ZU.__table__.columns:
        if column.name not in ["geom", "address_tsv"]:
            field_types[column.name] = str(column.type)

    for r in track_results:
        for id, box in enumerate(r.boxes, start=start):
            b = box.xyxy[0]
            building_polygon = Polygon(
                [
                    transform * (b[0], b[1]),
                    transform * (b[0], b[3]),
                    transform * (b[2], b[3]),
                    transform * (b[2], b[1]),
                    transform * (b[0], b[1]),
                ]
            )

            # Преобразование координат, если CRS различаются
            if transformer:
                transformed_coords = [
                    transformer.transform(x, y)
                    for x, y in building_polygon.exterior.coords
                ]
                building_polygon = Polygon(transformed_coords)

            building_shape = from_shape(building_polygon, srid=4326)

            try:
                subquery = (
                    select(
                        ZU.gid,
                        ZU.cadastra2,
                        ZU.address,
                        ZU.hasvalid5,
                        ZU.hascadas6,
                        ZU.isdraft,
                        ZU.ownershi8,
                        ZU.is_stroy,
                        ZU.is_nonca20,
                        ZU.area,
                        ZU.district_id,
                        ZU.comments,
                        func.ST_Area(
                            func.ST_Intersection(ZU.geom, building_shape)
                        ).label("intersection_area"),
                    )
                    .filter(func.ST_Intersects(ZU.geom, building_shape))
                    .order_by(
                        func.ST_Area(
                            func.ST_Intersection(ZU.geom, building_shape)
                        ).desc()
                    )
                    .limit(1)
                ).subquery()

                query = select(subquery)
                result = session.execute(query).first()

                if result:
                    row = result[0]
                    buildings.append(
                        {
                            "geometry": mapping(building_polygon),
                            "properties": {
                                "type": names[int(box.cls)],
                                "gid": row.gid,
                                "cadastra2": row.cadastra2,
                                "address": row.address,
                                "hasvalid5": row.hasvalid5,
                                "hascadas6": row.hascadas6,
                                "isdraft": row.isdraft,
                                "ownershi8": row.ownershi8,
                                "is_stroy": row.is_stroy,
                                "is_nonca20": row.is_nonca20,
                                "area": row.area,
                                "district_id": row.district_id,
                                "comments": row.comments,
                                "status": "Найдено",
                            },
                        }
                    )
                else:
                    buildings.append(
                        {
                            "geometry": mapping(building_polygon),
                            "properties": {
                                "type": names[int(box.cls)],
                                "gid": None,
                                "cadastra2": None,
                                "address": None,
                                "hasvalid5": None,
                                "hascadas6": None,
                                "isdraft": None,
                                "ownershi8": None,
                                "is_stroy": None,
                                "is_nonca20": None,
                                "area": None,
                                "district_id": None,
                                "comments": None,
                                "status": "Не найдено пересечение с земельными участками",
                            },
                        }
                    )
            except Exception as e:
                buildings.append(
                    {
                        "geometry": mapping(building_polygon),
                        "properties": {
                            "type": names[int(box.cls)],
                            "gid": None,
                            "cadastra2": None,
                            "address": None,
                            "hasvalid5": None,
                            "hascadas6": None,
                            "isdraft": None,
                            "ownershi8": None,
                            "is_stroy": None,
                            "is_nonca20": None,
                            "area": None,
                            "district_id": None,
                            "comments": None,
                            "status": f"Ошибка при выполнении запроса: {str(e)}",
                        },
                    }
                )

    return buildings, field_types


def read_geospatial_metadata_from_tif(
    path_to_tif: str,
) -> Tuple[rasterio.transform.Affine, str]:
    with rasterio.open(path_to_tif) as src:
        transform = src.transform
        coordinates = src.crs.to_proj4()

    return transform, coordinates


def create_buildings_shapefile(
    buildings: Union[List[Dict], List[None]],
    buildings_shapefile_path: str,
    field_types: Dict[str, str],
) -> None:
    shp_writer = shapefile.Writer(buildings_shapefile_path, shapeType=shapefile.POLYGON)

    shp_writer.field("type", "C")
    # Определение полей с учетом типов
    for field_name, field_type in field_types.items():
        if field_type.startswith("VARCHAR") or field_type == "Text":
            shp_writer.field(field_name, "C")
        elif field_type.startswith("INT") or field_type == "Integer":
            shp_writer.field(field_name, "N")
        elif (
            field_type.startswith("FLOAT")
            or field_type.startswith("DOUBLE")
            or field_type == "Numeric"
        ):
            shp_writer.field(field_name, "F")
        else:
            shp_writer.field(field_name, "C")  # Для всех остальных случаев

    # Добавляем поле 'status'
    shp_writer.field("status", "C")
    shp_writer.field("type", "C")

    for building in buildings:
        geometry = building["geometry"]
        properties = building["properties"]

        shp_writer.shape(geometry)

        # Запись записи в shapefile
        record = [properties.get(field, None) for field in field_types.keys()]
        record.append(properties.get("status", None))
        record.append(properties.get("type", None))
        shp_writer.record(*record)

    # Закрытие файла shapefile
    shp_writer.close()
