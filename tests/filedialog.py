from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5 import QtCore
import sys


def dialog():
    file , check = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileName()",
                                               "", "Mp3 files (*.mp3);;All Files (*)")
    if check:
        print(file)

def dialog2():
    file , check = QFileDialog.getSaveFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "PlayList File files (*.plmsmpsbox);;All Files (*)")
    if check:
        print(file)

app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(400,400,300,300)

 
button = QPushButton(win)
button.setText("Press")
button.clicked.connect(dialog2)
button.move(50,50)


button2 = QPushButton(win)
button2.setText("Press2")
button2.clicked.connect(dialog2)
button2.move(50,100)

win.show()
sys.exit(app.exec_())
