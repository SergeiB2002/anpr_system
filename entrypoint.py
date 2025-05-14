import asyncio
import yaml
from fastapi import FastAPI
from modules.video_capture.capture import start_capture
from modules.ocr_engine.detection import detect_plate
from modules.ocr_engine.recognition import ocr_read
from modules.db_manager.crud import verify_plate
from modules.access_control.control import trigger_barrier
from modules.access_control.notificator import play_sound

app = FastAPI()

with open("config/config.yaml") as f:
    cfg = yaml.safe_load(f)

@app.on_event("startup")
async def init_tasks():
    asyncio.create_task(start_capture(cfg))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process_frame")
async def process_frame():
    frame, mask = await detect_plate()  # из video_capture
    text, conf = ocr_read(frame, mask, cfg['ocr']['languages'])
    status = await verify_plate(text)
    if status == "VALID":
        trigger_barrier()
        play_sound('access_granted.mp3')
    else:
        play_sound('access_denied.mp3')
    return {"plate": text, "confidence": conf, "status": status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)