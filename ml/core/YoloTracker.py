from ultralytics import YOLO
from typing import Tuple, List, Any
import numpy as np


def load_yolo_detection_model(model_path: str) -> YOLO:
    """
    Загружает модель YOLO для детекции объектов.

    Parameters:
    - model_path (str): Путь к файлу модели.

    Returns:
    - YOLO: Загруженная модель YOLO.
    """
    return YOLO(model_path, task="detect")


def detect_objects_in_image(
    img: np.ndarray, path_to_model: str
) -> Tuple[Any, List[str]]:
    model = load_yolo_detection_model(path_to_model)
    names = model.names

    # Получение предсказаний модели YOLO
    results = model.predict(img)

    return results, names
