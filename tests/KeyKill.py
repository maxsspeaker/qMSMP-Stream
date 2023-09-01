import signal, sys
from PyQt6 import QtWidgets # also works with PySide

# You HAVE TO reimplement QApplication.event, otherwise it does not work.
# I believe that you need some python callable to catch the signal
# or KeyboardInterrupt exception.
class Application(QtWidgets.QApplication):
    def event(self, e):
        return QtWidgets.QApplication.event(self, e)

app = Application(sys.argv)

# Connect your cleanup function to signal.SIGINT
signal.signal(signal.SIGINT, lambda *a: app.quit())
# And start a timer to call Application.event repeatedly.
# You can change the timer parameter as you like.
app.startTimer(200)

w = QtWidgets.QWidget()
w.show()
app.exec()
