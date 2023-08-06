import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider


class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            new_value = self.minimum() + ((self.maximum() - self.minimum()) * event.x()) / self.width()
            self.setValue(new_value)
        super().mousePressEvent(event)


class CustomSliderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Clickable Slider Example")
        self.setGeometry(100, 100, 300, 100)

        slider = ClickableSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)

        self.setCentralWidget(slider)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomSliderApp()
    window.show()
    sys.exit(app.exec())
