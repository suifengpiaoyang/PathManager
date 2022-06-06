# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigForm(object):
    def setupUi(self, ConfigForm):
        if not ConfigForm.objectName():
            ConfigForm.setObjectName(u"ConfigForm")
        ConfigForm.resize(622, 378)
        font = QFont()
        font.setPointSize(10)
        ConfigForm.setFont(font)
        self.verticalLayout = QVBoxLayout(ConfigForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(ConfigForm)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(115, 25))

        self.horizontalLayout.addWidget(self.pushButton)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit.setMinimumSize(QSize(0, 25))

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 262, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButtonConfirm = QPushButton(ConfigForm)
        self.pushButtonConfirm.setObjectName(u"pushButtonConfirm")

        self.horizontalLayout_2.addWidget(self.pushButtonConfirm)

        self.pushButtonCancel = QPushButton(ConfigForm)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout_2.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ConfigForm)

        QMetaObject.connectSlotsByName(ConfigForm)
    # setupUi

    def retranslateUi(self, ConfigForm):
        ConfigForm.setWindowTitle(QCoreApplication.translate("ConfigForm", u"\u914d\u7f6e", None))
        self.groupBox.setTitle(QCoreApplication.translate("ConfigForm", u"Sublime Text \u914d\u7f6e", None))
        self.pushButton.setText(QCoreApplication.translate("ConfigForm", u"\u9009\u62e9\u7a0b\u5e8f\u4f4d\u7f6e", None))
        self.pushButtonConfirm.setText(QCoreApplication.translate("ConfigForm", u"\u786e\u5b9a", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("ConfigForm", u"\u53d6\u6d88", None))
    # retranslateUi

