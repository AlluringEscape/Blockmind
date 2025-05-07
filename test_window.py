import cv2
import numpy as np

cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Test", 800, 600)
cv2.imshow("Test", np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()