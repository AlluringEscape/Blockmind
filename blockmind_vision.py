
import cv2
import numpy as np
from blockmind_window_capture import capture_game_window

def analyze_frame(frame=None):
    # Use provided frame or capture a new one
    if frame is None:
        frame = capture_game_window()

    if frame is None:
        print("❌ No game window captured.")
        return {}

    print("👁️ Frame captured and processed.")

    # Detect center pixel (crosshair RGB)
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    crosshair_rgb = frame[center_y, center_x].tolist()

    return {
        "detections": [],
        "crosshair_rgb": crosshair_rgb
    }
