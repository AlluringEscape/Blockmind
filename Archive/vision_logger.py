
import pyautogui
import time
import os

# Configuration
CAPTURE_COUNT = 10
CAPTURE_DELAY = 1  # seconds
SAVE_DIR = "vision_logs"

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

print(f"📁 Saving screenshots to: {SAVE_DIR}")

for i in range(CAPTURE_COUNT):
    try:
        print(f"📸 Capturing screenshot #{i + 1}...")
        screenshot = pyautogui.screenshot()
        filename = os.path.join(SAVE_DIR, f"vision_debug_{i + 1:02d}.png")
        screenshot.save(filename)
        print(f"✅ Saved to: {filename}")
        time.sleep(CAPTURE_DELAY)
    except Exception as e:
        print(f"❌ Error on capture #{i + 1}: {e}")

print("✅ Done capturing 10 screenshots.")
