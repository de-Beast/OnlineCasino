from PySide6 import QtCore, QtGui, QtWidgets

from Client.AllUi.ui_Enter import Ui_Enter
from Client.src.client_sockets.socket_threads.account_initial import AccountInitialSocketThread

class EnterWindow():
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Enter()
        self.UI.setupUi(self.widget)

        self.UI.Enter_Button.clicked.connect(self.OnEnterClicked)

        self.thread = AccountInitialSocketThread()

    def OnEnterClicked(self):
        email = self.UI.Edit_Email.text()
        password = self.UI.Edit_Password.text()
        self.thread.auth(email, password)