
# blockmind_launcher.py
import time
import cv2
from blockmind_window_capture import capture_game_window
from blockmind_vision import analyze_frame

def draw_detections(frame, detections):
    for det in detections:
        label = det.get("label", "Unknown")
        x, y, w, h = det.get("box", (0, 0, 0, 0))
        color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame

def main():
    print("🧠 Blockmind Vision Debug Mode (Press 'q' to quit')")
    while True:
        try:
            frame = capture_game_window()
            result = analyze_frame(frame)

            detections = result.get("detections", [])
            crosshair_rgb = result.get("crosshair_rgb", None)

            frame = draw_detections(frame, detections)

            if crosshair_rgb:
                cv2.putText(frame, f"Crosshair RGB: {crosshair_rgb}", (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Blockmind Sees", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            time.sleep(0.1)  # Throttle loop

        except Exception as e:
            print(f"❌ Error: {e}")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
