
from PIL import Image, ImageStat
import numpy as np
import datetime

def analyze_visual_interest(image, save_debug=False):
    w, h = image.size
    region = image.crop((w//2 - 200, h//2 - 200, w//2 + 200, h//2 + 200))
    pixels = np.array(region)

    avg_r = np.mean(pixels[:,:,0])
    avg_g = np.mean(pixels[:,:,1])
    avg_b = np.mean(pixels[:,:,2])

    brown = avg_r > 90 and avg_g > 50 and avg_b < 80
    green = avg_g > avg_r and avg_g > avg_b and avg_g > 80

    interesting = brown or green

    if save_debug:
        debug_path = f"vision_debug_{datetime.datetime.now().strftime('%H%M%S')}.png"
        region.save(debug_path)

    return {
        "interesting": interesting,
        "avg_r": int(avg_r),
        "avg_g": int(avg_g),
        "avg_b": int(avg_b)
    }
