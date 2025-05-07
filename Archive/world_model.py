
import json
import os
from datetime import datetime

WORLD_STATE_FILE = "map_andy.json"
POSITION_LOG_FILE = "movement_log.json"

class WorldModel:
    def __init__(self):
        self.landmarks = []
        self.position_history = []
        self.load()

    def add_landmark(self, label, position, color=None):
        for lm in self.landmarks:
            if lm["label"] == label and lm["position"] == position:
                return  # Skip duplicates
        self.landmarks.append({
            "label": label,
            "position": position,
            "color": color,
            "time": datetime.now().isoformat()
        })
        self.save()

    def update_position(self, position):
        self.position_history.append({
            "position": position,
            "time": datetime.now().isoformat()
        })
        self.save()

    def save(self):
        try:
            with open(WORLD_STATE_FILE, "w") as f:
                json.dump({"landmarks": self.landmarks}, f, indent=2)
            with open(POSITION_LOG_FILE, "w") as f:
                json.dump(self.position_history, f, indent=2)
            print("🗺️ Map memory saved")
        except Exception as e:
            print(f"❌ Failed to save world model: {e}")

    def load(self):
        if os.path.exists(WORLD_STATE_FILE):
            try:
                with open(WORLD_STATE_FILE, "r") as f:
                    data = json.load(f)
                    self.landmarks = data.get("landmarks", [])
                print(f"🗺️ Map memory loaded ({len(self.landmarks)} landmarks)")
            except Exception as e:
                print(f"❌ Failed to load map memory: {e}")

        if os.path.exists(POSITION_LOG_FILE):
            try:
                with open(POSITION_LOG_FILE, "r") as f:
                    self.position_history = json.load(f)
            except Exception as e:
                print(f"❌ Failed to load position log: {e}")

# Singleton instance
world_model = WorldModel()
