# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from custom_widgets import CustomQListWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(703, 492)
        font = QFont()
        font.setPointSize(13)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.lineEditSearch = QLineEdit(self.frame)
        self.lineEditSearch.setObjectName(u"lineEditSearch")

        self.verticalLayout.addWidget(self.lineEditSearch)

        self.listWidget = CustomQListWidget(self.frame)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setFont(font)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragDropOverwriteMode(False)
        self.listWidget.setDragDropMode(QAbstractItemView.DragDrop)

        self.verticalLayout.addWidget(self.listWidget)


        self.horizontalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.lineEditName = QLineEdit(self.frame_2)
        self.lineEditName.setObjectName(u"lineEditName")

        self.verticalLayout_2.addWidget(self.lineEditName)

        self.textEditPath = QTextEdit(self.frame_2)
        self.textEditPath.setObjectName(u"textEditPath")

        self.verticalLayout_2.addWidget(self.textEditPath)

        self.textEditComment = QTextEdit(self.frame_2)
        self.textEditComment.setObjectName(u"textEditComment")

        self.verticalLayout_2.addWidget(self.textEditComment)


        self.horizontalLayout.addWidget(self.frame_2)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 5)
        self.addButton = QPushButton(self.frame_3)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout_2.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.frame_3)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout_2.addWidget(self.deleteButton)

        self.moveFirstButton = QPushButton(self.frame_3)
        self.moveFirstButton.setObjectName(u"moveFirstButton")

        self.horizontalLayout_2.addWidget(self.moveFirstButton)

        self.moveUpButton = QPushButton(self.frame_3)
        self.moveUpButton.setObjectName(u"moveUpButton")

        self.horizontalLayout_2.addWidget(self.moveUpButton)

        self.moveDownButton = QPushButton(self.frame_3)
        self.moveDownButton.setObjectName(u"moveDownButton")

        self.horizontalLayout_2.addWidget(self.moveDownButton)

        self.moveLastButton = QPushButton(self.frame_3)
        self.moveLastButton.setObjectName(u"moveLastButton")

        self.horizontalLayout_2.addWidget(self.moveLastButton)

        self.freshButton = QPushButton(self.frame_3)
        self.freshButton.setObjectName(u"freshButton")

        self.horizontalLayout_2.addWidget(self.freshButton)

        self.saveButton = QPushButton(self.frame_3)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_2.addWidget(self.saveButton)


        self.verticalLayout_3.addWidget(self.frame_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 703, 29))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8def\u5f84\u7ba1\u7406\u5de5\u5177", None))
        self.lineEditSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u540d\u79f0", None))
        self.textEditPath.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8def\u5f84", None))
        self.textEditComment.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u5907\u6ce8", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.moveFirstButton.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u5230\u6700\u524d", None))
        self.moveUpButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u79fb", None))
        self.moveDownButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u79fb", None))
        self.moveLastButton.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u5230\u6700\u540e", None))
        self.freshButton.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
    # retranslateUi

