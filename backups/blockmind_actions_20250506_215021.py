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
    logging.info("🚶 Walking toward tree...")
    try:
        screenshot = pyautogui.screenshot()
        scene = analyze_frame(screenshot)
        wood_blocks = [b for b in scene.get("blocks", []) if any(alias in b["label"].lower() for alias in WOOD_ALIASES)]

        if not wood_blocks:
            logging.warning("No trees in view.")
            return False

        target = wood_blocks[0]
        x, y, _ = target["box"]  # Get bounding box center
        logging.info(f"🎯 Targeting tree at ({x}, {y})")
        pyautogui.moveTo(x, y + 30)  # Offset for window title bar
        pyautogui.keyDown('w')
        time.sleep(1.5)
        pyautogui.keyUp('w')
        return True
    except Exception as e:
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
