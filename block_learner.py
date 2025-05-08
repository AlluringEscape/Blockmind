import json
import os
from scipy.spatial import distance

PROFILE_FILE = "block_profiles.json"

def load_block_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_block_profiles(profiles):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def match_block_label(color, profiles, threshold=60):
    closest_label = "Unknown"
    closest_dist = float('inf')

    for label, colors in profiles.items():
        for c in colors:
            dist = distance.euclidean(color, c)
            if dist < closest_dist:
                closest_dist = dist
                closest_label = label

    return closest_label if closest_dist < threshold else "Unknown"

def learn_block(label, color, profiles):
    color = [int(x) for x in color]
    if label not in profiles:
        profiles[label] = []
    profiles[label].append(color)
    save_block_profiles(profiles)

def detect_blocks(frame, profiles):
    height, width, _ = frame.shape
    cx, cy = width // 2, height // 2
    center_rgb = frame[cy, cx].tolist()

    label = match_block_label(center_rgb, profiles)
    return [{
        "label": label,
        "center": (cx, cy),
        "rgb": center_rgb
    }]
