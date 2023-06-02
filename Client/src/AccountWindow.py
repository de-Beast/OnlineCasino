from PySide6 import QtCore, QtGui, QtWidgets

from Client.AllUi.ui_Account import Ui_Account
from Client.src.client_sockets.socket_threads.account_info import AccountInfoSocketThread

class AccountWindow():
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Account()
        self.UI.setupUi(self.widget)

        self.thread = AccountInfoSocketThread()
        self.thread.responseRecieved.connect(self.OnUpdateAccountInfo)

    def OnUpdateAccountInfo(self, info : dict):
        self.UI.emailEdit.setText(info['login'])
        self.UI.passwordEdit.setText(info['password'])
        self.UI.balanceLabel.setText(str(info['balance']))

        #history = self.UI.historyTable
        #history.clear()

        #for ind, operation in enumerate(info['operations']):
        #    history.setItem(ind, 0, QtWidgets.QTableWidgetItem(operation[0])) #тип операции
        #    history.setItem(ind, 1, QtWidgets.QTableWidgetItem(operation[1])) #откуда
        #    history.setItem(ind, 2, QtWidgets.QTableWidgetItem(operation[2])) #цена
        #    print(ind, operation)