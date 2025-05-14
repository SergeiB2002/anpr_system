import cv2
import numpy as np

def adjust_brightness(frame: np.ndarray, lux: float) -> np.ndarray:
    # Простая линейная коррекция по люксам
    alpha = 1 + (lux - 1000) / 10000
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=0)


def extract_plate_mask(frame: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Морфологические операции для чистки
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return mask