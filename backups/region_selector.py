import cv2
import numpy as np
import mss

drawing = False
start_point = (-1, -1)
end_point = (-1, -1)
region = None

def draw_rectangle(event, x, y, flags, param):
    global start_point, end_point, drawing, region

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
        end_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        end_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        x1, y1 = start_point
        x2, y2 = end_point
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x1 - x2), abs(y1 - y2)
        region = (x, y, w, h)
        print(f"✅ Selected region: x={x}, y={y}, width={w}, height={h}")
        cv2.destroyAllWindows()

def select_screen_region():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Full primary monitor
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    clone = img.copy()
    cv2.namedWindow("Select Region")
    cv2.setMouseCallback("Select Region", draw_rectangle)

    while True:
        display = clone.copy()
        if drawing:
            cv2.rectangle(display, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Select Region", display)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cv2.destroyAllWindows()
    return region

if __name__ == "__main__":
    region = select_screen_region()
    if region:
        print(f"Use this for your capture: {region}")
    else:
        print("❌ No region selected.")

