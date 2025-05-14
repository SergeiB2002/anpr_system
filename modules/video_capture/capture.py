import cv2
import numpy as np
import asyncio
from skimage.metrics import structural_similarity as ssim
from .preprocessing import adjust_brightness, extract_plate_mask
from .metrics import compute_quality

async def start_capture(cfg):
    rtsp_url = cfg['cameras'][0]['rtsp']
    cap = cv2.VideoCapture(rtsp_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            await asyncio.sleep(0.1)
            continue
        lux = read_light_sensor(cfg['light_sensor']['endpoint'])
        frame = adjust_brightness(frame, lux)
        mask = extract_plate_mask(frame)
        q = compute_quality(frame, mask)
        if q < cfg['processing']['quality_threshold']:
            continue
        # Сохранить кадр и маску во временное хранилище или publish в очередь
        await asyncio.sleep(1/25)

def read_light_sensor(endpoint: str) -> float:
    # HTTP-запрос к сенсору освещённости
    import requests
    r = requests.get(endpoint)
    return float(r.json().get('lux', 0))