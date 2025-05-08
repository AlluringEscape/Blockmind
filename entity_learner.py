import json
import os
import cv2
import numpy as np
from scipy.spatial import distance

PROFILE_FILE = "entity_profiles.json"

MINECRAFT_MOBS = {
    "passive": [...],
    "neutral": [...],
    "hostile": [...],
    "boss": ["ender_dragon", "wither"]
}

ALL_MOBS = set(sum(MINECRAFT_MOBS.values(), []))

def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def predict_entity(color, profiles, threshold=50):
    closest_label = "Unknown"
    closest_dist = float('inf')
    for label, colors in profiles.items():
        for c in colors:
            dist = distance.euclidean(color, c)
            if dist < closest_dist:
                closest_dist = dist
                closest_label = label
    return closest_label if closest_dist < threshold else "Unknown"

def describe_color(color):
    r, g, b = color
    if r > 200 and g < 100 and b < 100:
        return "red_thing"
    elif g > 200 and r < 100 and b < 100:
        return "green_thing"
    elif b > 200 and r < 100 and g < 100:
        return "blue_thing"
    elif r > 180 and g > 180 and b > 180:
        return "light_thing"
    elif r < 50 and g < 50 and b < 50:
        return "dark_thing"
    else:
        return "thing"

def generate_unknown_label(profiles):
    i = 1
    while True:
        label = f"unk_{i:03d}"
        if label not in profiles:
            return label
        i += 1

def learn_new_entity(color, profiles, interactive=False, image=None, bbox=None):
    color = [int(x) for x in color]
    guess = describe_color(color)
    label = f"{guess}_{len(profiles)}"
    print(f"🧠 Auto-learned entity at {color} → {label}")
    if label not in profiles:
        profiles[label] = []
    profiles[label].append(color)
    save_profiles(profiles)
    return label

def detect_entities(frame, profiles=None):
    if profiles is None:
        profiles = {}
    # Add your detection logic here
    return []

