import mss
import numpy as np
import win32gui
import win32con
import threading
import cv2
import os

class ThreadSafeCapturer:
    def __init__(self):
        self.local = threading.local()
        self.monitor = None
        self.lock = threading.Lock()
        self.debug_mode = True
        
    def _get_mss_instance(self):
        if not hasattr(self.local, "mss"):
            self.local.mss = mss.mss()
        return self.local.mss
        
    def _update_monitor(self):
        # Find any window containing "Minecraft" in title
        def callback(hwnd, hwnds):
            if 'Minecraft' in win32gui.GetWindowText(hwnd):
                hwnds.append(hwnd)
            return True
        
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        
        if hwnds:
            hwnd = hwnds[0]
            rect = win32gui.GetWindowRect(hwnd)
            with self.lock:
                self.monitor = {
                    "left": max(0, rect[0]),
                    "top": max(0, rect[1]),
                    "width": max(0, rect[2] - rect[0]),
                    "height": max(0, rect[3] - rect[1])
                }
            if self.debug_mode:
                print(f"🔍 Window found: {win32gui.GetWindowText(hwnd)}")
                print(f"📐 Monitor region: {self.monitor}")
        else:
            print("❌ No Minecraft window found with 'Minecraft' in title!")
    
    def capture_frame(self):
        self._update_monitor()  # Force update every frame
        
        if not self.monitor or self.monitor["width"] <= 0 or self.monitor["height"] <= 0:
            print("⚠️ Invalid capture region, check window visibility!")
            return None
            
        try:
            sct = self._get_mss_instance()
            frame = np.array(sct.grab(self.monitor))
            
            if self.debug_mode:
                output_path = os.path.abspath("last_capture.png")
                cv2.imwrite(output_path, frame)
                print(f"📸 Saved debug capture to: {output_path}")
                print(f"📏 Frame dimensions: {frame.shape}")
                
            return frame
        except Exception as e:
            print(f"🚨 Capture failed: {str(e)}")
            return None