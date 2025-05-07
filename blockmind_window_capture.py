import dxcam
import cv2
import pygetwindow as gw
import time

camera = dxcam.create(output_color="BGR")
camera_started = False

def get_minecraft_window_region():
    for window in gw.getWindowsWithTitle("Minecraft"):
        if "minecraft" in window.title.lower() and window.visible:
            left, top = window.left, window.top
            right, bottom = left + window.width, top + window.height
            return (left, top, right, bottom)
    return None

def capture_game_window():
    global camera_started
    region = get_minecraft_window_region()
    if not region:
        print("❌ Minecraft window not found.")
        return None

    camera.region = region
    if not camera_started:
        camera.start(target_fps=30)
        time.sleep(0.1)  # allow first frame to buffer
        camera_started = True

    frame = camera.get_latest_frame()
    if frame is None:
        print("⚠️ No frame available.")
    return frame

def stop_camera():
    global camera_started
    if camera_started:
        camera.stop()
        camera_started = False

if __name__ == "__main__":
    try:
        print("📷 Starting preview...")
        while True:
            frame = capture_game_window()
            if frame is not None:
                cv2.imshow("Game Preview", frame)
            if cv2.waitKey(1) == 27:  # ESC to quit
                break
    finally:
        stop_camera()
        cv2.destroyAllWindows()
