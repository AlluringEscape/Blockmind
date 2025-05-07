import mss
import numpy as np
import pygetwindow as gw

def capture_game_window_image():
    try:
        windows = gw.getWindowsWithTitle("Minecraft")
        if not windows:
            print("❌ Minecraft window not found.")
            return None

        win = windows[0]

        # Define bounding box for mss
        bbox = {
            "top": win.top,
            "left": win.left,
            "width": win.width,
            "height": win.height
        }

        with mss.mss() as sct:
            sct_img = sct.grab(bbox)
            img = np.array(sct_img)[:, :, :3]  # Drop alpha channel
            return img
    except Exception as e:
        print(f"❌ Window capture error: {e}")
        return None
