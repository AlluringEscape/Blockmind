import cv2
from object_detector import detect_objects

def build_scene_model(image):
    scene = {
        "entities": [],
        "blocks": [],
        "sky": None,
        "biome": "unknown",
        "player": {
            "health": "unknown",
            "food": "unknown"
        }
    }

    detections = detect_objects(image)
    for obj in detections:
        label = obj["label"].lower()
        if label in ["cow", "pig", "zombie", "creeper", "sheep", "villager"]:
            scene["entities"].append(obj)
        elif label in ["tree", "grass", "log", "dirt", "stone"]:
            scene["blocks"].append(obj)

    return scene
