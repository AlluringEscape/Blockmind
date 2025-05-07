import json
import os
from collections import defaultdict

NAVIGATION_FILE = "navigation_memory.json"

def load_navigation_memory():
    if os.path.exists(NAVIGATION_FILE):
        with open(NAVIGATION_FILE, "r") as f:
            data = json.load(f)
            return defaultdict(int, data)
    return defaultdict(int)

def save_navigation_memory(history):
    with open(NAVIGATION_FILE, "w") as f:
        json.dump(dict(history), f, indent=2)
