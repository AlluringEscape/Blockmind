import pygetwindow as gw
import pyautogui
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

selected_coords = None

def capture_window_screenshot(window):
    # Bring to front and take a screenshot
    window.activate()
    coords = (window.left, window.top, window.right, window.bottom)
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))

    # Save it to logs folder
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"logs/window_preview_{timestamp}.png"
    screenshot.save(screenshot_path)

    return coords, screenshot_path

def set_game_window():
    global selected_coords

    windows = [w for w in gw.getAllWindows() if w.title and w.width > 100 and w.height > 100]

    if not windows:
        messagebox.showerror("Error", "No suitable windows found.")
        return None

    # Build selection GUI
    root = tk.Tk()
    root.title("Select Game Window")
    root.geometry("500x400")

    label = tk.Label(root, text="Select a window:")
    label.pack(pady=5)

    listbox = tk.Listbox(root, height=15, width=60)
    listbox.pack()

    for w in windows:
        listbox.insert(tk.END, w.title)

    def confirm_selection():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No window selected.")
            return

        selected_window = windows[selected_index[0]]
        try:
            coords, image_path = capture_window_screenshot(selected_window)
            print(f"📐 Selected window coords: {coords}")
            print(f"🖼️ Screenshot saved to: {image_path}")
            messagebox.showinfo("Window Selected", f"Screenshot saved to:\n{image_path}")
            global selected_coords
            selected_coords = coords
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture window: {e}")

    confirm_button = tk.Button(root, text="Confirm", command=confirm_selection)
    confirm_button.pack(pady=10)

    root.mainloop()
    return selected_coords

def find_minecraft_window_rect():
    for win in gw.getWindowsWithTitle("Minecraft"):
        if win.title and win.width > 100 and win.height > 100:
            return {
                "left": win.left,
                "top": win.top,
                "width": win.width,
                "height": win.height,
                "right": win.right,
                "bottom": win.bottom
            }
    return None
