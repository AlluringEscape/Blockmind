import cv2
import numpy as np
import threading
import time
import win32gui
import win32con
import win32api
from PIL import ImageGrab

# Constants
WINDOW_NAME = "Blockmind Overlay"
REFRESH_DELAY = 0.03  # ~30 FPS

def draw_overlay():
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Grab screen region (you can adjust for just the Minecraft window)
        screen = np.array(ImageGrab.grab())
        frame = screen.copy()

        height, width, _ = frame.shape

        # Example: draw a bounding box where the bot "sees" a tree
        cv2.rectangle(frame, (1275, 691), (1285, 701), (0, 255, 0), 2)
        cv2.putText(frame, "Crosshair", (1275, 685), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        # OPTIONAL: Draw detection summary from memory or file
        # Example:
        # detections = load_last_detections()
        # for d in detections:
        #     x1, y1, x2, y2 = d['bbox']
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
        #     cv2.putText(frame, d['label'], (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

        # Resize if needed for display
        overlay = cv2.resize(frame, (width//2, height//2))
        cv2.imshow(WINDOW_NAME, overlay)

        if cv2.waitKey(1) == 27:  # Press ESC to quit
            break

    cv2.destroyAllWindows()

def run_overlay_thread():
    thread = threading.Thread(target=draw_overlay)
    thread.daemon = True
    thread.start()

