import sys
import traceback
from PyQt5 import QtWidgets, QtGui, QtCore


class ErrorApp:
    # ...

    def raise_error(self):
        assert False


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()
    # or QtWidgets.QApplication.exit(0)


sys.excepthook = excepthook
e = ErrorApp()
ret = e.app.exec_()
print("event loop exited")
sys.exit(ret)
