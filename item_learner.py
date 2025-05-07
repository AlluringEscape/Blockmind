import json
import os
from scipy.spatial import distance

PROFILE_FILE = "item_profiles.json"

def load_item_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_item_profiles(profiles):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def describe_color(color):
    r, g, b = color
    if r > 200 and g < 100 and b < 100:
        return "red"
    elif g > 200 and r < 100 and b < 100:
        return "green"
    elif b > 200 and r < 100 and g < 100:
        return "blue"
    elif r > 180 and g > 180 and b > 180:
        return "light"
    elif r < 50 and g < 50 and b < 50:
        return "dark"
    else:
        return "neutral"

def predict_item(color, profiles, threshold=50):
    closest_label = "Unknown"
    closest_dist = float('inf')
    for label, colors in profiles.items():
        for c in colors:
            dist = distance.euclidean(color, c)
            if dist < closest_dist:
                closest_dist = dist
                closest_label = label
    return closest_label if closest_dist < threshold else "Unknown"

def learn_new_item(color, profiles, interactive=True, image=None, bbox=None):
    color = [int(x) for x in color]
    base = "item_" + describe_color(color)
    i = 1
    while True:
        label = f"{base}_{i:03d}"
        if label not in profiles:
            break
        i += 1

    print(f"🧠 Auto-learned item at {color} → {label}")
    if label not in profiles:
        profiles[label] = []
    profiles[label].append(color)
    save_item_profiles(profiles)
    return label
