import numpy as np

def detect_dimension(image):
    avg_color = image.mean(axis=0).mean(axis=0)
    r, g, b = avg_color

    brightness = (r + g + b) / 3

    # Nether: red glow, dark environment
    if r > 120 and g < 70 and b < 70 and brightness < 100:
        return "nether"

    # End: pale yellow-gray tones, often very bright or very dark
    if 170 < r < 230 and 170 < g < 230 and 100 < b < 180 and brightness > 140:
        return "end"

    # Default
    return "overworld"
