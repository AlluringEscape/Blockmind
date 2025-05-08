
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import Qt, QTimer
import cv2
from blockmind_vision import get_latest_frame

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blockmind Overlay")
        self.setGeometry(100, 100, 640, 480)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.image = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # refresh every 100ms

    def update_frame(self):
        frame = get_latest_frame()
        if frame is not None:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            self.image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.update()

    def paintEvent(self, event):
        if self.image:
            painter = QPainter(self)
            painter.drawImage(0, 0, self.image)

def run_overlay():
    app = QApplication(sys.argv)
    window = OverlayWindow()
    window.show()
    sys.exit(app.exec_())

def start_overlay_thread():
    thread = threading.Thread(target=run_overlay, daemon=True)
    thread.start()
