import json
import shutil

import plotly.express as px
from fastapi import FastAPI, Form, Request, Query, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from geoalchemy2.functions import ST_X, ST_Centroid, ST_Y, ST_AsGeoJSON
from sqlalchemy import create_engine, text, func, select
from sqlalchemy.orm import sessionmaker
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates

from ml.core.InferencePipelines import analyze_tif
from schemas.map import FilterRequest
from utils.constant import EXCLUDED_TABLES, PATH_TO_MODEL
import schemas
from queries import intersect_geoms
from sqlalchemy.exc import SQLAlchemyError
from models.maps import ZU
from models.archive import QueryArchive
from datetime import datetime
from openpyxl import Workbook
import tempfile
from fastapi.staticfiles import StaticFiles
from utils.utils import get_all_table_names, map_name_to_class
from zipfile import ZipFile
import shapefile
from shapely.geometry import mapping
from geoalchemy2.shape import to_shape
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Соединение с базой данных PostgreSQL
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/space", response_class=HTMLResponse)
async def space(request: Request):
    return templates.TemplateResponse("space.html", {"request": request})


@app.post("/comment/{gid}", response_class=JSONResponse)
async def post_comment(gid: int, comment: str = Form(...)):
    session = SessionLocal()
    try:
        # Найти запись с заданным gid
        zu_record = session.query(ZU).filter(ZU.gid == gid).first()
        if zu_record:
            # Обновить комментарий
            zu_record.comments = comment
            session.commit()
            return JSONResponse(
                content={"status": "success", "message": "Комментарий сохранен"}
            )
        else:
            return JSONResponse(
                content={"status": "error", "message": "Земельный участок не найден"},
                status_code=404,
            )
    except SQLAlchemyError as e:
        session.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
        )
    finally:
        session.close()


@app.post("/search", response_class=JSONResponse)
async def search(cadastra: str = Form(...)):
    session = SessionLocal()
    try:
        # Выполнить запрос к базе данных с помощью SQLAlchemy
        query = select(
            ZU.gid,
            ZU.cadastra2,
            ZU.address,
            ST_X(ST_Centroid(ZU.geom)).label("lon"),
            ST_Y(ST_Centroid(ZU.geom)).label("lat"),
            ZU.hasvalid5,
            ZU.hascadas6,
            ZU.isdraft,
            ZU.ownershi8,
            ZU.is_stroy,
            ZU.is_nonca20,
            ZU.area,
            ZU.comments,
            ST_AsGeoJSON(ZU.geom).label("geom"),
        ).filter(ZU.cadastra2 == cadastra)

        results = session.execute(query).mappings().all()

        if not results:
            return JSONResponse(
                content={"status": "error", "message": "Участок не найден"},
                status_code=404,
            )

        markers = []
        for row in results:
            zu_instance = ZU()
            popup_text = zu_instance.get_popup(row)
            markers.append(
                {
                    "lat": row["lat"],
                    "lon": row["lon"],
                    "geom": row["geom"],
                    "popup": popup_text,
                }
            )

        # Запись запроса в архив
        insert_query = QueryArchive(query_text=str(query), timestamp=datetime.now())
        session.add(insert_query)
        session.commit()

        return JSONResponse(content=markers)

    except SQLAlchemyError as e:
        session.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
        )
    finally:
        session.close()


@app.get("/archive", response_class=HTMLResponse)
async def get_archive(request: Request):
    session = SessionLocal()
    try:
        # Выполнить запрос к базе данных с помощью SQLAlchemy
        query = select(QueryArchive).order_by(QueryArchive.timestamp.desc())
        results = session.scalars(query).all()

        return templates.TemplateResponse(
            "archive.html", {"request": request, "data": results}
        )

    except SQLAlchemyError as e:
        return HTMLResponse(
            content=f"Ошибка при получении данных из архива: {str(e)}", status_code=500
        )
    finally:
        session.close()


