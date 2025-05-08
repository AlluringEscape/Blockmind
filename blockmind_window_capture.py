import mss
import numpy as np
import win32gui
import win32con
import threading
import cv2
import os
import pygetwindow as gw
import pyautogui


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
    
    def capture_frame(self):
        self._update_monitor()
        
        if not self.monitor or self.monitor["width"] <= 0:
            return None
            
        try:
            sct = self._get_mss_instance()
            frame = np.array(sct.grab(self.monitor))
            
            # Convert BGRA to BGR
            if frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Fixed conversion
                
            if self.debug_mode:
                debug_frame = frame.copy()
                cv2.imwrite("last_capture_corrected.png", debug_frame)
                print("📸 Saved color-corrected screenshot")
                
            return frame
        except Exception as e:
            print(f"Capture error: {str(e)}")
            return None

def capture_game_window():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Or a specific window region
        sct_img = sct.grab(monitor)
        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame, monitor
