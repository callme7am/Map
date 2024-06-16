from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ultralytics.utils.plotting import Annotator
from shapely.geometry import shape
import csv
import numpy as np
from typing import Any, List, Union, Dict


def create_results_pdf(
    buildings: Union[List[Dict], List[None]], output_pdf_path: str
) -> None:
    pdf = canvas.Canvas(output_pdf_path, pagesize=letter)
    y_coordinate = 700

    for building in buildings:
        info_lines = [
            f"ID Здания: {building['properties']['id']}",
            f"Тип здания: {building['properties']['Name']}",
            f"Местоположение здания: {shape(building['geometry']).centroid.coords[0]}",
            f"Кадастровый номер: {building['properties']['cadastral_']}",
        ]

        for line in info_lines:
            pdf.drawString(100, y_coordinate, line)
            y_coordinate -= 14
        pdf.showPage()
        y_coordinate = 700

    # Сохранение PDF-документа
    pdf.save()


def annotate_tracking_results(
    img: np.ndarray, track_results: Any, names: List[str]
) -> np.ndarray:
    annotator = Annotator(img)
    for r in track_results:
        for box in r.boxes:
            b = box.xyxy[0]
            label = names[int(box.cls)]
            annotator.box_label(b, label, color=(79, 226, 104))
    return annotator.result()


def create_result_csv(
    buildings: Union[List[Dict], List[None]], output_csv_path: str
) -> None:
    with open(output_csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID Здания", "Тип здания", "x", "y", "Кадастровый номер"])
        for building in buildings:
            writer.writerow(
                [
                    building["properties"]["gid"],
                    building["properties"]["type"],
                    shape(building["geometry"]).centroid.x,
                    shape(building["geometry"]).centroid.y,
                    building["properties"]["cadastra2"],
                ]
            )
