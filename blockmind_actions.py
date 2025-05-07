import time
import logging
import pyautogui
import numpy as np
import cv2
from blockmind_vision import analyze_frame

# === Base Actions ===

def look_around():
    logging.info("👀 Looking around...")
    try:
        screenshot = pyautogui.screenshot()
        result = analyze_frame(screenshot)
        return bool(result.get('entities') or result.get('items'))
    except Exception as e:
        logging.error(f"look_around error: {e}")
        return False

def gather_info():
    logging.info("📊 Gathering scene info...")
    try:
        screenshot = pyautogui.screenshot()
        result = analyze_frame(screenshot)
        return bool(result.get('entities') or result.get('items'))
    except Exception as e:
        logging.error(f"gather_info error: {e}")
        return False

def gather_wood():
    logging.info("🌲 Gathering wood...")
    try:
        screenshot = pyautogui.screenshot(region=(0, 30, 800, 600))
        frame = np.array(screenshot)
        frame = cv2.resize(frame, (400, 300))
        blocks = analyze_frame(frame)
        if 'wood' in str(blocks).lower():
            logging.info('Detected wood blocks!')
            return True
        logging.warning('No wood blocks detected.')
        return False
    except Exception as e:
        logging.error(f"gather_wood error: {e}")
        return False

def craft_planks():
    logging.info("🪵 Crafting plank...")
    time.sleep(1)
    return True

def place_walls():
    logging.info("🧱 Placing walls...")
    time.sleep(1)
    return True

def place_roof():
    logging.info("🏠 Placing roof...")
    time.sleep(1)
    return True


def walk_to_tree():
    import pygetwindow as gw
    import pyautogui
    import time
    import numpy as np
    import cv2
    from blockmind_vision import analyze_frame

    try:
        print("🎮 Performing action: walk_to_tree")
        win = gw.getWindowsWithTitle("Minecraft")[0]
        x, y, w, h = win.left, win.top, win.width, win.height

        # Screenshot and crop to game window
        full = pyautogui.screenshot()
        cropped = full.crop((x, y, x + w, y + h))
        img = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR)
        scene = analyze_frame(img)

        # Find tree or fallback block
        targets = [b for b in scene['blocks'] if 'tree' in b['label'].lower() or 'wood' in b['label'].lower()]
        if not targets:
            print("🌲 No tree detected")
            return False

        # Use first detected tree block
        target = targets[0]
        bx1, by1, bx2, by2 = target["bbox"]
        center_x = x + (bx1 + bx2) // 2
        center_y = y + (by1 + by2) // 2

        # Move mouse to tree and walk
        pyautogui.moveTo(center_x, center_y)
        pyautogui.mouseDown()
        pyautogui.keyDown('w')
        time.sleep(2.5)
        pyautogui.keyUp('w')
        pyautogui.mouseUp()
        return True
    except Exception as e:
        import logging
        logging.error(f"walk_to_tree error: {e}")
        return False
def punch_tree():
    logging.info("👊 Punching tree...")
    try:
        pyautogui.mouseDown()
        time.sleep(4.5)  # Hold long enough to break a log
        pyautogui.mouseUp()
        return True
    except Exception as e:
        logging.error(f"punch_tree error: {e}")
        return False

def collect_log():
    logging.info("🎒 Collecting dropped log...")
    try:
        pyautogui.keyDown('w')
        time.sleep(1.0)
        pyautogui.keyUp('w')
        return True
    except Exception as e:
        logging.error(f"collect_log error: {e}")
        return False
