import cv2
import numpy as np

def detect_objects(frame):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Detect trees (green)
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Detect stone (gray)
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([179, 50, 200])
    gray_mask = cv2.inRange(hsv, lower_gray, upper_gray)
    
    # Find contours
    detections = []
    
    # Detect trees
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        detections.append({
            "label": "tree",
            "box": [x, y, x+w, y+h],
            "confidence": 0.9
        })
    
    # Detect stone
    contours, _ = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        detections.append({
            "label": "stone",
            "box": [x, y, x+w, y+h],
            "confidence": 0.8
        })
    
    return {
        "detections": detections,
        "frame_size": frame.shape[:2]
    }