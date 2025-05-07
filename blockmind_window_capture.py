import pyautogui
import cv2
import numpy as np
import win32gui
import win32con

def find_minecraft_window():
    def callback(hwnd, hwnds):
        if 'Minecraft' in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
        return True
    
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def capture_game_window():
    hwnd = find_minecraft_window()
    if not hwnd:
        print("⚠️ Minecraft window not found!")
        return None, None
    
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    
    rect = win32gui.GetWindowRect(hwnd)
    region = (rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])
    screenshot = pyautogui.screenshot(region=region)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return frame, region