# Simplified stub version
latest_frame = None

def analyze_frame(frame):
    global latest_frame
    latest_frame = frame.copy()
    # Your vision detection code here
    return {"blocks": [], "entities": [], "items": [], "player": {"food": "unknown", "health": "unknown"}, "summary": {"tree": False, "cave": False, "animal": False, "flower": False, "sky": True}}

def get_latest_detection_image():
    return latest_frame
