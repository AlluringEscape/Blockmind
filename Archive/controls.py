import ctypes
import time
import pyautogui
import random
import math
import keyboard  # low-level keyboard input

# Windows mouse movement constants
MOUSEEVENTF_MOVE = 0x0001

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MouseInput)
    ]

def move_mouse_relative(x, y):
    extra = ctypes.c_ulong(0)
    mi = MouseInput(dx=x, dy=y, mouseData=0, dwFlags=MOUSEEVENTF_MOVE, time=0, dwExtraInfo=ctypes.pointer(extra))
    input_struct = Input(type=0, mi=mi)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_struct), ctypes.sizeof(input_struct))

# === Movement ===
def move_forward(duration=0.5):
    keyboard.press('w')
    time.sleep(duration)
    keyboard.release('w')

def move_backward(duration=0.5):
    keyboard.press('s')
    time.sleep(duration)
    keyboard.release('s')

def strafe_left(duration=0.5):
    keyboard.press('a')
    time.sleep(duration)
    keyboard.release('a')

def strafe_right(duration=0.5):
    keyboard.press('d')
    time.sleep(duration)
    keyboard.release('d')

def jump():
    keyboard.press("space")
    time.sleep(0.1)  # hold the key for realism
    keyboard.release("space")

def sneak(duration=0.5):
    keyboard.press('shift')
    time.sleep(duration)
    keyboard.release('shift')

def sprint(duration=0.5):
    keyboard.press('ctrl')
    keyboard.press('w')
    time.sleep(duration)
    keyboard.release('w')
    keyboard.release('ctrl')

# === Mouse-based interaction ===
def punch(duration=2.5):
    press_key("left")
    time.sleep(duration)
    release_key("left")


def use_item():
    pyautogui.mouseDown(button='right')
    time.sleep(0.1)
    pyautogui.mouseUp(button='right')

def pick_block():
    pyautogui.middleClick()

# === Inventory and slots ===
def open_inventory():
    keyboard.send('e')

def drop_item():
    keyboard.send('q')

def swap_offhand():
    keyboard.send('f')

def select_hotbar_slot(slot: int):
    if 1 <= slot <= 9:
        keyboard.send(str(slot))

# === Mouse look ===
def look_left(pixels=100):
    step = 5
    delay = 0.01
    for _ in range(0, pixels, step):
        move_mouse_relative(-step, 0)
        time.sleep(delay)

def look_right(pixels=100):
    step = 5
    delay = 0.01
    for _ in range(0, pixels, step):
        move_mouse_relative(step, 0)
        time.sleep(delay)

def look_up(pixels=100):
    step = 5
    delay = 0.01
    for _ in range(0, pixels, step):
        move_mouse_relative(0, -step)
        time.sleep(delay)

def look_down(pixels=100):
    step = 5
    delay = 0.01
    for _ in range(0, pixels, step):
        move_mouse_relative(0, step)
        time.sleep(delay)

def look_diagonal():
    dx = random.choice([-1, 1]) * random.randint(30, 100)
    dy = random.choice([-1, 1]) * random.randint(30, 100)
    steps = 10
    for _ in range(steps):
        move_mouse_relative(dx // steps, dy // steps)
        time.sleep(0.01)

def look_spin(degrees=360, radius=100):
    steps = int(degrees / 10)
    for i in range(steps):
        angle = math.radians(i * (360 / steps))
        dx = int(math.cos(angle) * radius / steps)
        dy = int(math.sin(angle) * radius / steps)
        move_mouse_relative(dx, dy)
        time.sleep(0.01)

def look_around():
    direction = random.choice(["left", "right", "up", "down", "diagonal", "spin"])
    if direction == "left":
        look_left()
    elif direction == "right":
        look_right()
    elif direction == "up":
        look_up()
    elif direction == "down":
        look_down()
    elif direction == "diagonal":
        look_diagonal()
    elif direction == "spin":
        look_spin()
