from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from starlette.templating import Jinja2Templates

router = APIRouter(tags=["templates"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/auth", response_class=HTMLResponse)
async def auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/space", response_class=HTMLResponse)
async def space(request: Request):
    return templates.TemplateResponse("space.html", {"request": request})


@router.get("/maps", response_class=HTMLResponse)
async def maps_page(request: Request):
    return templates.TemplateResponse("maps.html", {"request": request})


@router.get("/intersections", response_class=HTMLResponse)
async def intersections_page(request: Request):
    return templates.TemplateResponse("intersections.html", {"request": request})
