import cv2
import numpy as np

OBJECT_RANGES = {
    "tree": {
        "lower": np.array([25, 80, 40]),
        "upper": np.array([95, 255, 200]),
        "color": (0, 255, 0)
    }
}

def process_frame(frame):
    debug_frame = None
    detections = []
    
    try:
        if frame is None or frame.size == 0:
            return {"detections": [], "debug_frame": np.zeros((480, 640, 3), dtype=np.uint8)}
        
        # Convert RGBA to BGR if needed
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        debug_frame = frame.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        for obj_name, params in OBJECT_RANGES.items():
            mask = cv2.inRange(hsv, params["lower"], params["upper"])
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                if cv2.contourArea(cnt) > 300:
                    x, y, w, h = cv2.boundingRect(cnt)
                    detections.append({
                        "label": obj_name,
                        "box": [x, y, x+w, y+h],
                        "confidence": cv2.contourArea(cnt)/10000
                    })
                    cv2.rectangle(debug_frame, (x,y), (x+w,y+h), params["color"], 2)
        
        return {
            "detections": detections,
            "debug_frame": debug_frame
        }
    
    except Exception as e:
        print(f"Vision error: {str(e)}")
        return {"detections": [], "debug_frame": np.zeros((480, 640, 3), dtype=np.uint8)}