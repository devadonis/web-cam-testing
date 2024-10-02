import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap

class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Webcam Feed with Brightness Control")
        self.setGeometry(100, 100, 800, 600)

        # Initialize webcam variable
        self.cap = None

        # Set up the QLabel to display the video
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        # Set up the brightness slider
        self.brightness_slider = QSlider(Qt.Horizontal, self)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.setToolTip("Adjust Brightness")

        # Set up the buttons
        self.open_button = QPushButton("Open Webcam", self)
        self.open_button.clicked.connect(self.open_webcam)
        self.close_button = QPushButton("Close Webcam", self)
        self.close_button.clicked.connect(self.close_webcam)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(self.open_button)
        layout.addWidget(self.close_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up a timer to update the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.stop()  # Initially stopped

        # Initialize brightness value
        self.brightness_value = 0

    def open_webcam(self):
        # Open the webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            return

        # Start the timer to update the video feed
        self.timer.start(30)  # Update every 30 ms

    def close_webcam(self):
        # Stop the timer and release the webcam
        if self.cap is not None:
            self.timer.stop()
            self.cap.release()
            self.cap = None

        # Clear the video label
        self.video_label.clear()

    def update_frame(self):
        if self.cap is None:
            return

        # Read frame from webcam
        ret, frame = self.cap.read()
        if not ret:
            return

        # Update brightness value from slider
        self.brightness_value = self.brightness_slider.value()

        # Apply brightness adjustment
        frame = self.adjust_brightness(frame, self.brightness_value)

        # Convert the frame to QImage format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        q_img = QImage(frame_rgb.data, w, h, w * ch, QImage.Format_RGB888)

        # Set the QImage to QLabel
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)

    def adjust_brightness(self, frame, brightness):
        # Adjust brightness
        frame = frame.astype(np.float32)
        frame += brightness
        frame = np.clip(frame, 0, 255)  # Clip to valid range
        frame = frame.astype(np.uint8)
        return frame

    def closeEvent(self, event):
        # Ensure the webcam is released when closing the application
        self.close_webcam()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec())
