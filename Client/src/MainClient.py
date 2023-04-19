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
from Client.AllUi.ui_StartWidget import Ui_Start
from Client.AllUi.ui_Enter import Ui_Enter
from Client.AllUi.ui_Registration import Ui_Registration

def OnRegisterClicked():
    SavePageToHistory(StartWidget)
    mainUi.stackedWidget.setCurrentWidget(RegisterWidget)

def OnEnterClicked():
    SavePageToHistory(StartWidget)
    mainUi.stackedWidget.setCurrentWidget(EnterWidget)

def SavePageToHistory(widget):
    history.append(widget)

def GoBack():
    mainUi.stackedWidget.setCurrentWidget(history.pop())

def SetBackButtons():
    enterUi.backButton.clicked.connect(GoBack)
    registerUi.backButton.clicked.connect(GoBack)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    mainUi = Ui_MainWindow()
    mainUi.setupUi(MainWindow)

    StartWidget = QtWidgets.QWidget()
    startUi = Ui_Start()
    startUi.setupUi(StartWidget)

    mainUi.stackedWidget.addWidget(StartWidget)

    RegisterWidget = QtWidgets.QWidget()
    registerUi = Ui_Registration()
    registerUi.setupUi(RegisterWidget)
    startUi.RegistrButton.clicked.connect(OnRegisterClicked)
    mainUi.stackedWidget.addWidget(RegisterWidget)

    EnterWidget = QtWidgets.QWidget()
    enterUi = Ui_Enter()
    enterUi.setupUi(EnterWidget)
    startUi.EnterButton.clicked.connect(OnEnterClicked)
    mainUi.stackedWidget.addWidget(EnterWidget)

    history = []
    SetBackButtons()

    MainWindow.show()
    sys.exit(app.exec())

