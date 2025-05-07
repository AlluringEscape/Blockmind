import pyautogui
import time
from PIL import ImageGrab
import numpy as np
from blockmind_vision import analyze_frame, get_latest_detection

# --- Constants ---
CROSSHAIR_REGION = (1275, 691, 1285, 701)
COLOR_DIFF_THRESHOLD = 5.0
REPOSITION_ATTEMPT_LIMIT = 3

def get_crosshair_color(region=CROSSHAIR_REGION):
    img = np.array(ImageGrab.grab(bbox=region))
    return img.mean(axis=(0, 1))

def punch_tree():
    print("🌳 Starting to punch tree...")

    start_color = get_crosshair_color()
    pyautogui.mouseDown(button='left')
    time.sleep(1.0)
    pyautogui.mouseUp()

    time.sleep(0.5)
    end_color = get_crosshair_color()
    diff = np.linalg.norm(start_color - end_color)

    print(f"🎯 Block color change: {diff:.2f}")
    if diff < COLOR_DIFF_THRESHOLD:
        print("❌ No progress punching. Repositioning.")
        jump_forward()
        return False
    return True

def jump_forward():
    print("🦘 Attempted jump forward.")
    pyautogui.keyDown("space")
    pyautogui.keyDown("w")
    time.sleep(0.5)
    pyautogui.keyUp("space")
    pyautogui.keyUp("w")

def walk_to_tree():
    print("🚶 Walking to tree...")
    tree = get_latest_detection("tree_center_pixel")
    if not tree:
        print("❌ No tree found.")
        return False

    # If tree isn't centered in view, move slightly
    bbox = tree["bbox"]
    x_center = (bbox[0] + bbox[2]) / 2
    screen_center_x = 1280  # Assuming 2560x1440 split screen
    delta_x = x_center - screen_center_x
    if abs(delta_x) > 30:
        direction = "right" if delta_x > 0 else "left"
        pyautogui.keyDown(direction)
        time.sleep(0.2)
        pyautogui.keyUp(direction)

    pyautogui.keyDown("w")
    time.sleep(0.7)
    pyautogui.keyUp("w")
    return True

def collect_log():
    print("🎒 Collecting log...")
    pyautogui.moveRel(0, 0)  # Just to reset any move hangups
    time.sleep(0.2)
