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

from Client.AllUi.ui_MainWindow import Ui_MainWindow

from Client.src.AccountWindow import AccountWindow
from Client.src.StartWindow import StartWindow
from Client.src.EnterWindow import EnterWindow
from Client.src.RegistrationWindow import RegistrationWindow
from Client.src.GameWindow import GameWindow

def SavePageToHistory(widget : QWidget):
    history.append(widget)
def SaveLastPageToHistory():
    SavePageToHistory(mainUi.stackedWidget.currentWidget())

def GoBack():
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
    SaveLastPageToHistory()
    mainUi.stackedWidget.setCurrentWidget(GameWindow.widget)

def RegisterNavigation():
    StartWindow.UI.EnterButton.clicked.connect(ToEnterWindow)
    StartWindow.UI.RegistrButton.clicked.connect(ToRegistrWindow)

    EnterWindow.UI.Enter_Button.clicked.connect(ToGameWindow)
    EnterWindow.UI.backButton.clicked.connect(GoBack)

    RegistrationWindow.UI.Sign_up.clicked.connect(ToGameWindow)

    AccountWindow.UI.pushButton.clicked.connect(GoBack)

    GameWindow.UI.accountButton.clicked.connect(ToAccountWindow)
    GameWindow.UI.backButton.clicked.connect(GoBack)

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

