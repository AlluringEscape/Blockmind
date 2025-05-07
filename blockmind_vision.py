import cv2
import numpy as np

def process_frame(frame):
    if frame is None:
        return {"detections": [], "debug_frame": None}

    # Convert RGBA to BGR and handle alpha channel
    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    
    # Resize for faster processing (maintain aspect ratio)
    height, width = frame.shape[:2]
    processed = cv2.resize(frame, (1280, int(1280 * height/width)))
    
    # Enhanced tree detection parameters for your resolution
    hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
    lower_green = np.array([25, 60, 30], dtype=np.uint8)
    upper_green = np.array([95, 255, 220], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Visual debugging
    debug_frame = processed.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x,y,w,h = cv2.boundingRect(cnt)
            detections.append({
                "label": "tree",
                "box": [x,y,x+w,y+h],
                "confidence": cv2.contourArea(cnt)/10000
            })
            cv2.rectangle(debug_frame, (x,y), (x+w,y+h), (0,255,0), 2)
    
    return {
        "detections": detections,
        "debug_frame": debug_frame
    }