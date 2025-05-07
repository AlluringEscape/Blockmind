import pyautogui
import numpy as np
import logging
from blockmind_vision import analyze_frame

def gather_wood(context=None):
    """
    Attempts to gather wood by analyzing the screen for tree-like structures and clicking on them.

    Returns:
        bool: True if wood-like entities or blocks were detected and interacted with; False otherwise.
    """
    logging.basicConfig(level=logging.INFO)

    try:
        # Take a screenshot and convert it to numpy array for OpenCV
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)

        # Analyze the frame for wood or tree entities
        result = analyze_frame(frame)
        logging.info(f"Vision result: {result}")

        # Check if any entities or blocks look like wood
        wood_found = False
        if result:
            for entity in result.get("entities", []):
                if "tree" in entity["label"].lower() or "log" in entity["label"].lower():
                    x, y, w, h = entity["box"]
                    pyautogui.moveTo(x + w // 2, y + h // 2)
                    pyautogui.click()
                    wood_found = True
                    logging.info("🪓 Interacted with tree/log entity")

            for block in result.get("blocks", []):
                if "wood" in block["label"].lower() or "log" in block["label"].lower():
                    x, y, w, h = block["box"]
                    pyautogui.moveTo(x + w // 2, y + h // 2)
                    pyautogui.click()
                    wood_found = True
                    logging.info("🪓 Interacted with wood/log block")

        return wood_found

    except Exception as e:
        logging.error(f"Error during gather_wood: {e}")
        return False


import pyautogui
from blockmind_vision import analyze_frame
import logging

def look_around():
    """
    Perform the Minecraft task: look around.
    
    This function captures a screenshot of the current game state, analyzes it for meaningful entities or items,
    and returns True if anything is found. Otherwise, it returns False.

    Args:
        None

    Returns:
        bool: Whether any meaningful entities or items were detected in the analysis.
    """
    try:
        # Capture a screenshot of the current game state
        screenshot = pyautogui.screenshot()

        # Analyze the frame for vision
        result = analyze_frame(screenshot)

        # Log and print whether any meaningful entities or items were found
        if result:
            logging.info("Found entities or items in the analysis.")
            return True
        else:
            logging.info("No entities or items found in the analysis.")
            return False

    except Exception as e:
        # Log any exceptions that occur during the process
        logging.error(f"An error occurred while analyzing the frame: {e}")
        return False
