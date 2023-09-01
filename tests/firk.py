from PyQt6 import QtCore, QtGui, QtWidgets
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QtWidgets.QTableView()
        self.setCentralWidget(self.table)
        
        model = QtGui.QStandardItemModel(2, 1)
        self.table.setModel(model)
        
        text = "текст<br>текст"
        item = QtGui.QStandardItemModel()
        item.setData(text, QtCore.Qt.ItemDataRole.DisplayRole)
        item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        model.setItem(0, 0, item)
        
        self.show()
app = QtWidgets.QApplication([])
window = MainWindow()
app.exec()
