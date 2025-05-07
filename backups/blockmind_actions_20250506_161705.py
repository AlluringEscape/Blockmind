def explore(world, x_range, y_range, z_range):
    import pyautogui
    import cv2
    import numpy as np
    import time
    from blockmind_vision import analyze_frame

    print("🔍 Starting intelligent exploration...")
    found_something = False
    scanned_tiles = 0

    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            for z in range(z_range[0], z_range[1]):
                print(f"📍 Exploring ({x}, {y}, {z})")
                screenshot = pyautogui.screenshot()
                img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                vision = analyze_frame(img)
                scanned_tiles += 1

                if vision and (vision.get("entities") or vision.get("items") or vision.get("biome")):
                    print("✅ Detected during exploration:", vision)
                    found_something = True

                time.sleep(0.05)

    print(f"🧭 Finished scanning {scanned_tiles} tiles. Found something? {found_something}")
    return found_something
