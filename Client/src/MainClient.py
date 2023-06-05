from AccountWindow import AccountWindow
from AllUi.ui_MainWindow import Ui_MainWindow
from EnterWindow import EnterWindow
from GameWindow import GameWindow
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget
from RegistrationWindow import RegistrationWindow
from StartWindow import StartWindow

from chat.api import GameType
from Shared.account.enums import AccountInitialResponse


def SavePageToHistory(widget: QWidget):
    history.append(widget)


def SaveLastPageToHistory():
    SavePageToHistory(mainUi.stackedWidget.currentWidget())


def GoBack():
    Game_Window.chatApi.disconnect_from_chat_room()
    Game_Window.rouletteAPI.disconnect_from_game()
    mainUi.stackedWidget.setCurrentWidget(history.pop())


def ToRegistrWindow():
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(Registration_Window.widget)


def ToEnterWindow():
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(Enter_Window.widget)


def ToAccountWindow():
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(Account_Window.widget)


def ToGameWindow():
    Game_Window.chatApi.connect_to_chat_room(GameType.ROULETTE)
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(Game_Window.widget)

    Game_Window.accountAPI.get_account_info()
    Game_Window.rouletteAPI.connect_to_game()

    Game_Window.ClearLayout(Game_Window.UI.horizontalLayout_6) #clear history


def RegisterNavigation():
    Start_Window.UI.EnterButton.clicked.connect(ToEnterWindow)
    Start_Window.UI.RegistrButton.clicked.connect(ToRegistrWindow)

    Enter_Window.UI.backButton.clicked.connect(GoBack)
    Enter_Window.accountAPI.responseAccountInitial.connect(OnEnterResponce)

    Account_Window.UI.pushButton.clicked.connect(GoBack)

    Registration_Window.UI.backButton.clicked.connect(GoBack)
    Registration_Window.accountAPI.responseAccountInitial.connect(OnRegisterResponce)

    Game_Window.UI.accountButton.clicked.connect(ToAccountWindow)
    Game_Window.UI.backButton.clicked.connect(GoBack)


def OnRegisterResponce(responce: AccountInitialResponse):
    print("reg: " + str(responce))
    match responce:
        case AccountInitialResponse.REGISTER_SUCCESS:
            ToGameWindow()
        case _:
            pass


def OnEnterResponce(responce: AccountInitialResponse):
    print("enter: " + str(responce))
    if responce == AccountInitialResponse.AUTH_SUCCESS:
        print(responce)
        ToGameWindow()


history: list[QWidget] = []
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    mainUi = Ui_MainWindow()
    mainUi.setupUi(MainWindow)

    Start_Window = StartWindow()
    Registration_Window = RegistrationWindow()
    Enter_Window = EnterWindow()
    Account_Window = AccountWindow()
    Game_Window = GameWindow()

    mainUi.stackedWidget.addWidget(Start_Window.widget)
    mainUi.stackedWidget.addWidget(Registration_Window.widget)
    mainUi.stackedWidget.addWidget(Enter_Window.widget)
    mainUi.stackedWidget.addWidget(Account_Window.widget)
    mainUi.stackedWidget.addWidget(Game_Window.widget)

    RegisterNavigation()

    MainWindow.show()
    sys.exit(app.exec())
