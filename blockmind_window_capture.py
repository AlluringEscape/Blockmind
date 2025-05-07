import pyautogui
import cv2
import numpy as np

# Use your selected region from the selector
REGION = (2552, 1, 2554, 1370)

def capture_game_window():
    screenshot = pyautogui.screenshot(region=REGION)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return frame

def stop_camera():
    pass  # Placeholder for compatibility
