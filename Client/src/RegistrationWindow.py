from PySide6 import QtCore, QtGui, QtWidgets

from Client.AllUi.ui_Registration import Ui_Registration
from Client.src.account.api import AccountAPI

class RegistrationWindow():
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Registration()
        self.UI.setupUi(self.widget)

        self.accountAPI = AccountAPI()

        self.UI.Sign_up.clicked.connect(self.OnRegisterClicked)

    def OnRegisterClicked(self):
        email = self.UI.Edit_Email.text()
        password = self.UI.Edit_Password.text()
        self.accountAPI.register(email, password)