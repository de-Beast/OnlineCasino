from AllUi.ui_Enter import Ui_Enter
from PySide6 import QtWidgets

from account.api import AccountAPI


class EnterWindow:
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Enter()
        self.UI.setupUi(self.widget)

        self.accountAPI = AccountAPI()

        self.UI.Enter_Button.clicked.connect(self.OnEnterClicked)

    def OnEnterClicked(self):
        print("enter clicked")
        email = self.UI.Edit_Email.text()
        password = self.UI.Edit_Password.text()
        self.accountAPI.auth(email, password)
