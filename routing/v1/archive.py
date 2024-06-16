from fastapi import APIRouter, Request, Depends
from starlette.responses import HTMLResponse

from routing.v1.static import templates
from services.archive import ArchiveService

router = APIRouter(tags=["archive"])


@router.get("/archive", response_class=HTMLResponse)
async def get_archive(request: Request, archive_service: ArchiveService = Depends()):
    results = await archive_service.list()
    return templates.TemplateResponse(
        "archive.html", {"request": request, "data": results}
    )
