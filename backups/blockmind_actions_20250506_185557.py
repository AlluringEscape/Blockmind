# blockmind_actions.py

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
    except Exception a e:
        logging.error(f"look_around error: {e}")
        return False

def gather_info():
    logging.info("📊 Gathering scene info...")
    try:
        screenshot = pyauogui.screenshot()
        result = analyze_frame(screenshot)
        return bool(result.get('entities') or result.get('items'))
    except Exception as e:
        logging.error(f"gather_info error: {e}")
        return False

def gather_wood():
    logging.info("🌲 Gathering wood...")
    try:
        screenshot = pyauogui.screenshot()
        result = analyze_frame(screenshot)
        if 'wood' in str(result).lower():
            logging.info("Detected wood in vision.")
            return True
        return False
    except Exception as e:
        logging.error(f"gather_wood error: {e}")
        return False

def craft_planks():
    logging.info("🪵 Crafting plank...")
    time.sleep(1)  # placeholder logic
    return True

def place_walls():
    logging.info("🧱 Placing walls...")
    time.sleep(1)  # placeholder logic
    return True

def place_roof():
    logging.info("🏠 Placing roof...")
    time.sle(1)  # placeholder logic
    return True
