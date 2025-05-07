import cv2
import numpy as np
from ultralytics import YOLO

# Load Minecraft-trained YOLO model (you'll need to train/create this)
model = YOLO("minecraft_yolov8.pt") 

def analyze_frame(frame):
    if frame is None:
        return {"detections": []}

    results = model(frame, verbose=False)[0]
    return {
        "detections": [{
            "label": model.names[int(box.cls[0])],
            "confidence": float(box.conf[0]),
            "box": list(map(int, box.xyxy[0]))
        } for box in results.boxes],
        "frame_size": frame.shape[:2]
    }