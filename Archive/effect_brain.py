import json

def load_effect_profiles(file_path="effect_profiles.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def classify_effect(effect_name, profiles):
    if effect_name in profiles["positive"]:
        return "positive"
    elif effect_name in profiles["negative"]:
        return "negative"
    return "unknown"
