
import time
from PIL import ImageGrab
from blockmind_memory import has_seen, remember_new_block, update_block_name
from blockmind_vision import get_image_hash, save_full_screenshot

def capture_and_identify():
    print("📸 Capturing full screen...")
    screenshot = ImageGrab.grab()
    save_full_screenshot(screenshot)
    image_hash = get_image_hash(screenshot)
    known = has_seen(image_hash)

    if known:
        print(f"👁️ I recognize this block! It's {known}")
    else:
        new_obj = remember_new_block(screenshot)
        print(f"👁️ This is new. Calling it: {new_obj}")
        time.sleep(1)
        update_block_name(new_obj, "Unknown Block")
        print(f"📘 Updated {new_obj}'s name to: Unknown Block")

if __name__ == "__main__":
    while True:
        capture_and_identify()
        time.sleep(5)  # Wait 5 seconds between each capture
