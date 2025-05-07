import pyautogui
import time
from pynput import keyboard

class ActionHandler:
    def __init__(self):
        self.controller = keyboard.Controller()
        self.action_map = {
            "move": self.move,
            "mine": self.mine,
            "craft": self.craft,
            "evade": self.evade,
            "collect": self.collect
        }

    def execute(self, action):
        return self.action_map[action["type"]](**action["params"])

    def move(self, direction, duration=1.0):
        self.controller.press(direction)
        time.sleep(duration)
        self.controller.release(direction)
        return {"status": "success", "distance": duration*4}

    def mine(self, target):
        pyautogui.mouseDown(button='left')
        time.sleep(1.5 if target == "wood" else 3.0)
        pyautogui.mouseUp()
        return {"status": "success", "item": target}

    def craft(self, item):
        pyautogui.press('e')
        time.sleep(0.5)
        # Add crafting logic based on item
        return {"status": "crafted", "item": item}