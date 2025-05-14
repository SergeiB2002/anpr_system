from ultralytics import YOLO
import cv2

def detect_plate() -> tuple:
    model = YOLO('yolov8n.pt')
    # Берём последний сохранённый кадр из очереди/памяти
    frame = load_latest_frame()
    results = model(frame)
    for r in results:
        if r.boxes:
            box = r.boxes[0].xyxy[0].cpu().numpy().astype(int)
            x1,y1,x2,y2 = box
            plate_img = frame[y1:y2, x1:x2]
            mask = create_mask_from_box(frame.shape, box)
            return plate_img, mask
    raise RuntimeError("Пластина не найдена")