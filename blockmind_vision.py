
import cv2
import numpy as np
import os
import json
import tempfile
import webbrowser
from datetime import datetime
from ultralytics import YOLO
from blockmind_window_capture import capture_game_window

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Save paths
UNKNOWN_DIR = "datasets/unknown_screenshots"
LOG_FILE = "logs/unknown_log.json"
KNOWN_CLASSES_FILE = "logs/known_classes.json"
VISUAL_MEMORY_FILE = "logs/learned_visuals.json"
os.makedirs(UNKNOWN_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Load known class list
if os.path.exists(KNOWN_CLASSES_FILE):
    with open(KNOWN_CLASSES_FILE, "r") as f:
        known_classes = json.load(f)
else:
    known_classes = []

# Load visual memory
if os.path.exists(VISUAL_MEMORY_FILE):
    with open(VISUAL_MEMORY_FILE, "r") as f:
        visual_memory = json.load(f)
else:
    visual_memory = []

def save_known_classes():
    with open(KNOWN_CLASSES_FILE, "w") as f:
        json.dump(known_classes, f, indent=2)

def save_visual_memory():
    with open(VISUAL_MEMORY_FILE, "w") as f:
        json.dump(visual_memory, f, indent=2)

def extract_color_histogram(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [4, 4, 4], [0, 180, 0, 256, 0, 256])
    return (hist / hist.sum()).flatten().tolist()

def is_similar(hist1, hist2, threshold=0.25):
    h1 = np.array(hist1)
    h2 = np.array(hist2)
    dist = cv2.compareHist(h1.astype("float32"), h2.astype("float32"), cv2.HISTCMP_BHATTACHARYYA)
    return dist < threshold

def identify_or_ask(frame_crop):
    current_hist = extract_color_histogram(frame_crop)
    for memory in visual_memory:
        if is_similar(memory["hist"], current_hist):
            return memory["label"]

    temp_path = os.path.join(tempfile.gettempdir(), "current_unknown.png")
    cv2.imwrite(temp_path, frame_crop)
    try:
        os.startfile(temp_path)
    except:
        webbrowser.open(temp_path)

    label = input("❓ What is this object? (check the image) → ").strip().lower()
    if label and label not in known_classes:
        known_classes.append(label)
        save_known_classes()
    visual_memory.append({"label": label, "hist": current_hist})
    save_visual_memory()
    return label

def save_yolo_labels(fname_base, frame_size, boxes):
    label_path = os.path.join(UNKNOWN_DIR, f"{fname_base}.txt")
    w, h = frame_size
    with open(label_path, "w") as f:
        for box in boxes:
            x1, y1, x2, y2 = box["box"]
            xc = ((x1 + x2) / 2) / w
            yc = ((y1 + y2) / 2) / h
            bw = (x2 - x1) / w
            bh = (y2 - y1) / h
            label = box["label"]
            class_id = known_classes.index(label)
            f.write(f"{class_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

def log_unknown(filename, detections):
    entry = {"timestamp": datetime.now().isoformat(), "file": filename, "detections": detections}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def analyze_frame(frame=None):
    if frame is None:
        frame = capture_game_window()
    if frame is None:
        print("❌ No game window captured.")
        return {}

    print("👁️ Frame captured and processed.")
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    crosshair_rgb = frame[cy, cx].tolist()

    results = model(frame, verbose=False)[0]
    detections = []
    unknowns = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        raw_label = model.names[cls_id]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = frame[y1:y2, x1:x2]

        label = identify_or_ask(crop)
        box_data = {
            "label": label,
            "confidence": round(conf, 2),
            "box": [x1, y1, x2, y2]
        }

        detections.append(box_data)
        if raw_label not in known_classes:
            unknowns.append(box_data)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    if unknowns:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname_base = f"{timestamp}"
        cv2.imwrite(os.path.join(UNKNOWN_DIR, f"{fname_base}.png"), frame)
        save_yolo_labels(fname_base, (w, h), unknowns)
        log_unknown(f"{fname_base}.png", unknowns)
        print(f"📸 Saved labeled data to {fname_base}.png and .txt")

    return {
        "detections": detections,
        "crosshair_rgb": crosshair_rgb
    }
