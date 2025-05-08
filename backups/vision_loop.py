
import time
import pyautogui
from blockmind_vision import analyze_frame

def run_vision_loop():
    while True:
        frame = pyautogui.screenshot()
        scene = analyze_frame(frame)
        print("Entities:", [e["label"] for e in scene["entities"]])
        print("Blocks:", [b["label"] for b in scene["blocks"]])
        print("Items:", [i["label"] for i in scene["items"]])
        time.sleep(0.5)  # ~2 FPS (adjustable)

if __name__ == "__main__":
    run_vision_loop()
