# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(812, 600)
        MainWindow.setToolTip("")
        MainWindow.setToolTipDuration(-1)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_border = QtWidgets.QWidget(self.centralwidget)
        self.button_border.setStyleSheet("#button_border {\n"
"        border-radius: 4px;\n"
"            border: 0.5px solid rgb(180, 180, 180);\n"
"    }")
        self.button_border.setObjectName("button_border")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.button_border)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openFileButton = QtWidgets.QPushButton(self.button_border)
        self.openFileButton.setToolTipDuration(1500)
        self.openFileButton.setStyleSheet("#openFileButton {\n"
"            background-color: white; \n"
"        border: 0.5px solid rgb(180, 180, 180);\n"
"            color: black;\n"
"        border-radius: 4px\n"
"    }\n"
"#openFileButton:hover { \n"
"        background-color: lightgray; \n"
"    }\n"
"#openFileButton:pressed{\n"
"        background-color:gray;\n"
"    }")
        self.openFileButton.setObjectName("openFileButton")
        self.verticalLayout.addWidget(self.openFileButton)
        self.graph_show_button = QtWidgets.QPushButton(self.button_border)
        self.graph_show_button.setToolTipDuration(1500)
        self.graph_show_button.setStyleSheet("#graph_show_button { \n"
"        background-color: white; \n"
"        border: 0.5px solid rgb(180, 180, 180);\n"
"            color: black;\n"
"        border-radius: 4px;\n"
"    }\n"
"#graph_show_button:hover { \n"
"        background-color: lightgray;\n"
"    }\n"
"#graph_show_button:pressed {\n"
"        background-color: gray;\n"
"    }")
        self.graph_show_button.setObjectName("graph_show_button")
        self.verticalLayout.addWidget(self.graph_show_button)
        self.graph_show_neighbors_button = QtWidgets.QPushButton(self.button_border)
        self.graph_show_neighbors_button.setToolTipDuration(1500)
        self.graph_show_neighbors_button.setStyleSheet("#graph_show_neighbors_button { \n"
"            background-color: white; \n"
"        border: 0.5px solid rgb(180, 180, 180);\n"
"            color: black;\n"
"        border-radius: 4px\n"
"    }\n"
"#graph_show_neighbors_button:hover { \n"
"        background-color: lightgray;\n"
"    }\n"
"#graph_show_neighbors_button:pressed{\n"
"        background-color: gray;\n"
"}")
        self.graph_show_neighbors_button.setObjectName("graph_show_neighbors_button")
        self.verticalLayout.addWidget(self.graph_show_neighbors_button)
        self.dijkstra_button = QtWidgets.QPushButton(self.button_border)
        self.dijkstra_button.setToolTipDuration(1500)
        self.dijkstra_button.setStyleSheet("#dijkstra_button { \n"
"        background-color: white; \n"
"        border: 0.5px solid rgb(180, 180, 180);\n"
"            color: black;\n"
"        border-radius: 4px\n"
"    }\n"
"#dijkstra_button:hover { \n"
"        background-color: lightgray; \n"
"    }\n"
"#dijkstra_button:pressed {\n"
"        background-color: gray;\n"
"}")
        self.dijkstra_button.setObjectName("dijkstra_button")
        self.verticalLayout.addWidget(self.dijkstra_button)
        self.dfs_button = QtWidgets.QPushButton(self.button_border)
        self.dfs_button.setToolTipDuration(1500)
        self.dfs_button.setStyleSheet("#dfs_button { \n"
"        background-color: white; \n"
"        border: 0.5px solid rgb(180, 180, 180);\n"
"            color: black;\n"
"        border-radius: 4px\n"
"    }\n"
"#dfs_button:hover { \n"
"        background-color: lightgray; \n"
"    }\n"
"#dfs_button:pressed {\n"
"        background-color: gray;\n"
"}")
        self.dfs_button.setObjectName("dfs_button")
        self.verticalLayout.addWidget(self.dfs_button)
        self.bfs_button = QtWidgets.QPushButton(self.button_border)
        self.bfs_button.setToolTipDuration(1500)
        self.bfs_button.setStyleSheet("#bfs_button { \n"
"        background-color: white; \n"
"        border: 0.5px solid rgb(180, 180, 180);\n"
"            color: black;\n"
"        border-radius: 4px\n"
"    }\n"
"#bfs_button:hover { \n"
"        background-color: lightgray; \n"
"    }\n"
"#bfs_button:pressed {\n"
"        background-color: gray;\n"
"}")
        self.bfs_button.setObjectName("bfs_button")
        self.verticalLayout.addWidget(self.bfs_button)
        self.horizontalLayout.addWidget(self.button_border)
        self.mplwidget_border = QtWidgets.QWidget(self.centralwidget)
        self.mplwidget_border.setStyleSheet("#mplwidget_border {\n"
"        border-radius: 4px;\n"
"            border: 0.5px solid rgb(180, 180, 180);\n"
"    }")
        self.mplwidget_border.setObjectName("mplwidget_border")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.mplwidget_border)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.overall_view_button = QtWidgets.QPushButton(self.mplwidget_border)
        self.overall_view_button.setStyleSheet("#overall_view_button {\n"
"            background-color: white; \n"
"        border: 0.5px solid rgb(180, 180, 180);\n"
"            color: black;\n"
"        border-radius: 4px\n"
"    }\n"
"#overall_view_button:hover { \n"
"        background-color: lightgray; \n"
"    }\n"
"#overall_view_button:pressed{\n"
"        background-color:gray;\n"
"    }")
        self.overall_view_button.setObjectName("overall_view_button")
        self.verticalLayout_4.addWidget(self.overall_view_button)
        self.mplwidget = MPLWidget(self.mplwidget_border)
        self.mplwidget.setStyleSheet("QWidget, QLabel {\n"
"        border-radius: 4px;\n"
"            border: 0.5px solid rgb(180, 180, 180);\n"
"    }")
        self.mplwidget.setObjectName("mplwidget")
        self.verticalLayout_4.addWidget(self.mplwidget)
        self.horizontalLayout.addWidget(self.mplwidget_border)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.info_board_border = QtWidgets.QWidget(self.centralwidget)
        self.info_board_border.setStyleSheet("#info_board_border {\n"
"        border-radius: 4px;\n"
"            border: 0.5px solid rgb(180, 180, 180);\n"
"    }")
        self.info_board_border.setObjectName("info_board_border")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.info_board_border)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.info_board = QtWidgets.QTextEdit(self.info_board_border)
        self.info_board.setStyleSheet("#info_board { \n"
"        border: none;\n"
"}\n"
"")
        self.info_board.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.info_board.setReadOnly(True)
        self.info_board.setObjectName("info_board")
        self.horizontalLayout_2.addWidget(self.info_board)
        self.verticalLayout_2.addWidget(self.info_board_border)
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setAutoFillBackground(False)
        self.progress_bar.setStyleSheet("")
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout_2.addWidget(self.progress_bar)
        self.verticalLayout_2.setStretch(0, 7)
        self.verticalLayout_2.setStretch(1, 4)
        self.verticalLayout_2.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 36))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openFileButton.setToolTip(_translate("MainWindow", "点击以打开文件"))
        self.openFileButton.setText(_translate("MainWindow", "打开文件"))
        self.graph_show_button.setToolTip(_translate("MainWindow", "点击以显示图形"))
        self.graph_show_button.setText(_translate("MainWindow", "显示图形"))
        self.graph_show_neighbors_button.setToolTip(_translate("MainWindow", "输入一个点，显示该点的第一、第二邻接点"))
        self.graph_show_neighbors_button.setText(_translate("MainWindow", "显示邻接点"))
        self.dijkstra_button.setToolTip(_translate("MainWindow", "输入两个点，计算并显示两点的测地距离和具体路径"))
        self.dijkstra_button.setText(_translate("MainWindow", "计算测地距离"))
        self.dfs_button.setToolTip(_translate("MainWindow", "选择一个点并以深度优先绘制图形"))
        self.dfs_button.setText(_translate("MainWindow", "DFS"))
        self.bfs_button.setToolTip(_translate("MainWindow", "选择一个点并以宽度优先绘制图形"))
        self.bfs_button.setText(_translate("MainWindow", "BFS"))
        self.overall_view_button.setText(_translate("MainWindow", "点击恢复全局视角"))
        self.progress_bar.setFormat(_translate("MainWindow", "%v/%m"))
from UI.mplwidget import MPLWidget

