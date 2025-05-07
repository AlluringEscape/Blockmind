
import cv2
import numpy as np
from ultralytics import YOLO
from block_learner import load_block_profiles, predict_block, learn_new_block
from entity_learner import load_profiles as load_entity_profiles, predict_entity, learn_new_entity
from item_learner import load_item_profiles, predict_item, learn_new_item

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load profiles
block_profiles = load_block_profiles()
entity_profiles = load_entity_profiles()
item_profiles = load_item_profiles()

def analyze_frame(frame):
    scene = {
        "blocks": [],
        "entities": [],
        "items": [],
        "player": {"food": "unknown", "health": "unknown"}
    }

    results = model(frame)[0]
    annotated = results.plot()
    cv2.imwrite("vision_annotated.png", annotated)  # Save annotated frame

    h, w = frame.shape[:2]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = map(int, result[:6])
        label = f"Unk_{int(cls):03d}"
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if 0 <= cx < w and 0 <= cy < h:
            color = frame[cy, cx].tolist()

            if cls < 30:
                label = predict_block(color, block_profiles)
                if label == "Unknown":
                    label = learn_new_block(color, block_profiles, interactive=False)
                scene["blocks"].append({
                    "label": label,
                    "bbox": [x1, y1, x2, y2],
                    "color": color
                })

            elif cls < 60:
                label = predict_entity(color, entity_profiles)
                if label == "Unknown":
                    label = learn_new_entity(color, entity_profiles, interactive=False, image=frame, bbox=(x1, y1, x2, y2))
                scene["entities"].append({
                    "label": label,
                    "bbox": [x1, y1, x2, y2],
                    "color": color
                })

            else:
                label = predict_item(color, item_profiles)
                if label == "Unknown":
                    label = learn_new_item(color, item_profiles, interactive=False, image=frame, bbox=(x1, y1, x2, y2))
                scene["items"].append({
                    "label": label,
                    "bbox": [x1, y1, x2, y2],
                    "color": color
                })

    # Fallback: center pixel check for wood-colored blocks
    center_x, center_y = w // 2, h // 2
    center_color = frame[center_y, center_x].tolist()
    brownish = center_color[0] < 100 and center_color[1] < 100 and center_color[2] < 100
    greenish = center_color[1] > center_color[0] and center_color[1] > center_color[2]

    if brownish or greenish:
        scene["blocks"].append({
            "label": "tree_center_pixel",
            "bbox": [center_x-5, center_y-5, center_x+5, center_y+5],
            "color": center_color
        })

    
    # === High-level summary detection ===
    summary = {
        "entity_aliases": ["sheep", "cow", "pig", "chicken"],
        "flower_colors": [(140, 0, 140), (255, 255, 255), (255, 0, 0)],
        "tree": False,
        "tree_aliases": ["tree", "log", "wood", "tree_center_pixel"],
        "cave": False,
        "animal": False,
        "flower": False,
        "sky": False
    }

    for entity in scene["entities"]:
        if any(alias in entity["label"].lower() for alias in summary["entity_aliases"]):
            summary["animal"] = True
        if "sheep" in entity["label"] or "cow" in entity["label"] or "pig" in entity["label"]:
            summary["animal"] = True

    for block in scene["blocks"]:
        avg_color = np.array(block["color"])
        for flower_color in summary["flower_colors"]:
            if np.linalg.norm(avg_color - np.array(flower_color)) < 50:
                summary["flower"] = True
        if any(alias in block["label"].lower() for alias in summary["tree_aliases"]):
            summary["tree"] = True
        if "log" in block["label"] or "wood" in block["label"]:
            summary["tree"] = True
        if "flower" in block["label"]:
            summary["flower"] = True
        if "stone" in block["label"] and block["position"][1] > h * 0.5:
            summary["cave"] = True

    avg_top_brightness = np.mean(frame[0:int(h*0.2), :, :])
    if avg_top_brightness > 60:
        summary["sky"] = True

    del summary["tree_aliases"]
    del summary["tree_aliases"]
    del summary["entity_aliases"]
    del summary["flower_colors"]
    scene["summary"] = summary

    return scene
