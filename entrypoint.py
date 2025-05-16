#!/usr/bin/env python3
import os
import asyncio
import yaml
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

# локальные модули
from modules.video_capture.capture import start_capture
from modules.ocr_engine.detection import detect_plate
from modules.ocr_engine.recognition import ocr_read
from modules.db_manager.crud import verify_plate
from modules.access_control.control import trigger_barrier
from modules.access_control.notificator import play_sound

# подгружаем .env
load_dotenv()

# логирование
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# читаем конфиг
config_path = os.getenv("CONFIG_PATH", "config/config.yaml")
with open(config_path, "r") as f:
    cfg = yaml.safe_load(f)

@app.on_event("startup")
async def startup_event():
    logger.info("Запуск задачи video_capture")
    asyncio.create_task(start_capture(cfg))

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/process_frame")
async def process_frame():
    frame, mask = detect_plate()  # захват из модуля video_capture
    text, conf = ocr_read(frame, mask, cfg["ocr"]["languages"])
    status = await verify_plate(text)
    if status == "VALID":
        trigger_barrier()
        play_sound(os.getenv("ACCESS_GRANTED_SOUND", "sounds/access_granted.mp3"))
    else:
        play_sound(os.getenv("ACCESS_DENIED_SOUND", "sounds/access_denied.mp3"))
    return {"plate": text, "confidence": conf, "status": status}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info")
    uvicorn.run("entrypoint:app", host=host, port=port, log_level=log_level)
