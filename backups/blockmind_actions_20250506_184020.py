import pyautogui
import numpy as np
import logging
from blockmind_vision import analyze_frame


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


import pyautogui
from blockmind_vision import analyze_frame
import logging

def gather_wood():
    """
    Bot function to fix the skill: gather_wood
    """
    
    # Check if Minecraft window is on screen
    try:
        screenshot = pyautogui.screenshot()
    except Exception as e:
        print(f"Error taking screenshot: {str(e)}")
        return False

    logging.info("Taking screenshot")

    # Analyze the frame for blocks, items or entities
    result = analyze_frame(screenshot)

    if result is not None:
        # Found something meaningful (like wood)
        print("Found something!")
        return True
    
    # If nothing was found, try to click on a nearby block
    else:
        logging.info("Clicking on a nearby block")
        # Implement logic to find and click on a nearby block here
        # For now, we just assume it finds one
        return True

# Example usage:
if __name__ == "__main__":
    gather_wood()
