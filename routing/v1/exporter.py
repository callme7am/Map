from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from schemas.exporter import SelectedObject
from services.exporter import ExporterService

router = APIRouter(tags=["exporters"])


@router.post("/export/shp", response_class=FileResponse)
async def export_shp(
    req: List[SelectedObject], exporter_service: ExporterService = Depends()
):
    path_to_zip = await exporter_service.to_shp(req)

    return FileResponse(
        path=path_to_zip,
        media_type="application/zip",
        filename="exported_data.zip",
    )


@router.post("/export/xlsx", response_class=FileResponse)
async def export_xlsx(
    req: List[SelectedObject], exporter_service: ExporterService = Depends()
):
    path_to_xlsx = await exporter_service.to_xlsx(req)

    return FileResponse(
        path=path_to_xlsx,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="exported_data.xlsx",
    )
