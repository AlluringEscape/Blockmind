import json
import random
import os
import logging
import pyautogui
import numpy as np
from survival_data import load_survival_guide
from blockmind_vision import analyze_frame

# === CONFIG ===
SURVIVAL_GUIDE_FILE = "data/survival_guide.json"

# === LOAD SURVIVAL GUIDE ===
def load_survival_tips():
    if os.path.exists(SURVIVAL_GUIDE_FILE):
        with open(SURVIVAL_GUIDE_FILE, 'r') as f:
            return json.load(f)
    return {}

survival_tips = load_survival_tips()

# === CONTEXT HANDLING ===
def match_context_to_tips(context):
    context_lower = context.lower()
    for tag, tips in survival_tips.items():
        if tag.lower() in context_lower:
            return tag, tips
    return None, []

def choose_best_tip(tips):
    return random.choice(tips) if tips else None

# === DECISION ENGINE ===
def get_survival_tip(context):
    tag, tips = match_context_to_tips(context)
    tip = choose_best_tip(tips)
    if tip:
        return tag, tip
    else:
        fallback_tip = random.choice([
            "Explore the surrounding area to collect information.",
            "Collect nearby resources like wood or stone.",
            "Find or build shelter before nightfall.",
            "Craft basic tools using available materials.",
            "Look for food sources such as animals or crops."
        ])
        return None, fallback_tip

# === MAIN DECISION FUNCTION ===
def decide_next_survival_action(observations, memory):
    context = " ".join(observations)
    tag, tip = get_survival_tip(context)
    return f"Survival Tip [{tag}]: {tip}", (tag, tip)

# === DEBUG USAGE ===
if __name__ == "__main__":
    test_context = ["It is getting dark", "I see zombies nearby", "I'm near a river"]
    memory = []
    result, detail = decide_next_survival_action(test_context, memory)
    print(result)
    print(detail)


