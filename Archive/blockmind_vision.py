import numpy as np
import cv2
import json
import os
from scipy.spatial import distance
from object_detector import detect_objects
from entity_learner import (
    load_profiles,
    predict_entity,
    learn_new_entity
)
from block_learner import (
    load_block_profiles,
    predict_block,
    learn_new_block
)
from item_learner import (
    load_item_profiles,
    predict_item,
    learn_new_item
)
from biome_detector import (
    load_biome_profiles,
    predict_biome,
    learn_new_biome
)
from feature_detector import detect_features, detect_structures
from dimension_detector import detect_dimension

# === Utilities ===
def get_average_color(bbox, image):
    x1, y1, x2, y2 = bbox
    crop = image[y1:y2, x1:x2]
    if crop.size == 0:
        return [0, 0, 0]
    avg_color = crop.mean(axis=0).mean(axis=0)
    return [int(c) for c in avg_color]

# === Scene Analysis ===
def analyze_frame(image):
    profiles = load_profiles()
    block_profiles = load_block_profiles()
    item_profiles = load_item_profiles()
    biome_profiles = load_biome_profiles()

    scene = {
        "entities": [],
        "blocks": [],
        "items": [],
        "sky": None,
        "biome": "unknown",
        "features": [],
        "structures": [],
        "dimension": "unknown",
        "player": {
            "health": "unknown",
            "food": "unknown"
        }
    }

    # === BIOME DETECTION ===
    avg_scene_rgb = image.mean(axis=0).mean(axis=0)
    avg_rgb = [int(x) for x in avg_scene_rgb]
    biome = predict_biome(avg_rgb, biome_profiles)
    if biome == "unknown":
        biome = learn_new_biome(avg_rgb, biome_profiles)
    scene["biome"] = biome

    # === DIMENSION DETECTION ===
    scene["dimension"] = detect_dimension(image)

    # === FEATURE & STRUCTURE DETECTION ===
    scene["features"] = detect_features(image)
    scene["structures"] = detect_structures(image)

    # === OBJECT DETECTION ===
    detections = detect_objects(image)
    for obj in detections:
        avg_rgb = get_average_color(obj["bbox"], image)
        label = predict_entity(avg_rgb, profiles)

        if label == "Unknown":
            label = learn_new_item(avg_rgb, item_profiles, interactive=False)


            print(f"🆕 Learned and labeled entity: {label}")
        else:
            print(f"👁️ Recognized {label} at {avg_rgb}")

        categorized = {
            "label": label,
            "rgb": avg_rgb,
            "bbox": obj["bbox"]
        }

        # === ENTITY CHECK ===
        if label.lower() in [
            "cow", "pig", "sheep", "zombie", "creeper", "villager", "chicken", "spider", "person"
        ]:
            scene["entities"].append(categorized)
            continue

        # === BLOCK CHECK ===
        block_label = predict_block(avg_rgb, block_profiles)
        if block_label != "Unknown":
            categorized["label"] = block_label
            print(f"🧱 Recognized block: {block_label} at {avg_rgb}")
            scene["blocks"].append(categorized)
            continue

        # === ITEM CHECK ===
        item_label = predict_item(avg_rgb, item_profiles)
        if item_label == "Unknown":
            item_label = learn_new_item(avg_rgb, item_profiles, interactive=True)
            print(f"🎒 Learned and labeled item: {item_label}")
        else:
            print(f"🎒 Recognized item: {item_label} at {avg_rgb}")
        categorized["label"] = item_label
        scene["items"].append(categorized)

    return scene
