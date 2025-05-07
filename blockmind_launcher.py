import time
import threading
import cv2
from blockmind_window_capture import ThreadSafeCapturer
from blockmind_vision import process_frame

class VisionCore:
    def __init__(self):
        self.capturer = ThreadSafeCapturer()
        self.running = True
        self.current_frame = None
        
    def capture_loop(self):
        print("🔄 Capture loop started")
        while self.running:
            start = time.perf_counter()
            frame = self.capturer.capture_frame()
            
            if frame is not None:
                print(f"🎮 New frame captured: {frame.shape}")
                self.current_frame = process_frame(frame)
                
            sleep_time = max(1/60 - (time.perf_counter() - start), 0)
            time.sleep(sleep_time)

def main():
    core = VisionCore()
    capture_thread = threading.Thread(target=core.capture_loop)
    capture_thread.start()
    
    try:
        print("""
        🔧 Debug Checklist:
        1. Minecraft window visible and not minimized
        2. Game in 3rd person view (F5 twice)
        3. FOV set to Normal (Options > Video Settings)
        4. Standing near trees/stone
        """)
        
        while True:
            if core.current_frame:
                # Corrected print statement
                print(f"🌳 Detected: {len(core.current_frame['detections'])} objects")
        
                if core.current_frame['debug_frame'] is not None:
                    cv2.imshow('Debug View', core.current_frame['debug_frame'])
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        pass
    finally:
        core.running = False
        capture_thread.join()
        cv2.destroyAllWindows()
        print("🛑 System shutdown")

if __name__ == "__main__":
    main()