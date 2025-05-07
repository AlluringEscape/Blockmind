
import time
import pyautogui
import numpy as np
import cv2
from PIL import ImageGrab

def get_crosshair_color(region=(960, 540, 5, 5)):
    img = np.array(ImageGrab.grab(bbox=region))
    avg_color = np.mean(img, axis=(0, 1))
    return avg_color

def punch_tree():
    print("🌳 Starting to punch tree...")
    start_color = get_crosshair_color()
    pyautogui.mouseDown()
    time.sleep(1.0)
    pyautogui.mouseUp()
    end_color = get_crosshair_color()
    color_change = np.linalg.norm(np.array(start_color) - np.array(end_color))
    print(f"🎯 Block color change: {color_change:.2f}")

    if color_change > 8.0:
        print("✅ Block is breaking. Continuing punch.")
        pyautogui.mouseDown()
        time.sleep(1.5)
        pyautogui.mouseUp()
        return True
    else:
        print("❌ No progress punching. Repositioning or retrying.")
        pyautogui.moveRel(10, 0)
        time.sleep(0.5)
        return False

def walk_to_tree():
    print("🚶 Walking to tree...")
    pyautogui.keyDown('w')
    time.sleep(1.5)
    pyautogui.keyUp('w')

def collect_log():
    print("🎒 Collecting log...")
    pyautogui.keyDown('w')
    time.sleep(0.5)
    pyautogui.keyUp('w')

# Add other actions as needed
