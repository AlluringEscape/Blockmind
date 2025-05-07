import numpy as np
import cv2

def detect_features(image):
    features = []

    h, w, _ = image.shape
    center_pixel = image[h // 2, w // 2]
    avg_color = image.mean(axis=0).mean(axis=0)
    brightness = avg_color.mean()

    # === Tree Detection (green + brown vertical forms)
    green = avg_color[1] > 100 and avg_color[0] < 100 and avg_color[2] < 100
    brownish = 50 < center_pixel[0] < 120 and 40 < center_pixel[1] < 100 and 20 < center_pixel[2] < 70
    if green and brownish:
        features.append("tree")

    # === Water Detection (blue-heavy horizontal patches)
    if avg_color[0] < 100 and avg_color[1] < 140 and avg_color[2] > 130:
        features.append("water")

    # === Cliff Detection (sharp vertical brightness changes)
    vertical_gradient = np.abs(cv2.Sobel(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F, 0, 1, ksize=5)).mean()
    if vertical_gradient > 30 and brightness < 100:
        features.append("cliff")

    # === Hill Detection (slight upward gradient, sky break)
    top_strip = image[0:50, w//2-25:w//2+25]
    sky_pixels = np.mean(top_strip) > 180
    if sky_pixels and vertical_gradient > 10:
        features.append("hill")

    if not features:
        features.append("flat_land")

    return features


def detect_structures(image):
    structures = []

    h, w, _ = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 180)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    building_like = 0
    tall_rectangles = 0

    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        aspect_ratio = cw / float(ch + 1)
        area = cw * ch

        # Building-like shapes
        if 3000 < area < 20000 and 0.6 < aspect_ratio < 1.8:
            building_like += 1
        # Portal/doorway shapes
        if 0.2 < aspect_ratio < 0.5 and ch > 50:
            tall_rectangles += 1

    if building_like >= 3:
        structures.append("structure")

    if tall_rectangles >= 2:
        structures.append("portal_or_door")

    return structures
