# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EntertbYJus.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import project_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(688, 403)
        Form.setStyleSheet(u"image: url(:/Money/pngegg (1) 1.png);\n"
"\n"
"background-color: rgb(255, 241, 191);")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Necasino = QLabel(Form)
        self.Necasino.setObjectName(u"Necasino")
        font = QFont()
        font.setPointSize(45)
        font.setBold(True)
        self.Necasino.setFont(font)
        self.Necasino.setStyleSheet(u"color: qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(35, 40, 3, 255), stop:0.16 rgba(136, 106, 22, 255), stop:0.225 rgba(166, 140, 41, 255), stop:0.285 rgba(204, 181, 74, 255), stop:0.345 rgba(235, 219, 102, 255), stop:0.415 rgba(245, 236, 112, 255), stop:0.52 rgba(209, 190, 76, 255), stop:0.57 rgba(187, 156, 51, 255), stop:0.635 rgba(168, 142, 42, 255), stop:0.695 rgba(202, 174, 68, 255), stop:0.75 rgba(218, 202, 86, 255), stop:0.815 rgba(208, 187, 73, 255), stop:0.88 rgba(187, 156, 51, 255), stop:0.935 rgba(137, 108, 26, 255), stop:1 rgba(35, 40, 3, 255));")

        self.verticalLayout_2.addWidget(self.Necasino, 0, Qt.AlignHCenter)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.Registr = QLabel(Form)
        self.Registr.setObjectName(u"Registr")
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.Registr.setFont(font1)
        self.Registr.setStyleSheet(u"color: rgb(70, 34, 8);")

        self.verticalLayout_2.addWidget(self.Registr, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.Email1 = QLabel(Form)
        self.Email1.setObjectName(u"Email1")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        self.Email1.setFont(font2)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.Email1)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"background-color: rgb(244, 216, 116);")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.Password1 = QLabel(Form)
        self.Password1.setObjectName(u"Password1")
        self.Password1.setFont(font2)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.Password1)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(244, 216, 116);")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.Login1 = QPushButton(Form)
        self.Login1.setObjectName(u"Login1")
        self.Login1.setFont(font2)

        self.verticalLayout_2.addWidget(self.Login1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u041c\u0438\u0440 \u0444\u0438\u0448\u0435\u043a", None))
        self.Necasino.setText(QCoreApplication.translate("Form", u"\u041c\u0418\u0420  \u0424\u0418\u0428\u0415\u041a", None))
        self.Registr.setText(QCoreApplication.translate("Form", u"\u0412\u0425\u041e\u0414 \u0412 \u041b\u0418\u0427\u041d\u042b\u0419 \u041a\u0410\u0411\u0418\u041d\u0415\u0422", None))
        self.Email1.setText(QCoreApplication.translate("Form", u"\u0410\u0434\u0440\u0435\u0441 \u043f\u043e\u0447\u0442\u044b", None))
        self.Password1.setText(QCoreApplication.translate("Form", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.Login1.setText(QCoreApplication.translate("Form", u"\u0412\u041e\u0419\u0422\u0418", None))
    # retranslateUi

