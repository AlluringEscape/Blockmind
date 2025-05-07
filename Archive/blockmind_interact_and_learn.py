import cv2
import time
from blockmind_memory import remember_object

def capture_and_remember():
    print("📸 Capturing block under crosshair...")
    screenshot = cv2.imread("vision_logs/last_seen.png")  # Change this to real-time capture if needed

    if screenshot is None:
        print("❌ Failed to capture or locate image.")
        return

    name = remember_object(screenshot)
    print(f"📘 Updated object name to: {name}")

if __name__ == "__main__":
    capture_and_remember()