# list_all_windows.py
import win32gui

def enum_windows():
    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if title:
            print(f"{hex(hwnd)} → {title}")
    win32gui.EnumWindows(callback, None)

enum_windows()
