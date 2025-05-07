
from blockmind_window_capture import grab_game_window
import time

def main():
    print("🤖 Blockmind booted up.")
    time.sleep(1)
    print("👁️ Capturing view...")
    screenshot = grab_game_window()
    screenshot.save("last_vision.png")
    print("✅ Screenshot saved as last_vision.png")

if __name__ == "__main__":
    main()
