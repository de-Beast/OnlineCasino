# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GamebHPfay.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

class Ui_Game(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(839, 552)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Manrope"])
        font.setBold(True)
        Form.setFont(font)
        Form.setStyleSheet(u"background: rgba(255, 241, 191, 1);\n"
"padding: 0px;\n"
"margin: 0px;")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.backButton = QPushButton(Form)
        self.backButton.setObjectName(u"backButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy1)
        self.backButton.setMinimumSize(QSize(120, 0))
        font1 = QFont()
        font1.setFamilies([u"Manrope"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.backButton.setFont(font1)
        self.backButton.setStyleSheet(u"background-color: rgba(140, 101, 65, 0.6);\n"
"border-radius: 13px;")

        self.horizontalLayout_2.addWidget(self.backButton)

        self.balanceLabel = QLabel(Form)
        self.balanceLabel.setObjectName(u"balanceLabel")
        self.balanceLabel.setFont(font1)
        self.balanceLabel.setStyleSheet(u"background: radial-gradient(50% 50% at 50% 50%, rgba(244, 216, 116, 0.63) 60.42%, rgba(244, 216, 116, 0) 100%);\n"
"text-align: center;")
        self.balanceLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout_2.addWidget(self.balanceLabel)

        self.accountButton = QPushButton(Form)
        self.accountButton.setObjectName(u"accountButton")
        sizePolicy1.setHeightForWidth(self.accountButton.sizePolicy().hasHeightForWidth())
        self.accountButton.setSizePolicy(sizePolicy1)
        self.accountButton.setMinimumSize(QSize(120, 0))
        self.accountButton.setFont(font1)
        self.accountButton.setStyleSheet(u"border-radius: 25px;\n"
"background-color: rgba(140, 101, 65, 0.6)\n"
"")

        self.horizontalLayout_2.addWidget(self.accountButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 0))
        font2 = QFont()
        font2.setFamilies([u"Manrope"])
        font2.setPointSize(14)
        font2.setBold(False)
        self.widget.setFont(font2)
        self.widget.setStyleSheet(u"background: rgba(248, 224, 140, 1);\n"
"border-radius: 20px;")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.circle = QLabel(self.widget)
        self.circle.setObjectName(u"circle")
        self.circle.setMaximumSize(QSize(300, 300))
        self.circle.setStyleSheet(u"border-radius: 100px;")

        self.horizontalLayout_3.addWidget(self.circle)

        self.tools = QWidget(self.widget)
        self.tools.setObjectName(u"tools")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tools.sizePolicy().hasHeightForWidth())
        self.tools.setSizePolicy(sizePolicy2)
        self.verticalLayout_7 = QVBoxLayout(self.tools)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.betEdit = QTextEdit(self.tools)
        self.betEdit.setObjectName(u"betEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.betEdit.sizePolicy().hasHeightForWidth())
        self.betEdit.setSizePolicy(sizePolicy3)
        self.betEdit.setMaximumSize(QSize(16777215, 40))
        font3 = QFont()
        font3.setFamilies([u"Manrope"])
        font3.setPointSize(12)
        font3.setBold(True)
        self.betEdit.setFont(font3)
        self.betEdit.setStyleSheet(u"background: rgba(255, 241, 191, 1);\n"
"border-radius: 10px;")

        self.verticalLayout_7.addWidget(self.betEdit)

        self.label_2 = QLabel(self.tools)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"padding-left: 9px;")

        self.verticalLayout_7.addWidget(self.label_2)

        self.betButtonsContainer = QWidget(self.tools)
        self.betButtonsContainer.setObjectName(u"betButtonsContainer")
        font4 = QFont()
        font4.setPointSize(14)
        self.betButtonsContainer.setFont(font4)
        self.horizontalLayout_5 = QHBoxLayout(self.betButtonsContainer)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.redBetButton = QPushButton(self.betButtonsContainer)
        self.redBetButton.setObjectName(u"redBetButton")
        self.redBetButton.setFont(font1)
        self.redBetButton.setStyleSheet(u"border-radius: 5px;\n"
"background: rgba(217, 73, 73, 1);\n"
"color: rgba(255, 241, 191, 1);\n"
"")

        self.horizontalLayout_5.addWidget(self.redBetButton)

        self.blackBetButton = QPushButton(self.betButtonsContainer)
        self.blackBetButton.setObjectName(u"blackBetButton")
        self.blackBetButton.setFont(font1)
        self.blackBetButton.setStyleSheet(u"background: rgba(0, 0, 0, 1);\n"
"border-radius: 5px;\n"
"color: rgba(255, 241, 191, 1);\n"
"")

        self.horizontalLayout_5.addWidget(self.blackBetButton)

        self.greenBetButton = QPushButton(self.betButtonsContainer)
        self.greenBetButton.setObjectName(u"greenBetButton")
        self.greenBetButton.setFont(font1)
        self.greenBetButton.setStyleSheet(u"background: rgba(87, 187, 52, 1);\n"
"border-radius: 5px;\n"
"color: rgba(255, 241, 191, 1);\n"
"")

        self.horizontalLayout_5.addWidget(self.greenBetButton)


        self.verticalLayout_7.addWidget(self.betButtonsContainer)

        self.label_3 = QLabel(self.tools)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"padding-left: 9px;")

        self.verticalLayout_7.addWidget(self.label_3)

        self.history = QListWidget(self.tools)
        self.history.setObjectName(u"history")
        sizePolicy2.setHeightForWidth(self.history.sizePolicy().hasHeightForWidth())
        self.history.setSizePolicy(sizePolicy2)

        self.verticalLayout_7.addWidget(self.history)


        self.horizontalLayout_3.addWidget(self.tools)


        self.verticalLayout_2.addWidget(self.widget)

        self.bets = QWidget(Form)
        self.bets.setObjectName(u"bets")
        self.horizontalLayout_4 = QHBoxLayout(self.bets)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.redBetContainer = QWidget(self.bets)
        self.redBetContainer.setObjectName(u"redBetContainer")
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setBold(False)
        font5.setKerning(True)
        self.redBetContainer.setFont(font5)
        self.redBetContainer.setAutoFillBackground(False)
        self.redBetContainer.setStyleSheet(u"background: rgba(217, 73, 73, 1);\n"
"border-radius: 26px;\n"
"layoutMargins: 0px;")
        self.verticalLayout_4 = QVBoxLayout(self.redBetContainer)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 13, 0, 0)
        self.widget_4 = QWidget(self.redBetContainer)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setStyleSheet(u"background: rgba(248, 224, 140, 1);")
        self.verticalLayout_8 = QVBoxLayout(self.widget_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.redBetsSum = QLabel(self.widget_4)
        self.redBetsSum.setObjectName(u"redBetsSum")
        font6 = QFont()
        font6.setFamilies([u"Manrope"])
        font6.setPointSize(10)
        font6.setBold(True)
        self.redBetsSum.setFont(font6)
        self.redBetsSum.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.redBetsSum)

        self.redBets = QTextBrowser(self.widget_4)
        self.redBets.setObjectName(u"redBets")

        self.verticalLayout_8.addWidget(self.redBets)


        self.verticalLayout_4.addWidget(self.widget_4)


        self.horizontalLayout_4.addWidget(self.redBetContainer)

        self.blackBetContainer = QWidget(self.bets)
        self.blackBetContainer.setObjectName(u"blackBetContainer")
        self.blackBetContainer.setStyleSheet(u"background: rgba(41, 20, 4, 1);\n"
"border-radius: 26px;")
        self.verticalLayout_5 = QVBoxLayout(self.blackBetContainer)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 13, 0, 0)
        self.widget_5 = QWidget(self.blackBetContainer)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setFont(font6)
        self.widget_5.setStyleSheet(u"background: rgba(248, 224, 140, 1);\n"
"")
        self.verticalLayout_9 = QVBoxLayout(self.widget_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.blackBetsSum = QLabel(self.widget_5)
        self.blackBetsSum.setObjectName(u"blackBetsSum")
        self.blackBetsSum.setFont(font6)

        self.verticalLayout_9.addWidget(self.blackBetsSum)

        self.blackBets = QTextBrowser(self.widget_5)
        self.blackBets.setObjectName(u"blackBets")

        self.verticalLayout_9.addWidget(self.blackBets)


        self.verticalLayout_5.addWidget(self.widget_5)


        self.horizontalLayout_4.addWidget(self.blackBetContainer)

        self.greenBetContainer = QWidget(self.bets)
        self.greenBetContainer.setObjectName(u"greenBetContainer")
        self.greenBetContainer.setStyleSheet(u"background: rgba(87, 187, 52, 1);\n"
"border-radius: 26px;")
        self.verticalLayout_6 = QVBoxLayout(self.greenBetContainer)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 13, 0, 0)
        self.widget_6 = QWidget(self.greenBetContainer)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setStyleSheet(u"background: rgba(248, 224, 140, 1);\n"
"")
        self.verticalLayout_10 = QVBoxLayout(self.widget_6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.greenBetsSum = QLabel(self.widget_6)
        self.greenBetsSum.setObjectName(u"greenBetsSum")
        self.greenBetsSum.setFont(font6)

        self.verticalLayout_10.addWidget(self.greenBetsSum)

        self.greenBets = QTextBrowser(self.widget_6)
        self.greenBets.setObjectName(u"greenBets")

        self.verticalLayout_10.addWidget(self.greenBets)


        self.verticalLayout_6.addWidget(self.widget_6)


        self.horizontalLayout_4.addWidget(self.greenBetContainer)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 2)
        self.horizontalLayout_4.setStretch(2, 2)

        self.verticalLayout_2.addWidget(self.bets)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy4)
        self.widget_3.setMinimumSize(QSize(200, 0))
        self.widget_3.setMaximumSize(QSize(300, 16777215))
        self.widget_3.setStyleSheet(u"background: rgba(244, 216, 116, 1);\n"
"border-radius: 26px;")
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.chat = QTextBrowser(self.widget_3)
        self.chat.setObjectName(u"chat")

        self.verticalLayout_3.addWidget(self.chat)

        self.messageEdit = QLineEdit(self.widget_3)
        self.messageEdit.setObjectName(u"messageEdit")
        self.messageEdit.setMinimumSize(QSize(0, 30))
        self.messageEdit.setStyleSheet(u"background: rgba(255, 241, 191, 1);\n"
"border-radius: 15px;")

        self.verticalLayout_3.addWidget(self.messageEdit)


        self.horizontalLayout.addWidget(self.widget_3)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.backButton.setText(QCoreApplication.translate("Form", u"\u041d\u0410\u0417\u0410\u0414", None))
        self.balanceLabel.setText(QCoreApplication.translate("Form", u"\u0411\u0410\u041b\u0410\u041d\u0421", None))
        self.accountButton.setText(QCoreApplication.translate("Form", u"\u041b\u0418\u0427\u041d\u042b\u0419\n"
"\u041a\u0410\u0411\u0418\u041d\u0415\u0422", None))
        self.circle.setText(QCoreApplication.translate("Form", u"Circle", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u0421\u0414\u0415\u041b\u0410\u0422\u042c \u0421\u0422\u0410\u0412\u041a\u0423", None))
        self.redBetButton.setText(QCoreApplication.translate("Form", u"\u0416\u041c\u0418", None))
        self.blackBetButton.setText(QCoreApplication.translate("Form", u"\u0416\u041c\u0418", None))
        self.greenBetButton.setText(QCoreApplication.translate("Form", u"\u0416\u041c\u0418", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u0418\u0421\u0422\u041e\u0420\u0418\u042f \u0412\u042b\u041f\u0410\u0414\u0415\u041d\u0418\u0419", None))
        self.redBetsSum.setText(QCoreApplication.translate("Form", u"\u041e\u0411\u0429\u0410\u042f \u0421\u0422\u0410\u0412\u041a\u0410", None))
        self.blackBetsSum.setText(QCoreApplication.translate("Form", u"\u041e\u0411\u0429\u0410\u042f \u0421\u0422\u0410\u0412\u041a\u0410", None))
        self.greenBetsSum.setText(QCoreApplication.translate("Form", u"\u041e\u0411\u0429\u0410\u042f \u0421\u0422\u0410\u0412\u041a\u0410", None))
    # retranslateUi

