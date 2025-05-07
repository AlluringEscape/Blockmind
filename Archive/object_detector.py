from ultralytics import YOLO
import cv2

# Load pretrained YOLOv8 model (YOLOv8n is fastest, use 'yolov8m' or 'l' for better accuracy)
model = YOLO("yolov8n.pt")

def detect_objects(image):
    # Convert BGR to RGB (YOLO prefers RGB)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run YOLO without forcing a downscale
    results = model.predict(source=rgb)

    detected = []
    for result in results:
        for box in result.boxes:
            cls = result.names[int(box.cls)]
            conf = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detected.append({
                "label": cls,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })
    return detected
