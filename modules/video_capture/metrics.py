import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compute_edge_contrast(frame: np.ndarray, mask: np.ndarray) -> float:
    edges = cv2.Canny(frame, 100, 200)
    return float((edges * (mask>0)).sum()) / (mask>0).sum()


def compute_quality(frame: np.ndarray, mask: np.ndarray) -> float:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask_gray = mask.astype(np.uint8)
    s = ssim(gray, mask_gray)
    e = compute_edge_contrast(frame, mask)
    return 0.3 * s + 0.7 * e