from AllUi.ui_Start import Ui_Start
from PySide6 import QtWidgets


class StartWindow:
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Start()
        self.UI.setupUi(self.widget)
