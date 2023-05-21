import sys
from PyQt5.QtWidgets import QScrollBar, QDialog, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.createWidgets()

    def createWidgets(self):
        self.layout = QVBoxLayout(self)

        self.scrollbar1 = QScrollBar(Qt.Vertical, self)

        for widget in [self.scrollbar1]:
            widget.valueChanged.connect(self.test)
            self.layout.addWidget(widget)

    def test(self, event):
        print(self.sender().value())


stylesheet = """
    /* --------------------------------------- QScrollBar  -----------------------------------*/

    QScrollBar:vertical
    {
        background-color: #2A2929;
        width: 17px;
        margin: 14px 3px 14px 3px;
        border: 0px transparent;
        border-radius: 0px;
    }

    QScrollBar::handle:vertical
    {
        background-color: #181818;         /* #605F5F; */
        min-height: 5px;
    }
    QScrollBar::handle:vertical:hover
    {
        background-color: #B72E2B;         
        min-height: 5px;
    }

    QScrollBar::sub-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(img/SliderUp.png);
        height: 11px;
        width: 11px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(img/SliderDown.png);
        height: 11px;
        width: 11px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
    {
        border-image: url(img/SliderUpA.png);
        height: 11px;
        width: 11px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
    {
        border-image: url(img/SliderDownA.png);
        height: 11px;
        width: 11px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
    {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
    {
        background: none;
    }
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)       # <----
    GUI = MainWindow()
    GUI.resize(300, 200)
    GUI.show()
    sys.exit(app.exec_())
