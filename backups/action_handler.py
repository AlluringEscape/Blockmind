
import pyautogui
import time
import keyboard

class ActionHandler:
    def __init__(self):
        self.last_action_time = time.time()

    def wait(self, delay=0.5):
        time.sleep(delay)

    def move_forward(self, duration=1.0):
        keyboard.press('w')
        self.wait(duration)
        keyboard.release('w')

    def move_backward(self, duration=1.0):
        keyboard.press('s')
        self.wait(duration)
        keyboard.release('s')

    def strafe_left(self, duration=1.0):
        keyboard.press('a')
        self.wait(duration)
        keyboard.release('a')

    def strafe_right(self, duration=1.0):
        keyboard.press('d')
        self.wait(duration)
        keyboard.release('d')

    def jump(self):
        keyboard.press_and_release('space')

    def look_left(self, amount=100):
        pyautogui.moveRel(-amount, 0)

    def look_right(self, amount=100):
        pyautogui.moveRel(amount, 0)

    def look_up(self, amount=100):
        pyautogui.moveRel(0, -amount)

    def look_down(self, amount=100):
        pyautogui.moveRel(0, amount)

    def punch(self, duration=0.5):
        pyautogui.mouseDown()
        self.wait(duration)
        pyautogui.mouseUp()

    def open_inventory(self):
        keyboard.press_and_release('e')

    def crouch(self, duration=1.0):
        keyboard.press('shift')
        self.wait(duration)
        keyboard.release('shift')

    def place_block(self):
        pyautogui.mouseDown(button='right')
        self.wait(0.2)
        pyautogui.mouseUp(button='right')

    def interact(self):
        self.place_block()

    def select_hotbar_slot(self, index):
        if 1 <= index <= 9:
            keyboard.press_and_release(str(index))

    def drop_item(self):
        keyboard.press_and_release('q')

    def swim_up(self, duration=1.0):
        self.jump()
        self.move_forward(duration)

    def sprint_forward(self, duration=1.0):
        keyboard.press('w')
        keyboard.press('ctrl')
        self.wait(duration)
        keyboard.release('ctrl')
        keyboard.release('w')

    def sleep(self, duration=5.0):
        self.wait(duration)
