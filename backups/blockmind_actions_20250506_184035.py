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


import pyautogui
import cv2
from blockmind_vision import analyze_frame
import numpy as np
import logging

def craft_planks():
    """
    Perform the Minecraft task: craft planks.
    
    This function captures a screenshot, uses BlockMind Vision to detect items,
    and returns True if anything meaningful is detected. Otherwise, it returns False.
    
    Parameters:
    None
    
    Returns:
    bool: Whether any meaningful item was found
    """
    
    # Set up logging to print out the result of the detection
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Capture a screenshot of the Minecraft window
        img = pyautogui.screenshot()
        
        # Convert the image to a numpy array for analysis
        frame = np.array(img)
        
        # Use BlockMind Vision to analyze the frame
        result = analyze_frame(frame)
        
        # Check if any items were found
        if result['items']:
            logging.info("Detected planks in inventory")
            return True
        
    except Exception as e:
        # Log and print any exceptions that occur during the process
        logging.error(f"An error occurred: {e}")
    
    # If no items were found, log and print a message
    logging.info("No meaningful items detected in inventory")
    
    # Return False to indicate that nothing was detected
    return False

# Call the function to craft planks
craft_planks()
