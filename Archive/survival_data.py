import json
import os

SURVIVAL_GUIDE_FILE = "data/survival_guide.json"

def load_survival_guide():
    if os.path.exists(SURVIVAL_GUIDE_FILE):
        with open(SURVIVAL_GUIDE_FILE, "r") as f:
            return json.load(f)
    else:
        print(f"⚠️ Missing survival guide at {SURVIVAL_GUIDE_FILE}")
        return {}
