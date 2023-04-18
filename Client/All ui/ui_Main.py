# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainBGIclz.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)
import project_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(492, 335)
        MainWindow.setStyleSheet(u"\n"
"background-color: rgb(255, 241, 191);\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        palette = QPalette()
        brush = QBrush(QColor(255, 241, 191, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.centralwidget.setPalette(palette)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MainLogo = QLabel(self.centralwidget)
        self.MainLogo.setObjectName(u"MainLogo")
        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        self.MainLogo.setFont(font)
        self.MainLogo.setStyleSheet(u"color: qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(35, 40, 3, 255), stop:0.16 rgba(136, 106, 22, 255), stop:0.225 rgba(166, 140, 41, 255), stop:0.285 rgba(204, 181, 74, 255), stop:0.345 rgba(235, 219, 102, 255), stop:0.415 rgba(245, 236, 112, 255), stop:0.52 rgba(209, 190, 76, 255), stop:0.57 rgba(187, 156, 51, 255), stop:0.635 rgba(168, 142, 42, 255), stop:0.695 rgba(202, 174, 68, 255), stop:0.75 rgba(218, 202, 86, 255), stop:0.815 rgba(208, 187, 73, 255), stop:0.88 rgba(187, 156, 51, 255), stop:0.935 rgba(137, 108, 26, 255), stop:1 rgba(35, 40, 3, 255));")
        self.MainLogo.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.MainLogo)

        self.Win = QLabel(self.centralwidget)
        self.Win.setObjectName(u"Win")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(False)
        font1.setItalic(False)
        self.Win.setFont(font1)
        self.Win.setStyleSheet(u"")
        self.Win.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.Win)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.EnterButton = QPushButton(self.centralwidget)
        self.EnterButton.setObjectName(u"EnterButton")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        self.EnterButton.setFont(font2)
        self.EnterButton.setStyleSheet(u"background: rgba(140, 101, 65, 0.6);\n"
"border: 4px solid rgba(140, 101, 65, 0.38);\n"
"border-radius: 30px;")

        self.verticalLayout.addWidget(self.EnterButton)

        self.RegistrButton = QPushButton(self.centralwidget)
        self.RegistrButton.setObjectName(u"RegistrButton")
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(True)
        self.RegistrButton.setFont(font3)
        self.RegistrButton.setStyleSheet(u"background: #F4D874;\n"
"border-radius: 30px;")

        self.verticalLayout.addWidget(self.RegistrButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u043a\u0430\u0437\u0438\u043d\u043e", None))
        self.MainLogo.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0418\u0420 \u0424\u0418\u0428\u0415\u041a", None))
        self.Win.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0423\u0427\u0428\u0418\u0415 \u0418\u0413\u0420\u042b \u0418 \u0427\u0415\u0421\u0422\u041d\u042b\u0415 \u0412\u042b\u0418\u0413\u0420\u042b\u0428\u0418", None))
        self.EnterButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0425\u041e\u0414", None))
        self.RegistrButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0415\u0413\u0418\u0421\u0422\u0420\u0418\u0420\u0423\u0419\u0421\u042f \u041f\u0420\u042f\u041c\u041e \u0421\u0415\u0419\u0427\u0410\u0421!", None))
    # retranslateUi

