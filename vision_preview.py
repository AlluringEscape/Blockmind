import cv2
import numpy as np
from PIL import ImageGrab
import win32gui

TARGET_WINDOW = "Minecraft"

def get_minecraft_window_bbox():
    def enum_windows_callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if TARGET_WINDOW.lower() in title.lower():
                rect = win32gui.GetWindowRect(hwnd)
                result.append(rect)

    result = []
    win32gui.EnumWindows(enum_windows_callback, result)
    return result[0] if result else None

def main():
    print("🔍 Looking for Minecraft window...")
    bbox = get_minecraft_window_bbox()

    if not bbox:
        print("❌ Minecraft window not found.")
        return

    print("🎯 Capturing window area:", bbox)

    while True:
        frame = np.array(ImageGrab.grab(bbox=bbox))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        resized = cv2.resize(frame, (1280, 720))
        cv2.imshow("🎮 Minecraft Vision Preview", resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
