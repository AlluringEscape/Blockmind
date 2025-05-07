
from PIL import ImageStat

def is_likely_tree(image):
    # Simple heuristic: trees usually have brown + green
    w, h = image.size
    center_crop = image.crop((w//2 - 50, h//2 - 50, w//2 + 50, h//2 + 50))
    stat = ImageStat.Stat(center_crop)
    r, g, b = stat.mean[:3]

    brownish = (r > 80 and r < 160) and (g > 50 and g < 120) and (b < 80)
    greenish = g > r and g > b and g > 80

    return brownish or greenish
