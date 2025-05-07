
import pyautogui
import numpy as np
import json
from blockmind_vision import analyze_frame

class ActionHandler:
    def __init__(self):
        pass

    def perform(self, action_name):
        if hasattr(self, action_name):
            method = getattr(self, action_name)
            return method()
        else:
            print(f"⚠️ Unknown action: {action_name}")
            return False

    def scan_area(self):
        """
        Scan and analyze the surrounding area. Useful for situational awareness.
        """
        screenshot = self.capture_game_frame()
        if screenshot is None:
            print("❌ scan_area: No screenshot available.")
            return False

        scene = analyze_frame()
        print(f"🔍 Scan Results: {json.dumps(scene, indent=2)}")
        return True

    def capture_game_frame(self):
        return np.array(pyautogui.screenshot())
