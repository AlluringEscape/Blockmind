import time
import pyautogui
import numpy as np
from PIL import ImageGrab
from blockmind_vision import analyze_frame

CROSSHAIR_REGION = (1280 - 5, 720 - 5, 1280 + 5, 720 + 5)  # center 10x10
COLOR_CHANGE_THRESHOLD = 10.0

def get_crosshair_color(region=CROSSHAIR_REGION):
    img = np.array(ImageGrab.grab(bbox=region))
    avg_color = img.mean(axis=(0, 1))
    return avg_color

def jump_forward():
    pyautogui.keyDown("space")
    pyautogui.keyDown("w")
    time.sleep(0.4)
    pyautogui.keyUp("space")
    pyautogui.keyUp("w")
    print("🦘 Attempted jump forward.")

def walk_to_tree():
    print("🚶 Walking to tree...")
    pyautogui.keyDown("w")
    time.sleep(1.5)
    pyautogui.keyUp("w")

def punch_tree():
    print("🌳 Starting to punch tree...")
    try:
        start_color = get_crosshair_color()
        pyautogui.mouseDown()
        time.sleep(1.2)
        pyautogui.mouseUp()
        time.sleep(0.1)
        new_color = get_crosshair_color()
        delta = np.linalg.norm(start_color - new_color)
        print(f"🎯 Block color change: {delta:.2f}")
        if delta < COLOR_CHANGE_THRESHOLD:
            print("❌ No progress punching. Repositioning.")
            jump_forward()
    except Exception as e:
        print(f"⚠️ punch_tree failed: {e}")

def collect_log():
    print("🎒 Collecting log...")
    pyautogui.press("e")
    time.sleep(0.5)
    pyautogui.press("e")
