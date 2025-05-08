import time
import threading
import cv2
import numpy as np
from blockmind_window_capture import ThreadSafeCapturer
from blockmind_vision import process_frame

class VisionCore:
    def __init__(self):
        self.capturer = ThreadSafeCapturer()
        self.running = True
        self.current_frame = None
        
    def capture_loop(self):
        while self.running:
            frame = self.capturer.capture_frame()
            if frame is not None:
                self.current_frame = process_frame(frame)
            time.sleep(1/60)

def main():
    core = VisionCore()
    capture_thread = threading.Thread(target=core.capture_loop)
    capture_thread.start()
    
    # Initialize window first
    cv2.namedWindow("Debug View", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Debug View", 1280, 720)
    cv2.moveWindow("Debug View", 100, 100)
    
    try:
        while True:
            debug_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            
            if core.current_frame and core.current_frame["debug_frame"] is not None:
                debug_frame = cv2.resize(core.current_frame["debug_frame"], (1280, 720))
            
            cv2.imshow("Debug View", debug_frame)
            
            # Exit on Q press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    finally:
        core.running = False
        capture_thread.join()
        cv2.destroyAllWindows()
        print("🛑 System shutdown")

if __name__ == "__main__":
    main()