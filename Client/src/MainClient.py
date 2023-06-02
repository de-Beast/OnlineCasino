from PySide6 import QtCore, QtGui, QtWidgets

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

#import Client.src.chat.api
from Shared.account.enums import AccountInitialResponse, AccountInitialRequest

from chat.api import GameType

from AllUi.ui_MainWindow import Ui_MainWindow
from AccountWindow import AccountWindow
from StartWindow import StartWindow
from EnterWindow import EnterWindow
from RegistrationWindow import RegistrationWindow
from GameWindow import GameWindow

def SavePageToHistory(widget : QWidget):
    history.append(widget)
def SaveLastPageToHistory():
    SavePageToHistory(mainUi.stackedWidget.currentWidget())

def GoBack():
    GameWindow.chatApi.disconnect_from_chat_room()
    mainUi.stackedWidget.setCurrentWidget(history.pop())

def ToRegistrWindow():
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(RegistrationWindow.widget)

def ToEnterWindow():
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(EnterWindow.widget)

def ToAccountWindow():
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(AccountWindow.widget)

def ToGameWindow():
    GameWindow.chatApi.connect_to_chat_room(GameType.ROULETTE)
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(GameWindow.widget)

    GameWindow.accountAPI.get_account_info()
    #GameWindow.rouletteAPI.connect_to_game()

def RegisterNavigation():
    StartWindow.UI.EnterButton.clicked.connect(ToEnterWindow)
    StartWindow.UI.RegistrButton.clicked.connect(ToRegistrWindow)

    EnterWindow.UI.backButton.clicked.connect(GoBack)
    EnterWindow.accountAPI.responseAccountInitial.connect(OnEnterResponce)

    AccountWindow.UI.pushButton.clicked.connect(GoBack)

    RegistrationWindow.accountAPI.responseAccountInitial.connect(OnRegisterResponce)

    GameWindow.UI.accountButton.clicked.connect(ToAccountWindow)
    GameWindow.UI.backButton.clicked.connect(GoBack)

def OnRegisterResponce(responce : AccountInitialResponse):
    print("reg: " + str(responce))
    match responce:
        case AccountInitialResponse.REGISTER_SUCCESS:
            ToGameWindow()
        case _:
            pass

def OnEnterResponce(responce : AccountInitialResponse):
    print("enter: " + str(responce))
    if responce == AccountInitialResponse.AUTH_SUCCESS:
        print(responce)
        ToGameWindow()

history = []
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    mainUi = Ui_MainWindow()
    mainUi.setupUi(MainWindow)

    StartWindow = StartWindow()
    RegistrationWindow = RegistrationWindow()
    EnterWindow = EnterWindow()
    AccountWindow = AccountWindow()
    GameWindow = GameWindow()

    mainUi.stackedWidget.addWidget(StartWindow.widget)
    mainUi.stackedWidget.addWidget(RegistrationWindow.widget)
    mainUi.stackedWidget.addWidget(EnterWindow.widget)
    mainUi.stackedWidget.addWidget(AccountWindow.widget)
    mainUi.stackedWidget.addWidget(GameWindow.widget)

    RegisterNavigation()


    MainWindow.show()
    sys.exit(app.exec())

