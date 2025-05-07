
import time
import pyautogui
from PIL import ImageGrab
from collections import defaultdict

# Memory store
memory = defaultdict(str)

def get_center_pixel(screen):
    width, height = screen.size
    return screen.getpixel((width // 2, height // 2))

def classify_pixel(rgb):
    r, g, b = rgb
    if 80 < r < 140 and 40 < g < 100 and 20 < b < 70:
        return "Possible Wood"
    if 50 < r < 100 and 120 < g < 160 and 50 < b < 100:
        return "Grass"
    return "Unknown"

def act_on_classification(label):
    if label == "Possible Wood":
        print("👊 Detected wood-like pixel. Punching...")
        pyautogui.mouseDown()
        time.sleep(0.8)
        pyautogui.mouseUp()
    elif label == "Grass":
        print("🌱 Detected grass. Walking forward.")
        pyautogui.keyDown("w")
        time.sleep(1)
        pyautogui.keyUp("w")
    else:
        print("❓ No known block. Turning slightly.")
        pyautogui.moveRel(20, 0)  # small right turn

def loop():
    print("🧠 Blockmind PixelBot initialized. Watching center pixel...")
    while True:
        screenshot = ImageGrab.grab()
        pixel = get_center_pixel(screenshot)
        label = classify_pixel(pixel)
        print(f"🎯 Center pixel RGB: {pixel} → Classified as: {label}")
        if memory[pixel] == "":
            memory[pixel] = label
        act_on_classification(label)
        time.sleep(2)

if __name__ == "__main__":
    loop()
