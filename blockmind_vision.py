import cv2
import numpy as np
from blockmind_window_capture import capture_game_window

def analyze_frame():
    # Capture the current game window as a frame
    frame = capture_game_window()

    if frame is None:
        print("❌ No game window captured.")
        return None

    # === Debug View ===
    cv2.imshow("🧠 Blockmind Vision Debug", frame)
    cv2.waitKey(1)

    # === Placeholder for processing logic ===
    # This is where your detection logic (blocks, entities, HUD, etc.) would go
    print("👁️ Frame captured and displayed.")

    return frame
