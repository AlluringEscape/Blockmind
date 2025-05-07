# blockmind_launcher.py (to create)
import json
import time
from blockmind_brain import BlockmindBrain
from blockmind_gui import launch_gui  # optional GUI launcher
from pathlib import Path

# Load config
with open("config.json") as f:
    settings = json.load(f)

# Load agent profiles (andy.json)
for profile_path in settings["profiles"]:
    with open(profile_path) as f:
        profile = json.load(f)
    
    name = profile.get("name", "Agent")
    print(f"🤖 Launching Blockmind agent: {name}")

    brain = BlockmindBrain(profile=profile)
    brain.start(init_message=settings.get("init_message", ""))

    time.sleep(1)  # Delay to avoid overlap
