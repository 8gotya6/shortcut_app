# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\python_projects\PyQt5\47)Shortcut_App\Shortcut_App.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_icon_window(object):
    def setupUi(self, icon_window):
        icon_window.setObjectName("icon_window")
        icon_window.resize(100, 100)
        icon_window.setMinimumSize(QtCore.QSize(0, 0))
        icon_window.setMaximumSize(QtCore.QSize(999, 999))
        icon_window.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon_window.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon_window.setWindowTitle("")
        icon_window.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(icon_window)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.menu_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu_btn.sizePolicy().hasHeightForWidth())
        self.menu_btn.setSizePolicy(sizePolicy)
        self.menu_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menu_btn.setStyleSheet("")
        self.menu_btn.setText("")
        self.menu_btn.setObjectName("menu_btn")
        self.gridLayout.addWidget(self.menu_btn, 0, 1, 1, 1)
        icon_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(icon_window)
        QtCore.QMetaObject.connectSlotsByName(icon_window)

    def retranslateUi(self, icon_window):
        pass