
from PIL import Image
import numpy as np

def find_interesting_region(focus_image):
    # Convert image to numpy array
    img_array = np.array(focus_image)

    # Compute basic pixel uniqueness across small chunks
    chunk_size = 20
    height, width, _ = img_array.shape
    scores = []

    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            chunk = img_array[y:y+chunk_size, x:x+chunk_size]
            if chunk.shape[0] != chunk_size or chunk.shape[1] != chunk_size:
                continue
            variance = np.var(chunk)
            scores.append((variance, (x + chunk_size//2, y + chunk_size//2)))

    # Sort regions by highest variance (likely to be unique/interesting)
    scores.sort(reverse=True)

    if scores:
        return scores[0][1]  # Return most unique region's center
    return None
