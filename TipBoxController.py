from PyQt5 import QtWidgets
from views.Tip import Ui_tipBox


class TipBoxController(QtWidgets.QDialog):
    def __init__(self):
        super(TipBoxController, self).__init__()
        self.ui = Ui_tipBox()
        self.ui.setupUi(self)