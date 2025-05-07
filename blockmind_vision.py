
import cv2
import numpy as np
from ultralytics import YOLO
from blockmind_window_capture import capture_game_window

# Load YOLOv8 model once (you can switch to another YOLOv8 variant if needed)
model = YOLO("yolov8n.pt")  # 'n' = nano (fastest, smallest)

def analyze_frame(frame=None):
    # Use provided frame or capture a new one
    if frame is None:
        frame = capture_game_window()

    if frame is None:
        print("❌ No game window captured.")
        return {}

    print("👁️ Frame captured and processed.")

    # Detect center pixel (crosshair RGB)
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    crosshair_rgb = frame[center_y, center_x].tolist()

    # Run YOLO object detection
    results = model(frame, verbose=False)[0]
    detections = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x, y, w, h = x1, y1, x2 - x1, y2 - y1
        detections.append({
            "label": label,
            "box": [x, y, w, h]
        })

    return {
        "detections": detections,
        "crosshair_rgb": crosshair_rgb
    }
