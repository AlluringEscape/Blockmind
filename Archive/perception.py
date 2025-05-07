from PIL import ImageGrab

def observe_environment():
    screenshot = ImageGrab.grab()
    width, height = screenshot.size

    # Focused region: center 200x200 pixels
    center_x = width // 2
    center_y = height // 2
    box = (center_x - 100, center_y - 100, center_x + 100, center_y + 100)
    focus_area = screenshot.crop(box)

    return {
        'full': screenshot,
        'focus': focus_area
    }
