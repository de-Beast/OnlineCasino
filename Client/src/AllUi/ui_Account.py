# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AccountiprcaD.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Account(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(633, 463)
        font = QFont()
        font.setFamilies([u"Manrope"])
        font.setPointSize(15)
        font.setBold(True)
        Form.setFont(font)
        Form.setLayoutDirection(Qt.LeftToRight)
        Form.setStyleSheet(u"text_align: center;\n"
"background: rgba(255, 241, 191, 1);\n"
"")
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(u"background: rgba(140, 101, 65, 0.7);\n"
"border-radius: 10px;\n"
"padding: 5px")

        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

        self.emailEdit = QLineEdit(Form)
        self.emailEdit.setObjectName(u"emailEdit")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(False)
        self.emailEdit.setFont(font1)
        self.emailEdit.setStyleSheet(u"background: rgba(244, 216, 116, 1);\n"
"border-radius: 10px;\n"
"padding: 3px")
        self.emailEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.emailEdit, 1, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Manrope"])
        font2.setPointSize(20)
        font2.setBold(True)
        self.label_6.setFont(font2)
        self.label_6.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)

        self.balanceLabel = QLabel(Form)
        self.balanceLabel.setObjectName(u"balanceLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.balanceLabel.sizePolicy().hasHeightForWidth())
        self.balanceLabel.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(15)
        font3.setBold(True)
        self.balanceLabel.setFont(font3)
        self.balanceLabel.setLayoutDirection(Qt.LeftToRight)
        self.balanceLabel.setStyleSheet(u"background: rgba(244, 216, 116, 1);\n"
"border-radius: 10px;\n"
"padding: 3px")
        self.balanceLabel.setScaledContents(False)
        self.balanceLabel.setWordWrap(False)

        self.gridLayout.addWidget(self.balanceLabel, 2, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u041d\u0410\u0417\u0410\u0414", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u041b\u0438\u0447\u043d\u044b\u0439 \u043a\u0430\u0431\u0438\u043d\u0435\u0442", None))
        self.balanceLabel.setText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"\u0411\u0430\u043b\u0430\u043d\u0441", None))
    # retranslateUi