# === NEW SKILLS ===
def look_around(context=None):
    """
    Scans the screen for items, entities, and other meaningful objects using vision.

    Args:
        context (dict): Context-aware arguments such as player position and facing direction.

    Returns:
        bool: True if anything meaningful is detected; False otherwise.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        screen = pyautogui.screenshot()
    except Exception as e:
        logging.error(f"Error capturing screen: {e}")
        return False

    try:
        detection_result = analyze_frame(np.array(screen))
    except Exception as e:
        logging.error(f"Error analyzing frame: {e}")
        return False

    if detection_result:
        logging.info("Meaningful object detected!")
        return True
    else:
        logging.info("Nothing meaningful detected.")
        return False

def gather_info(context=None):
    """
    Scans the current screen for meaningful information and returns True if detected.

    Args:
        context (dict, optional): Optional context-aware arguments. Defaults to None.

    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        image = pyautogui.screenshot()
        detection = analyze_frame(np.array(image))

        if detection is not None:
            logging.info(f"Detected: {detection}")
            return True

    except Exception as e:
        logging.error(f"Error scanning screen: {str(e)}")

    logging.info("Nothing detected.")
    return False

    Returns:
        bool: True if wood-like entities or blocks were detected and interacted with; False otherwise.
    """
    logging.basicConfig(level=logging.INFO)

    try:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
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

def gather_wood():
    """
    Fixes the skill: gather_wood by scanning the screen for wood blocks.
    
    Returns:
        bool: True if wood blocks are detected, False otherwise.
    """
    
    # Set up logging to print messages in the console
    logging.basicConfig(level=logging.INFO)
    
    # Take a screenshot of the current window
    screenshot = pyautogui.screenshot()
    
    try:
        # Analyze the screenshot using blockmind vision
        result = analyze_frame(screenshot)
        
        # Log any detected items, entities, or blocks
        if 'entities' in result and len(result['entities']) > 0:
            logging.info("Detected entities: {}".format(result['entities']))
        elif 'items' in result and len(result['items']) > 0:
            logging.info("Detected items: {}".format(result['items']))
        elif 'blocks' in result and 'wood' in result['blocks']:
            logging.info("Detected wood blocks!")
            
            # If wood blocks are detected, return True
            return True
    
    except Exception as e:
        # Log any exceptions that occur during analysis
        logging.error("Error analyzing frame: {}".format(str(e)))
    
    # If no meaningful items or entities are detected, return False
    return False


import pyautogui
from blockmind_vision import analyze_frame
import logging

def craft_planks(item_name='plank'):
    try:
        # Take a screenshot of the crafting area
        screen = pyautogui.screenshot(region=(0, 100, 800, 200))

        # Analyze the frame to detect items and entities in the crafting area
        detection_result = analyze_frame(screen)

        # Check if the item we are looking for is detected
        if 'items' in detection_result and any(item['name'].lower() == item_name.lower() for item in detection_result['items']):
            logging.info(f"Detected {item_name} in crafting area")
            return True

    except Exception as e:
        logging.error(f"Error while scanning crafting area: {str(e)}")

    # If nothing meaningful is detected, return False
    logging.info("Nothing meaningful detected in crafting area")
    return False


import pyautogui
from blockmind_vision import analyze_frame
import logging

def place_walls(width, height, delay=0.5):
    """
    Places walls in Minecraft using the current vision system.

    Args:
        width (int): The width of the screenshot.
        height (int): The height of the screenshot.
        delay (float, optional): The delay between screenshots. Defaults to 0.5.

    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """

    logging.info("Starting wall placement process...")
    
    # Capture the screen
    try:
        screenshot = pyautogui.screenshot(region=(100, 100, width, height))
    except Exception as e:
        logging.error(f"Failed to capture screenshot: {str(e)}")
        return False

    # Analyze the frame
    result = analyze_frame(screenshot)
    
    if result:
        logging.info("Meaningful content detected. Placing walls...")
        # Simulate mouse clicks to place walls (assuming default Minecraft controls)
        for _ in range(4):
            pyautogui.click()
        
        return True
    
    logging.info("No meaningful content detected.")
    
    return False


import pyautogui
import logging
from blockmind_vision import analyze_frame

def place_roof():
    """
    Perform the Minecraft task: place roof.
    
    This function captures a screenshot, uses BlockMind vision to analyze it,
    and returns True if anything meaningful is detected. If no items or entities are found,
    it returns False.

    Returns:
        bool: Whether something meaningful was detected.
    """

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Capture the screen
        screenshot = pyautogui.screenshot()

        # Analyze the frame using BlockMind vision
        result = analyze_frame(screenshot)

        if result['detected']:
            return True  # Meaningful thing detected

        # If nothing was detected, log a message and return False
        logging.info("Nothing meaningful found.")

    except Exception as e:
        # Log any exceptions that occur during execution
        logging.error(f"Error placing roof: {str(e)}")
        raise

    return False  # Default to returning False if no error occurred but nothing was detected


# Example usage:
if __name__ == "__main__":
    result = place_roof()
    print("Meaningful thing detected:", result)


import pyautogui
from blockmind_vision import analyze_frame
import logging

def gather_wood(width=1920, height=1080):
    try:
        # Take a screenshot of the game window
        screenshot = pyautogui.screenshot(region=(0, 100, width, height - 100))
        
        # Analyze the screenshot to detect wood logs or other items
        result = analyze_frame(screenshot)
        
        # Check if any items or entities are detected
        if 'wood' in str(result) or 'tree' in str(result):
            logging.info("Detected wood logs or a tree. Gathering wood...")
            return True
        else:
            logging.info("No wood logs or trees detected. Cannot gather wood.")
            return False
    
    except Exception as e:
        logging.error(f"Error gathering wood: {str(e)}")
        return False

# Usage example
gather_wood()


import pyautogui
from blockmind_vision import analyze_frame
import cv2
import numpy as np
import logging

def craft_planks():
    """
    Perform the Minecraft task: craft plank crafting table.
    
    This function captures a screenshot, analyzes the frame for items/entities,
    and logs whether any meaningful data was found. It returns True if anything
    is detected and False otherwise.

    Returns:
        bool: Whether anything meaningful was detected in the screenshot.
    """

    try:
        # Capture a full-screen screenshot
        image = pyautogui.screenshot()
        
        # Convert the screenshot to an OpenCV image
        frame = np.array(image)
        
        # Resize the frame for faster processing (optional but recommended)
        frame = cv2.resize(frame, (800, 600))
        
        # Analyze the frame using blockmind_vision's analyze_frame function
        entities = analyze_frame(frame)
        
        # If any items/entities were detected, log a success message and return True
        if entities:
            logging.info("Detected planks or crafting table")
            return True
        
        # If nothing was found, log an error message and return False
        else:
            logging.error("Failed to detect planks or crafting table")
            return False
    
    except Exception as e:
        # Log any exceptions that occur during the process
        logging.error(f"An error occurred: {e}")
        return False

# Example usage
if __name__ == "__main__":
    result = craft_planks()
    print(result)
pip install pyautogui blockmind_vision opencv-python numpy


import pyautogui
from blockmind_vision import analyze_frame
import logging

def place_walls():
    """
    Perform the Minecraft task: place walls.
    
    This function takes a screenshot, analyzes it using BlockMind vision,
    and logs the result. If anything meaningful is detected, it returns True;
    otherwise, it returns False.
    """

    # Take a screenshot of the current window
    screen = pyautogui.screenshot()

    # Analyze the frame for any meaningful content (e.g., items, entities)
    analysis_result = analyze_frame(screen)

    # Log the result
    if analysis_result:
        logging.info(f"Meaningful content detected: {analysis_result}")
        return True

    # If no meaningful content is found, log a message and return False
    else:
        logging.info("No meaningful content detected.")
        return False


import pyautogui
from blockmind_vision import analyze_frame
import logging

def place_roof():
    # Log the start of the function
    logging.info("Starting roof placement")

    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Analyze the frame for entities or items that indicate the need to place a roof
    result = analyze_frame(screenshot)
    
    if result:
        # If anything meaningful is detected, return True and log a message
        logging.info("Detected something on the screen")
        return True
    
    else:
        # If nothing meaningful is detected, return False and log a message
        logging.info("Found empty space")
        return False

# Set up logging to print messages
logging.basicConfig(level=logging.INFO)


import pyautogui
from blockmind_vision import analyze_frame
import logging

def look_around(screen=None, resolution=(1920, 1080)):
    """
    Perform the Minecraft task: look around.

    Args:
        screen (numpy array): The screenshot to be analyzed. If None, a new screenshot will be captured.
        resolution (tuple): The resolution of the game window.

    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """

    # Log the start of the function
    logging.info("Looking around...")

    # If no screen is provided, capture a new screenshot
    if screen is None:
        try:
            screen = pyautogui.screenshot()
        except Exception as e:
            logging.error(f"Failed to capture screenshot: {e}")
            return False

    # Analyze the frame
    result = analyze_frame(screen)

    # Log the analysis result
    logging.info("Analysis result:")
    print(result)

    # Check if anything meaningful is detected
    if result.get('entities') or result.get('items'):
        # If something meaningful is detected, return True
        logging.info("Meaningful thing found!")
        return True

    # If nothing meaningful is detected, return False
    logging.info("Nothing interesting found.")
    return False


import pyautogui
import logging
from blockmind_vision import analyze_frame
import cv2

def gather_info(window_name="Minecraft"):
    """
    Capture the Minecraft window, analyze it for items or entities and return True if found, False otherwise.
    
    Args:
        window_name (str): The name of the Minecraft window. Default is "Minecraft".

    Returns:
        bool: Whether any meaningful information was detected in the Minecraft window.
    """

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Capture a screenshot of the Minecraft window
        screen = pyautogui.screenshot(region=(0, 0, 1920, 1080))  # Assuming a 1920x1080 resolution

        # Convert the screenshot to OpenCV format
        frame = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2BGR)

        # Analyze the frame for items or entities using blockmind_vision
        result = analyze_frame(frame)

        # Log whether any meaningful information was detected
        logging.info(f"Detected: {result}")

        # Return True if anything meaningful was detected, False otherwise
        return bool(result)

    except Exception as e:
        # Log any exceptions that occur during the process
        logging.error(f"An error occurred: {e}")
        return False

import numpy
