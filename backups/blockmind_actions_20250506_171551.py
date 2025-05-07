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
        # Take screenshot and convert to NumPy array
        screen = pyautogui.screenshot()
        frame = np.array(screen)
    except Exception as e:
        logging.error(f"Error capturing screen: {e}")
        return False

    try:
        detection_result = blockmind_vision.analyze_frame(frame)
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
        # Take screenshot and convert to NumPy array
        image = pyautogui.screenshot()
        frame = np.array(image)

        detection = blockmind_vision.analyze_frame(frame)
        if detection is not None:
            logging.info(f"Detected: {detection}")
            return True

    except Exception as e:
        logging.error(f"Error scanning screen: {str(e)}")

    logging.info("Nothing detected.")
    return False
