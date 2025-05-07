import json
import random
import os
from survival_data import load_survival_guide

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
import pyautogui
import blockmind_vision
import logging


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
        detection_result = blockmind_vision.analyze_frame(screen)
    except Exception as e:
        logging.error(f"Error analyzing frame: {e}")
        return False

    if detection_result:
        logging.info("Meaningful object detected!")
        return True
    else:
        logging.info("Nothing meaningful detected.")
        return False


    Args:
        context (dict, optional): Optional context-aware arguments. Defaults to None.

    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        image = pyautogui.screenshot()
        detection = blockmind_vision.analyze_frame(image)

        if detection is not None:
            logging.info(f"Detected: {detection}")
            return True

    except Exception as e:
        logging.error(f"Error scanning screen: {str(e)}")

    logging.info("Nothing detected.")
    return False


import pyautogui
from blockmind_vision import analyze_frame
import logging
import time

    Args:
        context (dict): The current game state.
        player_position (tuple): The position of the player.
        vision_range (int): The range to scan around the player. Defaults to 5.

    Returns:
        bool: Whether anything meaningful was detected.
    """

    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Take a screenshot of the area around the player
        screenshot = pyautogui.screenshot(region=(player_position[0] - vision_range, 
                                                  player_position[1] - vision_range, 
                                                  vision_range * 2, 
                                                  vision_range * 2))

        # Analyze the screenshot for meaningful objects or entities
        analysis_result = analyze_frame(screenshot)

        # Check if anything meaningful was detected
        if analysis_result:
            logger.info("Detected something meaningful!")
            return True

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    # If no meaningful objects were found, return False
    return False


import pyautogui
import blockmind_vision
import logging

    Args:
        context (dict): Context-aware arguments if needed
    
    Returns:
        bool: True if anything meaningful is detected, False otherwise
    """

    # Initialize logger
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    try:
        # Take a screenshot using pyautogui
        screen = pyautogui.screenshot()

        # Analyze the frame for any items or entities
        result = blockmind_vision.analyze_frame(screen)

        # Check if anything meaningful is detected
        if result:
            log.info(f"Detected: {result}")
            return True

    except Exception as e:
        # Log any exceptions that occur during the process
        log.error(f"Error gathering info: {e}")

    # Return False if nothing meaningful is detected
    return False


import pyautogui
from blockmind_vision import analyze_frame
import logging

def look_around(context=None):
    """
    Function to scan the player's surroundings for meaningful objects.
    
    Args:
        context (dict, optional): Context-aware arguments if needed. Defaults to None.

    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """

    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Take a screenshot of the player's surroundings
        screen_shot = pyautogui.screenshot(region=(0, 0, 1920, 1080))

        # Analyze the frame for meaningful objects
        result = analyze_frame(screen_shot)

        # Log the result
        logging.info(result)

        # Check if anything meaningful was detected
        if any(item in result['objects'] for item in context.get('items_of_interest', [])):
            return True

        # If no meaningful items were found, check for entities
        if any(entity in result['entities'] for entity in context.get('entities_of_interest', [])):
            return True

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    # If no meaningful objects or entities were detected, return False
    return False


import pyautogui
from blockmind_vision import analyze_frame
import cv2
import numpy as np

def gather_info(context=None):
    """
    Gather information from the Minecraft screen.
    
    Args:
        context (dict, optional): Context-aware arguments for the bot. Defaults to None.
        
    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """

    # Check if vision module is enabled
    if not blockmind_vision.enabled:
        print("Vision module not enabled.")
        return False

    # Take a screenshot of the Minecraft screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to OpenCV image
    frame = np.array(screenshot)

    # Analyze the frame using BlockMind Vision
    detection_result = analyze_frame(frame)

    # Check if any entity is detected
    for detection in detection_result:
        # Print the detection result
        print(f"Detected: {detection['label']} at ({detection['x']}, {detection['y']})")

        # If an item or entity is detected, return True
        if 'item' in detection['label'].lower() or 'entity' in detection['label'].lower():
            return True

    # If no meaningful information is detected, return False
    print("No meaningful information detected.")
    return False
