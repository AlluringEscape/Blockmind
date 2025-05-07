import argparse
import json
from blockmind_brain import BlockmindBrain
from overlay_window import run_overlay
import threading

overlay_thread = threading.Thread(target=run_overlay, daemon=True)
overlay_thread.start()



def load_profile(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

class BlockmindAgent:
    def __init__(self, profile_path):
        profile = load_profile(profile_path)
        self.brain = BlockmindBrain(profile)

    def start(self, init_message=None):
        print(f"🧠 Starting AI: {self.brain.name}")
        self.brain.start(init_message=init_message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=str, default="profile.json")
    parser.add_argument("--goal", type=str, help="Initial goal (optional)")
    args = parser.parse_args()

    agent = BlockmindAgent(args.profile)
    agent.start(init_message=f"I want to {args.goal.replace('_', ' ')}." if args.goal else "Let's begin survival.")
