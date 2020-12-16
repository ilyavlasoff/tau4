from MainWindowController import MainWindowController
from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication([])
qapp = MainWindowController()
qapp.show()
sys.exit(app.exec())
