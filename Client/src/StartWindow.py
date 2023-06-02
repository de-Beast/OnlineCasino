from PySide6 import QtCore, QtGui, QtWidgets

from AllUi.ui_StartWidget import Ui_Start

class StartWindow():
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Start()
        self.UI.setupUi(self.widget)
