import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.trayIcon = QSystemTrayIcon(self)
        icon = QIcon("../icon.png")
        self.trayIcon.setIcon(icon)
        self.trayIcon.setVisible(True)
        self.trayMenu = QMenu()
        action = QAction("A menu item", self)
        self.trayMenu.addAction(action)
        quitAction = QAction("Quit", self)
        quitAction.triggered.connect(QApplication.instance().quit)
        self.trayMenu.addAction(quitAction)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.activated.connect(self.handleTrayIconActivated)
    def handleTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
