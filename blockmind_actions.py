import time
import pyautogui
import numpy as np
from PIL import ImageGrab


def get_crosshair_color():
    x, y = pyautogui.size()
    center_x, center_y = x // 2, y // 2
    left = min(center_x - 5, center_x + 5)
    right = max(center_x - 5, center_x + 5)
    top = min(center_y - 5, center_y + 5)
    bottom = max(center_y - 5, center_y + 5)

    try:
        img = np.array(ImageGrab.grab(bbox=(left, top, right, bottom)))
        center_pixel = img[(bottom - top) // 2, (right - left) // 2]
        return center_pixel.tolist()
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
        return [0, 0, 0]


def punch_tree():
    print("🌳 Starting to punch tree...")
    try:
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
            print("❌ No progress punching. Repositioning.")
            pyautogui.moveRel(10, 0)
            time.sleep(0.5)
            return False
    except Exception as e:
        print(f"❌ Action error: {e}")
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
