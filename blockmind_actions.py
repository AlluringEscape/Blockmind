import pyautogui
import time
import random
from pynput import keyboard

class ActionHandler:
    def __init__(self):
        self.keyboard = keyboard.Controller()
        self.mouse = pyautogui
        self.window_region = (0, 0, 0, 0)
        
    def set_window_region(self, region):
        self.window_region = region
        
    def execute(self, action):
        if action["type"] == "mine":
            return self._execute_mine(action)
        return self._execute_explore()
    
    def _execute_mine(self, action):
        if not action.get("center"):
            return {"status": "no_target"}
            
        # Convert to absolute screen coordinates
        abs_x = self.window_region[0] + action["center"][0]
        abs_y = self.window_region[1] + action["center"][1]
        
        # Move and click
        self.mouse.moveTo(abs_x, abs_y, duration=0.3)
        time.sleep(0.2)
        
        duration = 2.5 if action["target"] == "tree" else 4.0
        self.mouse.mouseDown()
        time.sleep(duration)
        self.mouse.mouseUp()
        return {"status": "mined", "item": action["target"]}
    
    def _execute_explore(self):
        # Move forward with random turns
        self.keyboard.press('w')
        move_duration = random.uniform(1.0, 2.5)
        time.sleep(move_duration)
        self.keyboard.release('w')
        
        # Random horizontal look
        self.mouse.move(
            random.choice([100, -100]), 
            0, 
            duration=0.5
        )
        return {"status": "exploring"}