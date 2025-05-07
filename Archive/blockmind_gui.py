import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import pyautogui
import cv2
import numpy as np
from blockmind_brain import BlockmindBrain

# --- GUI Setup ---
class BlockmindGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Blockmind Autopilot")
        self.running = False

        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(root, width=80, height=30, state="disabled", font=("Consolas", 10))
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Buttons
        self.toggle_button = tk.Button(root, text="Start", width=20, command=self.toggle)
        self.toggle_button.grid(row=1, column=0, padx=10, pady=10)

        self.quit_button = tk.Button(root, text="Exit", width=20, command=root.quit)
        self.quit_button.grid(row=1, column=1, padx=10, pady=10)

        # AI Instance
        self.brain = BlockmindBrain({
            "name": "andy",
            "model": "meta-llama/meta-llama-3-8b-instruct",
            "llm_provider": "llama3",
            "llm_url": "http://127.0.0.1:1234/v1/chat/completions",
            "load_memory": True
        })

    def toggle(self):
        if self.running:
            self.running = False
            self.toggle_button.config(text="Start")
            self.log("🛑 Stopped.")
        else:
            self.running = True
            self.toggle_button.config(text="Stop")
            self.log("🧠 Blockmind Started")
            threading.Thread(target=self.main_loop).start()

    def main_loop(self):
        while self.running:
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            result = self.brain.suggest_survival_goal()
            self.log(f"🎯 Suggested Goal: {result}")
            self.brain.perform_action(result)
            time.sleep(2)

    def log(self, text):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, text + "\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state="disabled")

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    gui = BlockmindGUI(root)
    root.mainloop()
