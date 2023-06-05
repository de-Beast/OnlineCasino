# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Registration.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import project_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(838, 625)
        Form.setStyleSheet(u"\n"
"\n"
"background-color: rgb(255, 241, 191);")
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.backButton = QPushButton(Form)
        self.backButton.setObjectName(u"backButton")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Manrope"])
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.backButton.setFont(font)
        self.backButton.setStyleSheet(u"font-family: 'Manrope';\n"
"font-style: normal;\n"
"\n"
"text-align: center;\n"
"\n"
"background: rgba(140, 101, 65, 0.7);\n"
"border: 2px solid rgba(140, 101, 65, 0.7);\n"
"border-radius: 10px;\n"
"padding: 3px;")

        self.verticalLayout_4.addWidget(self.backButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Icon1 = QLabel(Form)
        self.Icon1.setObjectName(u"Icon1")
        self.Icon1.setStyleSheet(u"border-image: url(:/Money/pngegg (1) 1.png);\n"
"object-fit: none;")
        self.Icon1.setScaledContents(True)
        self.Icon1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.Icon1)

        self.Logo = QLabel(Form)
        self.Logo.setObjectName(u"Logo")
        font1 = QFont()
        font1.setFamilies([u"Manrope"])
        font1.setPointSize(45)
        font1.setBold(True)
        self.Logo.setFont(font1)
        self.Logo.setStyleSheet(u"color: qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(35, 40, 3, 255), stop:0.16 rgba(136, 106, 22, 255), stop:0.225 rgba(166, 140, 41, 255), stop:0.285 rgba(204, 181, 74, 255), stop:0.345 rgba(235, 219, 102, 255), stop:0.415 rgba(245, 236, 112, 255), stop:0.52 rgba(209, 190, 76, 255), stop:0.57 rgba(187, 156, 51, 255), stop:0.635 rgba(168, 142, 42, 255), stop:0.695 rgba(202, 174, 68, 255), stop:0.75 rgba(218, 202, 86, 255), stop:0.815 rgba(208, 187, 73, 255), stop:0.88 rgba(187, 156, 51, 255), stop:0.935 rgba(137, 108, 26, 255), stop:1 rgba(35, 40, 3, 255));")
        self.Logo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.Logo)

        self.Icon2 = QLabel(Form)
        self.Icon2.setObjectName(u"Icon2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Icon2.sizePolicy().hasHeightForWidth())
        self.Icon2.setSizePolicy(sizePolicy1)
        self.Icon2.setStyleSheet(u"border-image: url(:/Money/pngegg (1) 1.png);\n"
"background-fit: fit;")
        self.Icon2.setScaledContents(False)

        self.horizontalLayout.addWidget(self.Icon2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.Bonus = QLabel(Form)
        self.Bonus.setObjectName(u"Bonus")
        font2 = QFont()
        font2.setFamilies([u"Manrope"])
        font2.setPointSize(20)
        font2.setBold(True)
        font2.setItalic(False)
        self.Bonus.setFont(font2)
        self.Bonus.setStyleSheet(u"position: absolute;\n"
"width: 1061.33px;\n"
"height: 154.46px;\n"
"left: 105.19px;\n"
"top: 22.74px;\n"
"\n"
"font-family: 'Manrope';\n"
"font-style: normal;\n"
"font-weight: 800;\n"
"font-size: 52.1191px;\n"
"line-height: 71px;\n"
"display: flex;\n"
"align-items: center;\n"
"text-align: center;\n"
"\n"
"color: #462208;")
        self.Bonus.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.Bonus)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(5)
        self.formLayout.setVerticalSpacing(15)
        self.Email = QLabel(Form)
        self.Email.setObjectName(u"Email")
        self.Email.setFont(font)
        self.Email.setStyleSheet(u"position: absolute;\n"
"width: 387.37px;\n"
"height: 75.64px;\n"
"left: 0px;\n"
"top: 13.75px;\n"
"\n"
"font-family: 'Manrope';\n"
"font-style: normal;\n"
"font-weight: 800;\n"
"font-size: 34.382px;\n"
"line-height: 47px;\n"
"display: flex;\n"
"align-items: center;\n"
"text-align: center;\n"
"\n"
"color: #462208;")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.Email)

        self.Edit_Email = QLineEdit(Form)
        self.Edit_Email.setObjectName(u"Edit_Email")
        self.Edit_Email.setMinimumSize(QSize(0, 30))
        self.Edit_Email.setStyleSheet(u"background-color: rgb(244, 216, 116);\n"
"border-radius: 15px;")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.Edit_Email)

        self.Password = QLabel(Form)
        self.Password.setObjectName(u"Password")
        self.Password.setFont(font)
        self.Password.setStyleSheet(u"position: absolute;\n"
"width: 387.37px;\n"
"height: 75.64px;\n"
"left: 0px;\n"
"top: 13.75px;\n"
"\n"
"font-family: 'Manrope';\n"
"font-style: normal;\n"
"font-weight: 800;\n"
"font-size: 34.382px;\n"
"line-height: 47px;\n"
"display: flex;\n"
"align-items: center;\n"
"text-align: center;\n"
"\n"
"color: #462208;")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.Password)

        self.Edit_Password = QLineEdit(Form)
        self.Edit_Password.setObjectName(u"Edit_Password")
        self.Edit_Password.setMinimumSize(QSize(0, 30))
        self.Edit_Password.setStyleSheet(u"background-color: rgb(244, 216, 116);\n"
"border-radius: 15px")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.Edit_Password)


        self.verticalLayout_4.addLayout(self.formLayout)

        self.Sign_up = QPushButton(Form)
        self.Sign_up.setObjectName(u"Sign_up")
        self.Sign_up.setFont(font)
        self.Sign_up.setStyleSheet(u"font-family: 'Manrope';\n"
"font-style: normal;\n"
"\n"
"text-align: center;\n"
"\n"
"background: rgba(140, 101, 65, 0.7);\n"
"border: 2px solid rgba(140, 101, 65, 0.7);\n"
"border-radius: 10px;")

        self.verticalLayout_4.addWidget(self.Sign_up)

        self.Chips = QLabel(Form)
        self.Chips.setObjectName(u"Chips")
        self.Chips.setStyleSheet(u"border-image: url(:/Money/money.png)")
        self.Chips.setScaledContents(False)

        self.verticalLayout_4.addWidget(self.Chips)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u041c\u0438\u0440 \u0444\u0438\u0448\u0435\u043a", None))
        self.backButton.setText(QCoreApplication.translate("Form", u"\u041d\u0410\u0417\u0410\u0414", None))
        self.Icon1.setText("")
        self.Logo.setText(QCoreApplication.translate("Form", u"\u041c\u0418\u0420  \u0424\u0418\u0428\u0415\u041a", None))
        self.Icon2.setText("")
        self.Bonus.setText(QCoreApplication.translate("Form", u"\u0417\u0410\u0420\u0415\u0413\u0418\u0421\u0422\u0420\u0418\u0420\u0423\u0419\u0421\u042f \u0418 \u041f\u041e\u041b\u0423\u0427\u0418 \u0411\u041e\u041d\u0423\u0421!", None))
        self.Email.setText(QCoreApplication.translate("Form", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.Password.setText(QCoreApplication.translate("Form", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.Sign_up.setText(QCoreApplication.translate("Form", u"\u0417\u0410\u0420\u0415\u0413\u0418\u0421\u0422\u0420\u0418\u0420\u041e\u0412\u0410\u0422\u042c\u0421\u042f", None))
        self.Chips.setText("")
    # retranslateUi

