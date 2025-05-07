import json
import os
from scipy.spatial import distance

BLOCK_PROFILE_FILE = "block_profiles.json"

def load_block_profiles():
    if os.path.exists(BLOCK_PROFILE_FILE):
        with open(BLOCK_PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_block_profiles(profiles):
    with open(BLOCK_PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def predict_block(color, profiles, threshold=50):
    closest_label = "Unknown"
    closest_dist = float('inf')
    for label, colors in profiles.items():
        for c in colors:
            dist = distance.euclidean(color, c)
            if dist < closest_dist:
                closest_dist = dist
                closest_label = label
    return closest_label if closest_dist < threshold else "Unknown"

def learn_new_block(color, profiles, interactive=True):
    color = [int(x) for x in color]

    if not interactive:
        label = generate_unknown_label(profiles)
        profiles[label] = [color]
        save_block_profiles(profiles)
        return label

    print(f"🆕 Learned new block at RGB {color}")
    suggestion = input("🧱 What block is this? (or press Enter to skip): ").strip()
    if suggestion == "":
        return learn_new_block(color, profiles, interactive=False)

    if suggestion not in profiles:
        profiles[suggestion] = []
    profiles[suggestion].append(color)
    save_block_profiles(profiles)
    return suggestion

def generate_unknown_label(profiles):
    unk_id = 1
    while True:
        label = f"Block_{unk_id:03}"
        if label not in profiles:
            return label
        unk_id += 1
