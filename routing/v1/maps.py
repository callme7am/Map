import json
from typing import List

from fastapi import APIRouter, Form, Depends, Query, Request
from starlette.responses import JSONResponse, HTMLResponse

from models import maps as model_maps
from routing.v1.static import templates
from schemas.map import Marker, CreateCommentOpts, FilterRequest
from services.maps import MapService
from utils.utils import map_name_to_class
import plotly.express as px

router = APIRouter(tags=["maps"])


@router.get("/map_list", response_model=List[str])
async def get_map_list(map_service: MapService = Depends()):
    return await map_service.get_available_maps()


@router.get("/map_columns/{map}", response_model=List[str])
async def get_map_columns(map: str, map_service: MapService = Depends()):
    return await map_service.get_map_columns(map)


@router.post("/filters", response_model=List[Marker])
async def filters(req: FilterRequest, map_service: MapService = Depends()):
    markers = await map_service.filters(req)
    return markers


@router.get("/search_by_address", response_model=List[Marker])
async def search_by_address(
    map_service: MapService = Depends(), address: str = Query(...)
):
    markers = await map_service.search_by_address(address)
    return markers


@router.post("/search", response_model=List[Marker])
async def search_by_cadastra(
    map_service: MapService = Depends(), cadastra: str = Form(...)
):
    markers = await map_service.search_by_cadastra(cadastra)
    return [markers]


@router.post("/map", response_class=JSONResponse)
async def get_maps(maps: list[str] = Form(...), map_service: MapService = Depends()):
    class_maps = []
    mn_to_cl = map_name_to_class(model_maps)

    for map in json.loads(maps[0]):
        class_maps.append(mn_to_cl[map])

    markers = await map_service.get_map_markers(class_maps)

    return markers


@router.post("/comment/{gid}", response_class=JSONResponse)
async def post_comment(
    gid: int, comment: str = Form(...), map_service: MapService = Depends()
):
    await map_service.create_comment(CreateCommentOpts(gid=gid, comment=comment))


@router.post("/map_intersections", response_class=JSONResponse)
async def get_map_intersections(
    maps: list[str] = Form(...), map_service: MapService = Depends()
):
    result = await map_service.maps_intersection(json.loads(maps[0]))

    return result


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, map_service: MapService = Depends()):
    results = await map_service.get_dashboard()

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
