def explore(world, x_range, y_range, z_range):
    import pyautogui
    import cv2
    import numpy as np
    import time
    from blockmind_vision import analyze_frame

    print("🔍 Starting intelligent exploration...")
    found_something = False
    scanned_tiles = 0

    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            for z in range(z_range[0], z_range[1]):
                print(f"📍 Exploring ({x}, {y}, {z})")
                screenshot = pyautogui.screenshot()
                img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                vision = analyze_frame(img)
                scanned_tiles += 1

                if vision and (vision.get("entities") or vision.get("items") or vision.get("biome")):
                    print("✅ Detected during exploration:", vision)
                    found_something = True

                time.sleep(0.05)

    print(f"🧭 Finished scanning {scanned_tiles} tiles. Found something? {found_something}")
    return found_something


import pyautogui
from blockmind_vision import analyze_frame
import logging
import time

def look_around(width=800, height=600, delay=0.5):
    """
    Perform the Minecraft task: look around.

    Args:
        width (int): The width of the game window.
        height (int): The height of the game window.
        delay (float): The delay between frames.

    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """

    try:
        logging.info("Looking around...")
        # Take a screenshot
        screen = pyautogui.screenshot(region=(0, 0, width, height))
        
        # Analyze the frame
        result = analyze_frame(screen)
        
        # Log the result
        logging.info(result)
        
        # Return True if anything meaningful is detected
        return any(item in str(result).lower() for item in ["diamond", "gold", "iron", "entity", "item"])
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False

# Example usage:
if __name__ == "__main__":
    while True:
        if look_around():
            print("Detected something meaningful!")
        else:
            print("Nothing meaningful detected.")
        
        # Sleep for 1 second
        time.sleep(1)


import pyautogui
from blockmind_vision import analyze_frame
import cv2
import numpy as np

def gather_info(width=1920, height=1080, threshold=0.5):
    """
    Performs the Minecraft task: gather info.

    Args:
        width (int): The screen width in pixels.
        height (int): The screen height in pixels.
        threshold (float): The minimum confidence threshold for object detection.

    Returns:
        bool: True if anything meaningful is detected, False otherwise.
    """
    
    # Ensure the display is updated to prevent errors
    pyautogui.sleep(1)
    
    try:
        # Take a screenshot of the entire screen
        image = pyautogui.screenshot(region=(0, 0, width, height))
        
        # Convert the image to OpenCV format
        frame = np.array(image)
        
        # Analyze the frame for entities or items
        detected_objects = analyze_frame(frame)
        
        # Check if any objects were detected with a confidence above the threshold
        for obj in detected_objects:
            if obj.confidence >= threshold:
                print(f"Detected object: {obj.label} at ({obj.x}, {obj.y})")
                
                # Return True to indicate that something was found
                return True
        
        # If no objects were found, print a message and return False
        print("No meaningful information detected.")
        
    except Exception as e:
        # Log any exceptions that occur during the process
        print(f"An error occurred: {str(e)}")
    
    # Return False to indicate that nothing was found
    return False

# Example usage
if __name__ == "__main__":
    gather_info()
