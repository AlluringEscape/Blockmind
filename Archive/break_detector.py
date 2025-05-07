
from PIL import ImageChops, ImageStat
import time

def block_was_broken(before_image, after_image, threshold=10):
    # Crop small region at center
    w, h = before_image.size
    box = (w//2 - 5, h//2 - 5, w//2 + 5, h//2 + 5)
    before_crop = before_image.crop(box)
    after_crop = after_image.crop(box)

    # Compare the center pixels
    diff = ImageChops.difference(before_crop, after_crop)
    stat = ImageStat.Stat(diff)
    diff_score = sum(stat.mean)

    return diff_score > threshold
