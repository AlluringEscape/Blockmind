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


import pyautogui
import blockmind_vision
import cv2
from PIL import ImageGrab
import numpy as np
import logging

def gather_wood():
    """
    Perform the Minecraft task: gather wood.
    
    This function takes a screenshot, analyzes it for blocks of wood,
    and returns True if any are found. If no blocks are detected, 
    it returns False.

    Args:
        None

    Returns:
        bool: Whether any blocks of wood were detected
    """

    # Take a screenshot of the Minecraft window
    img = pyautogui.screenshot(region=(0, 30, 800, 600))  # Assuming Minecraft is open on the left side of the screen
    
    # Convert the image to an OpenCV image
    frame = np.array(img)
    
    # Resize the frame for faster analysis
    frame = cv2.resize(frame, (400, 300))
    
    # Analyze the frame using BlockMind vision
    blocks = blockmind_vision.analyze_frame(frame)
    
    # Check if any wood is detected in the scene
    if 'wood' in blocks:
        logging.info('Detected wood blocks!')
        return True
    
    # If no wood is detected, log and return False
    else:
        logging.warning('No wood blocks detected.')
        return False

# Example usage
if __name__ == "__main__":
    result = gather_wood()
    print(result)
