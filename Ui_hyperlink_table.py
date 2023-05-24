# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\python_projects\PyQt5\47)Shortcut_App\hyperlink_table.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_hyperlink_window(object):
    def setupUi(self, hyperlink_window):
        hyperlink_window.setObjectName("hyperlink_window")
        hyperlink_window.resize(602, 326)
        hyperlink_window.setStyleSheet("background-color: rgb(248, 249, 238);")
        self.centralwidget = QtWidgets.QWidget(hyperlink_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.hyperlink_tabpage = QtWidgets.QTabWidget(self.centralwidget)
        self.hyperlink_tabpage.setStyleSheet("background-color: rgb(56, 76, 101);\n"
"color: rgb(248, 249, 238);")
        self.hyperlink_tabpage.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.hyperlink_tabpage.setElideMode(QtCore.Qt.ElideNone)
        self.hyperlink_tabpage.setDocumentMode(False)
        self.hyperlink_tabpage.setTabsClosable(False)
        self.hyperlink_tabpage.setTabBarAutoHide(False)
        self.hyperlink_tabpage.setObjectName("hyperlink_tabpage")
        self.gridLayout.addWidget(self.hyperlink_tabpage, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, 5)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("background-color: rgb(177, 196, 192);\n"
"color: rgb(255, 255, 255);\n"
"font: 700 10pt \"Microsoft JhengHei UI\";\n"
"padding: 3px")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.open_link_setting_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_link_setting_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.open_link_setting_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.open_link_setting_btn.setStyleSheet("background-color: rgb(165, 147, 135);\n"
"color: rgb(255, 255, 255);")
        self.open_link_setting_btn.setText("")
        self.open_link_setting_btn.setObjectName("open_link_setting_btn")
        self.horizontalLayout.addWidget(self.open_link_setting_btn)
        self.new_data_btn = QtWidgets.QPushButton(self.centralwidget)
        self.new_data_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.new_data_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.new_data_btn.setStyleSheet("background-color: rgb(165, 147, 135);\n"
"color: rgb(255, 255, 255);")
        self.new_data_btn.setText("")
        self.new_data_btn.setObjectName("new_data_btn")
        self.horizontalLayout.addWidget(self.new_data_btn)
        self.save_table_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_table_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.save_table_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.save_table_btn.setStyleSheet("background-color: rgb(165, 147, 135);\n"
"color: rgb(255, 255, 255);")
        self.save_table_btn.setText("")
        self.save_table_btn.setObjectName("save_table_btn")
        self.horizontalLayout.addWidget(self.save_table_btn)
        self.reload_table_btn = QtWidgets.QPushButton(self.centralwidget)
        self.reload_table_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.reload_table_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.reload_table_btn.setStyleSheet("background-color: rgb(165, 147, 135);\n"
"color: rgb(255, 255, 255);")
        self.reload_table_btn.setText("")
        self.reload_table_btn.setObjectName("reload_table_btn")
        self.horizontalLayout.addWidget(self.reload_table_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        hyperlink_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(hyperlink_window)
        self.hyperlink_tabpage.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(hyperlink_window)

    def retranslateUi(self, hyperlink_window):
        _translate = QtCore.QCoreApplication.translate
        hyperlink_window.setWindowTitle(_translate("hyperlink_window", "MainWindow"))
        self.label.setText(_translate("hyperlink_window", "1. Page右鍵可刪除\n"
"2. Table右鍵可「開啟連結」、「加入/取消我的最愛」、「刪除」"))
        self.open_link_setting_btn.setToolTip(_translate("hyperlink_window", "開啟設定檔"))
        self.new_data_btn.setToolTip(_translate("hyperlink_window", "新增連結"))
        self.save_table_btn.setToolTip(_translate("hyperlink_window", "存檔"))
        self.reload_table_btn.setToolTip(_translate("hyperlink_window", "重新整理"))