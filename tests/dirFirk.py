
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication, QMainWindow, QAbstractItemView
from PyQt5.QtCore import QDir, QModelIndex, QSize

class TreeView(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Дерево файлов')
        self.setGeometry(100, 100, 800, 600)

        root_path = r"A:\YandexDisk\python-projects\bmCastMusic\myPlaylists"
        self.model = self.get_file_tree_model(root_path)#.setHorizontalHeaderLabels(["Files"])

        self.tree = QTreeView(self)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(root_path))
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.resizeColumnToContents(0)
        self.tree.setColumnWidth(0, self.tree.columnWidth(0) + 20)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.doubleClicked.connect(self.handle_double_click)
        #self.tree.setHorizontalHeaderLabels(["file"])
        self.tree.hideColumn(3)
        self.tree.hideColumn(2)
        self.tree.hideColumn(1)

        self.setCentralWidget(self.tree)

    def get_file_tree_model(self, root_path):
        model = QFileSystemModel()
        model.setRootPath(root_path)
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        model.setNameFilters(['*'])
        model.setNameFilterDisables(False)
        return model

    def handle_double_click(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            if not self.model.canFetchMore(index):
                self.model.fetchMore(index)
            if self.model.rowCount(index) > 0:
                self.tree.setExpanded(index, True)
        else:
            print(path)

    def expand_all(self):
        self.tree.expandAll()

    def collapse_all(self):
        self.tree.collapseAll()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = TreeView()
    window.show()
    sys.exit(app.exec_())

