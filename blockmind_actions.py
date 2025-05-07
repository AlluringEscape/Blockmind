import pyautogui
import time
from pynput import keyboard

class ActionHandler:
    def __init__(self):
        self.keyboard = keyboard.Controller()
        self.mouse = pyautogui
        
    def execute(self, action):
        action_type = action.get("type")
        
        if action_type == "mine":
            return self.mine(action.get("target"))
        elif action_type == "explore":
            return self.move_random()
        return {"status": "unknown_action"}
    
    def mine(self, target):
        # Calculate mining time based on target
        duration = 2.0 if target == "tree" else 3.0
        pyautogui.mouseDown(button='left')
        time.sleep(duration)
        pyautogui.mouseUp()
        return {"status": "mined", "item": target}
    
    def move_random(self):
        directions = ['w', 'a', 's', 'd']
        self.keyboard.press(random.choice(directions))
        time.sleep(1.0)
        self.keyboard.release(random.choice(directions))
        return {"status": "moved"}