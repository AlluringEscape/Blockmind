import cv2
import time
from blockmind_window_capture import capture_game_window, stop_camera

def main():
    cv2.namedWindow("Game Preview", cv2.WINDOW_NORMAL)
    frame_count = 0
    start_time = time.time()

    while True:
        frame = capture_game_window()
        if frame is not None:
            cv2.imshow("Game Preview", frame)
            frame_count += 1

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time if elapsed_time > 0 else 0
    print(f"Screen Capture FPS: {int(fps)}")

    stop_camera()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
