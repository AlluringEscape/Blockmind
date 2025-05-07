
import sys
import numpy as np
import cv2
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.label = QLabel(self)
        self.setGeometry(0, 0, 1920, 1080)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(33)  # ~30 FPS

    def update_overlay(self):
        # Capture screen (center region or full screen)
        img = np.array(ImageGrab.grab())

        # Draw overlay content (green box at crosshair)
        cv2.rectangle(img, (1275, 691), (1285, 701), (0, 255, 0), 2)
        cv2.putText(img, "Crosshair", (1275, 685), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        # Convert to QImage and display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.label.setPixmap(QPixmap.fromImage(qt_img))

def run_overlay():
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.showFullScreen()
    sys.exit(app.exec_())
