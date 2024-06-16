import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from routing.v1.static import router as static_routes
from routing.v1.maps import router as map_routes
from routing.v1.exporter import router as exporter_routes
from routing.v1.archive import router as archive_routes
from routing.v1.auth import router as auth_routes

from configs.Environment import get_environment_variables

app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")

app.mount("/static", StaticFiles(directory="./static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO models

env = get_environment_variables()

if not env.DEBUG:
    logger.remove()
    logger.add(sys.stdout, level="INFO")

app.include_router(static_routes)
app.include_router(map_routes)
app.include_router(exporter_routes)
app.include_router(archive_routes)
app.include_router(auth_routes)
