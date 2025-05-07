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
