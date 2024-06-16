from typing import List, Optional
import os
from zipfile import ZipFile
from PIL import Image
import numpy as np
from loguru import logger


def check_and_convert_mode(img: Image.Image) -> Image.Image:
    if img.mode == "RGBA":
        return img.convert("RGB")
    return img


def convert_image(path_to_tif: str) -> np.ndarray:
    with Image.open(path_to_tif) as img:
        img = check_and_convert_mode(img)
        img = np.ascontiguousarray(img)
        return img


def get_files_to_archive(name: str, path_to_save_folder: str) -> List[str]:
    return [f for f in os.listdir(path_to_save_folder) if f.startswith(name)]


def archive_files(
    files_to_archive: List[str], path_to_save_folder: str, output_zip_path: str
) -> None:
    with ZipFile(output_zip_path, "w") as zipfile:
        for file_name in files_to_archive:
            file_path = os.path.join(path_to_save_folder, file_name)
            zipfile.write(file_path, os.path.basename(file_path))
            os.remove(file_path)


def archive_and_delete_files(
    name: str, path_to_save_folder: str, output_zip_path: str
) -> Optional[str]:
    if not os.path.exists(path_to_save_folder):
        logger.error(f"Папка '{path_to_save_folder}' не существует.")
        return None

    files_to_archive = get_files_to_archive(name, path_to_save_folder)

    if not files_to_archive:
        logger.error("Файлы куда-то испарились...")
        return None

    archive_files(files_to_archive, path_to_save_folder, output_zip_path)


def is_tif_file(filename: str) -> bool:
    file_extension = os.path.splitext(filename)[1]
    return file_extension.lower() == ".tif"


def generate_unique_name(path_to_file: str) -> Optional[str]:
    name = os.path.splitext(os.path.basename(path_to_file))[0]
    return name
