import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMenu

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()

        PlayListAddMenu = [
            {'add AudioStream': ['YouTube Video', 'soundcloud Treak']},
            'add Local File',
        ]

        btn = QPushButton('Click Me', self)
        btn.setStyleSheet('''font-size:25px;''')
        btn.move(100, 100)
        btn.resize(150, 150)

        menu = QMenu()
        menu.triggered.connect(lambda x: print(x.text()))

        btn.setMenu(menu)
        self.add_menu(PlayListAddMenu, menu)


    def add_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QMenu(k, menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.add_menu(element, menu_obj)
        else:
            action = menu_obj.addAction(data)
            action.setIconVisibleInMenu(False)


app = QApplication(sys.argv)        
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
