import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from blockmind_vision import get_latest_detection_image

def run_overlay():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
    window.setAttribute(Qt.WA_TranslucentBackground)
    window.setAttribute(Qt.WA_TransparentForMouseEvents)
    label = QLabel(window)
    label.resize(1280, 720)
    window.setGeometry(100, 100, 1280, 720)
    window.show()

    def update():
        frame = get_latest_detection_image()
        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap)

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(100)

    sys.exit(app.exec_())
