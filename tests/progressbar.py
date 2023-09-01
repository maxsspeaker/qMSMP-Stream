from PyQt5 import QtCore, QtGui, QtWidgets

data = [("1", "Baharak", 10), ("2", "Darwaz", 60),
        ("3", "Fays abad", 20), ("4", "Ishkashim", 80), 
        ("5", "Jurm", 100)]

class ProgressDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        progress = index.data(QtCore.Qt.UserRole+1000)
        opt = QtWidgets.QStyleOptionProgressBar()
        opt.rect = option.rect
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = "{}%".format(progress)
        opt.textVisible = True
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_ProgressBar, opt, painter)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QTableView()
    delegate = ProgressDelegate(w)
    w.setItemDelegateForColumn(2, delegate)
    model = QtGui.QStandardItemModel(0, 3)
    model.setHorizontalHeaderLabels(["ID", "Name", "Progress"])
    for _id, _name, _progress in data:
        it_id = QtGui.QStandardItem(_id)
        it_name = QtGui.QStandardItem(_name)
        it_progress = QtGui.QStandardItem()
        it_progress.setData(_progress, QtCore.Qt.UserRole+1000)
        model.appendRow([it_id, it_name, it_progress])
    w.setModel(model)
    w.show()
    sys.exit(app.exec_())
