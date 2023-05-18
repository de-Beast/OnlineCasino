from PySide6 import QtCore, QtGui, QtWidgets

from Client.AllUi.ui_Registration import Ui_Registration
from Client.src.client_sockets.socket_threads.account_initial import AccountInitialSocketThread

class RegistrationWindow():
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Registration()
        self.UI.setupUi(self.widget)

        self.thread = AccountInitialSocketThread()

    def OnRegisterClicked(self):
        email = self.UI.Edit_Email.text()
        password = self.UI.Edit_Password.text()
        self.thread.register(email, password)