import json
import os
from scipy.spatial import distance

BIOME_PROFILE_FILE = "biome_profiles.json"

# Predefined biome RGB color hints (based on sky/ground/scene colors)
BIOME_COLOR_HINTS = {
    "plains":       [120, 180, 90],     # green grass
    "forest":       [85, 140, 70],      # darker green
    "desert":       [230, 220, 160],    # light sand
    "savanna":      [190, 180, 80],     # yellow grass
    "jungle":       [70, 100, 50],      # thick, dark green
    "taiga":        [100, 130, 110],    # pine tone
    "snowy_tundra": [210, 210, 210],    # white/silver
    "swamp":        [80, 100, 70],      # brownish-green
    "beach":        [240, 230, 160],    # light sand + water
    "ocean":        [50, 80, 150],      # deep blue
    "nether":       [130, 0, 0],        # red hue
    "end":          [200, 200, 120],    # pale yellow/gray
}

def predict_biome(color, profiles=None, threshold=80):
    closest_label = "unknown"
    closest_dist = float('inf')
    for label, ref_color in BIOME_COLOR_HINTS.items():
        dist = distance.euclidean(color, ref_color)
        if dist < closest_dist:
            closest_dist = dist
            closest_label = label
    return closest_label if closest_dist < threshold else "unknown"

# Dummy function kept for compatibility with blockmind_vision
def load_biome_profiles():
    return {}  # not used anymore

def learn_new_biome(color, profiles=None):
    return predict_biome(color)
