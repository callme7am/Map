import os
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File
from starlette.responses import FileResponse

from ml.core.InferencePipelines import analyze_tif
from utils.constant import PATH_TO_MODEL

router = APIRouter(tags=["ml"])


@router.post("/analyze-tif", response_class=FileResponse)
async def analyze_tif_endpoint(
    file: UploadFile = File(...),
):
    session = None
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
