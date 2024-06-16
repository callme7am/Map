import os

from ml.core.MapCreator import (
    process_detection_results,
    read_geospatial_metadata_from_tif,
    create_buildings_shapefile,
)
from ml.core.ResultCreator import create_result_csv, annotate_tracking_results
from ml.core.YoloTracker import detect_objects_in_image
from ml.core.FilesPreprocessor import (
    archive_and_delete_files,
    generate_unique_name,
    convert_image,
)
import cv2 as cv
from sqlalchemy.orm import Session


def analyze_tif(
    session: Session,
    path_to_tif: str,
    path_to_save_folder: str,
    path_to_output_zip_folder: str,
    path_to_model: str,
) -> str:
    unique_name = generate_unique_name(path_to_tif)

    shapefile_path = os.path.join(
        path_to_output_zip_folder, "results", unique_name + ".shp"
    )
    output_boxed_jpg_path = os.path.join(
        path_to_output_zip_folder, "results", unique_name + "_boxed.jpg"
    )
    output_csv_path = os.path.join(
        path_to_output_zip_folder, "results", unique_name + ".csv"
    )
    output_zip_path = os.path.join(
        path_to_output_zip_folder, "results", unique_name + "_archive.zip"
    )

    transform, coordinates = read_geospatial_metadata_from_tif(path_to_tif)

    img = convert_image(path_to_tif)

    track_results, names = detect_objects_in_image(img, path_to_model)

    annotated_img = annotate_tracking_results(img, track_results, names)
    cv.imwrite(output_boxed_jpg_path, annotated_img)

    buildings, field_types = process_detection_results(
        session,
        track_results,
        names,
        transform,
        coordinates,
    )

    create_buildings_shapefile(
        buildings,
        shapefile_path,
        field_types,
    )
    create_result_csv(buildings, output_csv_path)

    archive_and_delete_files(unique_name, path_to_save_folder, output_zip_path)

    return output_zip_path
