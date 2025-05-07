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