@app.post("/export/shp", response_class=FileResponse)
async def export_shp(request: Request):
    session = SessionLocal()
    data = await request.json()
    selected_objects = data["selected_objects"]

    try:
        # Группируем объекты по типу карты
        objects_by_map = {}
        for obj in selected_objects:
            map_name = obj["map_name"]
            if map_name not in objects_by_map:
                objects_by_map[map_name] = []
            objects_by_map[map_name].append(obj["gid"])

        # Создание временной папки
        tmpdirname = tempfile.mkdtemp()

        for map_name, gids in objects_by_map.items():
            model_class = map_name_to_class(schemas)[map_name]

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

            # Add records
            query = select(*fields, model_class.geom).filter(model_class.gid.in_(gids))
            results = session.execute(query).fetchall()

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

        # Возвращаем zip архив
        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename="exported_data.zip",
        )
    except SQLAlchemyError as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
        )
    finally:
        session.close()


@app.post("/export/xlsx", response_class=FileResponse)
async def export_xlsx(request: Request):
    session = SessionLocal()
    data = await request.json()
    selected_objects = data["selected_objects"]

    try:
        # Группируем объекты по типу карты
        objects_by_map = {}
        for obj in selected_objects:
            map_name = obj["map_name"]
            if map_name not in objects_by_map:
                objects_by_map[map_name] = []
            objects_by_map[map_name].append(obj["gid"])

        # Создание временного файла
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            file_path = tmp.name
            wb = Workbook()

            for map_name, gids in objects_by_map.items():
                model_class = map_name_to_class(schemas)[map_name]
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
                query = select(*fields).filter(model_class.gid.in_(gids))
                results = session.execute(query).fetchall()

                for row in results:
                    row_data = [getattr(row, field.name) for field in fields]
                    ws.append(row_data)

            wb.save(file_path)
            wb.close()

            return FileResponse(
                path=file_path,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename="exported_data.xlsx",
            )

    except SQLAlchemyError as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
        )
    finally:
        session.close()


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    session = SessionLocal()
    try:
        # Выполнить запрос к базе данных с помощью SQLAlchemy
        query = select(
            ZU.ownershi8,
            func.count(ZU.gid).label("count"),
            func.sum(ZU.area).label("total_area"),
        ).group_by(ZU.ownershi8)

        results = session.execute(query).mappings().all()

        # Создаем графики с использованием Plotly
        bar_fig = px.bar(
            results,
            x="ownershi8",
            y="count",
            title="Количество участков по типу собственности",
            labels={"ownershi8": "Тип собственности", "count": "Количество участков"},
        )
        area_fig = px.pie(
            results,
            values="total_area",
            names="ownershi8",
            title="Общая площадь участков по типу собственности",
        )

        bar_fig_html = bar_fig.to_html(full_html=False)
        area_fig_html = area_fig.to_html(full_html=False)

        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "bar_fig": bar_fig_html, "area_fig": area_fig_html},
        )

    except SQLAlchemyError as e:
        return HTMLResponse(
            content=f"Ошибка при получении данных для панели управления: {str(e)}",
            status_code=500,
        )
    finally:
        session.close()


@app.post("/map", response_class=JSONResponse)
async def get_map_data(maps: list[str] = Form(...)):
    session = SessionLocal()
    class_maps = []
    markers = []
    mn_to_cl = map_name_to_class(schemas)

    for map in json.loads(maps[0]):
        class_maps.append(mn_to_cl[map])
    for model_class in class_maps:
        fields = [
            ST_AsGeoJSON(column).label("geom")
            if str(column) == f"{model_class.__tablename__}.geom"
            else column
            for column in model_class.__table__.columns
        ]

        fields.extend(
            [
                ST_X(ST_Centroid(model_class.geom)).label("lon"),
                ST_Y(ST_Centroid(model_class.geom)).label("lat"),
            ]
        )

        query = select(*fields)

        results = session.execute(query).mappings().all()

        markers_temp = [
            {
                "gid": result["gid"],
                "lat": result["lat"],
                "lon": result["lon"],
                "geom": result["geom"],
                "popup": model_class.get_popup(result),
                "map_name": model_class.__tablename__,
            }
            for result in results
        ]
        markers.extend(markers_temp)

    return JSONResponse(content=markers)


