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
from custom_widgets import CustomQTextEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(541, 402)
        font = QFont()
        font.setPointSize(13)
        MainWindow.setFont(font)
        self.configAction = QAction(MainWindow)
        self.configAction.setObjectName(u"configAction")
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
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEditName = QLineEdit(self.frame_2)
        self.lineEditName.setObjectName(u"lineEditName")

        self.verticalLayout_2.addWidget(self.lineEditName)

        self.textEditPath = CustomQTextEdit(self.frame_2)
        self.textEditPath.setObjectName(u"textEditPath")

        self.verticalLayout_2.addWidget(self.textEditPath)

        self.textEditComment = CustomQTextEdit(self.frame_2)
        self.textEditComment.setObjectName(u"textEditComment")

        self.verticalLayout_2.addWidget(self.textEditComment)


        self.horizontalLayout.addWidget(self.frame_2)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        font1 = QFont()
        font1.setPointSize(12)
        self.frame_3.setFont(font1)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 5)
        self.addButton = QPushButton(self.frame_3)
        self.addButton.setObjectName(u"addButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.frame_3)
        self.deleteButton.setObjectName(u"deleteButton")
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.deleteButton)

        self.moveFirstButton = QPushButton(self.frame_3)
        self.moveFirstButton.setObjectName(u"moveFirstButton")
        sizePolicy.setHeightForWidth(self.moveFirstButton.sizePolicy().hasHeightForWidth())
        self.moveFirstButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.moveFirstButton)

        self.moveLastButton = QPushButton(self.frame_3)
        self.moveLastButton.setObjectName(u"moveLastButton")
        sizePolicy.setHeightForWidth(self.moveLastButton.sizePolicy().hasHeightForWidth())
        self.moveLastButton.setSizePolicy(sizePolicy)
        self.moveLastButton.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.moveLastButton)

        self.freshButton = QPushButton(self.frame_3)
        self.freshButton.setObjectName(u"freshButton")
        sizePolicy.setHeightForWidth(self.freshButton.sizePolicy().hasHeightForWidth())
        self.freshButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.freshButton)

        self.saveButton = QPushButton(self.frame_3)
        self.saveButton.setObjectName(u"saveButton")
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.saveButton)


        self.verticalLayout_3.addWidget(self.frame_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 541, 26))
        font2 = QFont()
        font2.setPointSize(11)
        self.menubar.setFont(font2)
        self.menuConfig = QMenu(self.menubar)
        self.menuConfig.setObjectName(u"menuConfig")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuConfig.addAction(self.configAction)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8def\u5f84\u7ba1\u7406\u5de5\u5177", None))
        self.configAction.setText(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.configAction.setToolTip(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.lineEditSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
        self.lineEditName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u540d\u79f0", None))
        self.textEditPath.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8def\u5f84", None))
        self.textEditComment.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u5907\u6ce8", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.moveFirstButton.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u5230\u6700\u524d", None))
        self.moveLastButton.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u5230\u6700\u540e", None))
        self.freshButton.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.menuConfig.setTitle(QCoreApplication.translate("MainWindow", u"\u9996\u9009\u9879", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
    # retranslateUi

