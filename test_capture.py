# Temporary test script: test_capture.py
from blockmind_window_capture import ThreadSafeCapturer
capturer = ThreadSafeCapturer()
frame = capturer.capture_frame()
print(f"Capture result: {frame is not None}")
