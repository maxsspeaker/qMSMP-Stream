import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut, QLabel, QApplication, QHBoxLayout
from PyQt5 import QtCore 

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        #self.label = QLabel("Try Ctrl+O", self)
        self.shortcut = QShortcut(QKeySequence("Qt::Key_MediaPause"), self)
        self.shortcut.activated.connect(self.on_open)

        self.layout = QHBoxLayout()
        #self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.resize(150, 100)
        self.show()

    @pyqtSlot()
    def on_open(self):
        print("Opening!")
        
    def keyPressEvent(self, event):
         key = event.key()
         print(key)
         if key == QtCore.Qt.Key_MediaPrevious:
              print('test2')
         elif str(key) == "16777344":
              print('test1')
         elif key == QtCore.Qt.Key_MediaNext:
              print('test2')

app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())
