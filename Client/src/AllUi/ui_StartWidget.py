# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerhfNbOZ.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Start(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(682, 416)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MainLogo = QLabel(Form)
        self.MainLogo.setObjectName(u"MainLogo")
        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        self.MainLogo.setFont(font)
        self.MainLogo.setStyleSheet(u"color: qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(35, 40, 3, 255), stop:0.16 rgba(136, 106, 22, 255), stop:0.225 rgba(166, 140, 41, 255), stop:0.285 rgba(204, 181, 74, 255), stop:0.345 rgba(235, 219, 102, 255), stop:0.415 rgba(245, 236, 112, 255), stop:0.52 rgba(209, 190, 76, 255), stop:0.57 rgba(187, 156, 51, 255), stop:0.635 rgba(168, 142, 42, 255), stop:0.695 rgba(202, 174, 68, 255), stop:0.75 rgba(218, 202, 86, 255), stop:0.815 rgba(208, 187, 73, 255), stop:0.88 rgba(187, 156, 51, 255), stop:0.935 rgba(137, 108, 26, 255), stop:1 rgba(35, 40, 3, 255));")
        self.MainLogo.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.MainLogo)

        self.Win = QLabel(Form)
        self.Win.setObjectName(u"Win")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(False)
        font1.setItalic(False)
        self.Win.setFont(font1)
        self.Win.setStyleSheet(u"")
        self.Win.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.Win)

        self.verticalSpacer = QSpacerItem(471, 24, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.EnterButton = QPushButton(Form)
        self.EnterButton.setObjectName(u"EnterButton")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        self.EnterButton.setFont(font2)
        self.EnterButton.setStyleSheet(u"background: rgba(140, 101, 65, 0.6);\n"
"border: 4px solid rgba(140, 101, 65, 0.38);\n"
"border-radius: 30px;")

        self.verticalLayout.addWidget(self.EnterButton)

        self.RegistrButton = QPushButton(Form)
        self.RegistrButton.setObjectName(u"RegistrButton")
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(True)
        self.RegistrButton.setFont(font3)
        self.RegistrButton.setStyleSheet(u"background: #F4D874;\n"
"border-radius: 30px;")

        self.verticalLayout.addWidget(self.RegistrButton)

        self.verticalSpacer_2 = QSpacerItem(471, 249, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.MainLogo.setText(QCoreApplication.translate("Form", u"\u041c\u0418\u0420 \u0424\u0418\u0428\u0415\u041a", None))
        self.Win.setText(QCoreApplication.translate("Form", u"\u041b\u0423\u0427\u0428\u0418\u0415 \u0418\u0413\u0420\u042b \u0418 \u0427\u0415\u0421\u0422\u041d\u042b\u0415 \u0412\u042b\u0418\u0413\u0420\u042b\u0428\u0418", None))
        self.EnterButton.setText(QCoreApplication.translate("Form", u"\u0412\u0425\u041e\u0414", None))
        self.RegistrButton.setText(QCoreApplication.translate("Form", u"\u0420\u0415\u0413\u0418\u0421\u0422\u0420\u0418\u0420\u0423\u0419\u0421\u042f \u041f\u0420\u042f\u041c\u041e \u0421\u0415\u0419\u0427\u0410\u0421!", None))
    # retranslateUi

