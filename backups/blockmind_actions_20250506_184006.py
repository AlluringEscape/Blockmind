import pyautogui
import numpy as np
import logging
from blockmind_vision import analyze_frame


def gather_wood(context=None):
    """
    Detect and click on tree/log blocks using vision.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        frame = np.array(pyautogui.screenshot())
        result = analyze_frame(frame)
        logging.info(f"Vision result: {result}")

        wood_found = False
        if result:
            for entity in result.get("entities", []):
                if "tree" in entity["label"].lower() or "log" in entity["label"].lower():
                    x, y, w, h = entity["box"]
                    pyautogui.moveTo(x + w // 2, y + h // 2)
                    pyautogui.click()
                    wood_found = True
                    logging.info("🪓 Clicked tree/log entity")

            for block in result.get("blocks", []):
                if "wood" in block["label"].lower() or "log" in block["label"].lower():
                    x, y, w, h = block["box"]
                    pyautogui.moveTo(x + w // 2, y + h // 2)
                    pyautogui.click()
                    wood_found = True
                    logging.info("🪓 Clicked wood/log block")

        return wood_found
    except Exception as e:
        logging.error(f"Error during gather_wood: {e}")
        return False


def gather_info(context=None):
    """
    Scan for any visible entities/items using vision.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        frame = np.array(pyautogui.screenshot())
        result = analyze_frame(frame)
        if result:
            logging.info(f"Detected: {result}")
            return True
    except Exception as e:
        logging.error(f"Error gathering info: {str(e)}")
    logging.info("Nothing detected.")
    return False


def look_around(context=None):
    """
    Use vision to scan for meaningful nearby objects.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        frame = np.array(pyautogui.screenshot())
        result = analyze_frame(frame)
        if result:
            logging.info("👁️ Vision detected objects!")
            return True
    except Exception as e:
        logging.error(f"Error analyzing frame: {str(e)}")
    logging.info("No objects found.")
    return False
