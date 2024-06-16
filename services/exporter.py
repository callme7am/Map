import os
import tempfile
from typing import List
from zipfile import ZipFile

import shapefile
from fastapi import Depends
from geoalchemy2.shape import to_shape
from openpyxl.workbook import Workbook
from shapely.geometry import mapping
import models.maps as map_models
from schemas.exporter import SelectedObject
from services.maps import MapService
from utils.utils import map_name_to_class


class ExporterService:
    def __init__(self, map_service: MapService = Depends()):
        self._map_service = map_service

    async def to_shp(self, objects: List[SelectedObject]) -> str:
        objects_by_map = {}
        for obj in objects:
            map_name = obj.map_name
            if map_name not in objects_by_map:
                objects_by_map[map_name] = []
            objects_by_map[map_name].append(obj.gid)

        tmpdirname = tempfile.mkdtemp()

        for map_name, gids in objects_by_map.items():
            model_class = map_name_to_class(map_models)[map_name]

            fields = [
                column
                for column in model_class.__table__.columns
                if str(column) != f"{model_class.__tablename__}.geom"
            ]

            # Создаем shapefile writer
            shp_path = os.path.join(tmpdirname, f"{map_name}.shp")
            shp_writer = shapefile.Writer(shp_path, shapeType=shapefile.POLYGON)
            shp_writer.autoBalance = 1  # Ensure shapefile and dbf files are balanced

            # Add fields
            for field in fields:
                if field.type.python_type == str:
                    shp_writer.field(field.name, "C")
                elif field.type.python_type == int:
                    shp_writer.field(field.name, "N")
                elif field.type.python_type == float:
                    shp_writer.field(field.name, "F")
                else:
                    shp_writer.field(field.name, "C")

            results = await self._map_service.get_records_for_exporter(
                fields, model_class, gids
            )

            for row in results:
                geom = to_shape(row.geom)
                shp_writer.shape(mapping(geom))
                record = [getattr(row, field.name) for field in fields]
                shp_writer.record(*record)

            shp_writer.close()

            # Создаем zip архив
            zip_path = os.path.join(tmpdirname, "exported_data.zip")
            with ZipFile(zip_path, "w") as zipf:
                for root, _, files in os.walk(tmpdirname):
                    for file in files:
                        if (
                            file.endswith(".shp")
                            or file.endswith(".shx")
                            or file.endswith(".dbf")
                        ):
                            zipf.write(os.path.join(root, file), arcname=file)

            return zip_path

    async def to_xlsx(self, objects: List[SelectedObject]) -> str:
        objects_by_map = {}
        for obj in objects:
            map_name = obj.map_name
            if map_name not in objects_by_map:
                objects_by_map[map_name] = []
            objects_by_map[map_name].append(obj.gid)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            file_path = tmp.name
            wb = Workbook()

            for map_name, gids in objects_by_map.items():
                model_class = map_name_to_class(map_models)[map_name]
                ws = wb.create_sheet(title=map_name)

                # Получаем все поля, кроме geom
                fields = [
                    column
                    for column in model_class.__table__.columns
                    if str(column) != f"{model_class.__tablename__}.geom"
                ]
                headers = [field.name for field in fields]
                ws.append(headers)

                # Запрос для получения данных по gid
                results = await self._map_service.get_records_for_exporter(
                    fields, model_class, gids
                )

                for row in results:
                    row_data = [getattr(row, field.name) for field in fields]
                    ws.append(row_data)

            wb.save(file_path)
            wb.close()
        return file_path
