import pyautogui
import time

# === MOVEMENT ===
def move_forward(duration=1.0):
    pyautogui.keyDown('w')
    time.sleep(duration)
    pyautogui.keyUp('w')

def move_backward(duration=1.0):
    pyautogui.keyDown('s')
    time.sleep(duration)
    pyautogui.keyUp('s')

def strafe_left(duration=1.0):
    pyautogui.keyDown('a')
    time.sleep(duration)
    pyautogui.keyUp('a')

def strafe_right(duration=1.0):
    pyautogui.keyDown('d')
    time.sleep(duration)
    pyautogui.keyUp('d')

# === TURNING ===
def turn(direction="right", amount=100):
    if direction == "right":
        pyautogui.moveRel(amount, 0, duration=0.2)
    elif direction == "left":
        pyautogui.moveRel(-amount, 0, duration=0.2)
    elif direction == "up":
        pyautogui.moveRel(0, -amount, duration=0.2)
    elif direction == "down":
        pyautogui.moveRel(0, amount, duration=0.2)

# === INTERACTION ===
def punch(duration=1.0):
    pyautogui.mouseDown()
    time.sleep(duration)
    pyautogui.mouseUp()

def pick_up():
    pyautogui.press('e')  # opens inventory — can be used to simulate pickup
    time.sleep(0.5)
    pyautogui.press('e')

# === ACTION HELPERS ===
def wait(seconds=1.0):
    time.sleep(seconds)

def jump():
    pyautogui.press('space')

def sneak(duration=1.0):
    pyautogui.keyDown('shift')
    time.sleep(duration)
    pyautogui.keyUp('shift')