@app.get("/map_list", response_class=JSONResponse)
async def map_list():
    session = SessionLocal()
    tables = get_all_table_names(session)

    # Исключить нежелательные таблицы
    maps = [table for table in tables if table not in EXCLUDED_TABLES]

    return JSONResponse(content=maps)


@app.get("/search_by_address", response_class=JSONResponse)
async def search_by_address(address: str = Query(...)):
    session = SessionLocal()
    try:
        # Выполнить запрос к базе данных с помощью SQLAlchemy
        query = (
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
                ZU.comments,
                ZU.address,
                ST_X(ST_Centroid(ZU.geom)).label("lon"),
                ST_Y(ST_Centroid(ZU.geom)).label("lat"),
                ZU.address_tsv,
                ST_AsGeoJSON(ZU.geom).label("geom"),
            )
            .filter(text(f"address_tsv @@ plainto_tsquery('russian', '{address}')"))
            .params(address=address)
        )

        results = session.execute(query).mappings().all()

        if not results:
            return JSONResponse(
                content={"status": "error", "message": "Участок не найден"},
                status_code=404,
            )

        markers = []
        for row in results:
            zu_instance = ZU()
            popup_text = zu_instance.get_popup(row)
            markers.append(
                {
                    "lat": row["lat"],
                    "lon": row["lon"],
                    "geom": row["geom"],
                    "popup": popup_text,
                }
            )

        # Запись запроса в архив
        insert_query = QueryArchive(
            query_text=str(query.compile(compile_kwargs={"literal_binds": True})),
            timestamp=datetime.now(),
        )
        session.add(insert_query)
        session.commit()

        return JSONResponse(content=markers)

    except SQLAlchemyError as e:
        session.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
        )
    finally:
        session.close()


@app.post("/map_intersections", response_class=JSONResponse)
async def get_map_intersections(maps: list[str] = Form(...)):
    session = SessionLocal()

    class_maps = []
    mn_to_cl = map_name_to_class(schemas)

    for map in json.loads(maps[0]):
        class_maps.append(mn_to_cl[map])

    intersections = intersect_geoms(session, *class_maps)

    return intersections


@app.get("/maps", response_class=HTMLResponse)
async def maps_page(request: Request):
    return templates.TemplateResponse("maps.html", {"request": request})


@app.get("/intersections", response_class=HTMLResponse)
async def intersections_page(request: Request):
    return templates.TemplateResponse("intersections.html", {"request": request})


@app.post("/filter")
def filter_model(request: FilterRequest):
    db = SessionLocal()

    model_name = request.class_name
    filters = request.filters

    # Get the model class from the model name
    model_class = map_name_to_class(schemas)[model_name]
    if not model_class:
        raise HTTPException(status_code=404, detail="Model not found")

    # Create the query and apply the filters
    query = db.query(model_class)
    for field, value in filters.items():
        if hasattr(model_class, field):
            query = query.filter(getattr(model_class, field) == value)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' not found in model '{model_name}'",
            )

    results = query.all()
    return {"results": results}


@app.post("/analyze-tif", response_class=FileResponse)
async def analyze_tif_endpoint(
    file: UploadFile = File(...),
):
    session = SessionLocal()
    try:
        tmpdirname = tempfile.mkdtemp()
        file_path = os.path.join(tmpdirname, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        path_to_save_folder = os.path.join(tmpdirname, "results")
        path_to_output_zip_folder = tmpdirname
        os.makedirs(path_to_save_folder, exist_ok=True)

        output_zip_path = analyze_tif(
            session=session,
            path_to_tif=file_path,
            path_to_save_folder=path_to_save_folder,
            path_to_output_zip_folder=path_to_output_zip_folder,
            path_to_model=PATH_TO_MODEL,
        )

        return FileResponse(
            path=output_zip_path,
            media_type="application/zip",
            filename="analyzed_data.zip",
        )
    finally:
        session.close()
