from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(320, 10, 75, 30))
        self.exit_button.setObjectName("exit_button")
        self.help_button = QtWidgets.QPushButton(self.centralwidget)
        self.help_button.setGeometry(QtCore.QRect(240, 10, 75, 30))
        self.help_button.setObjectName("help_button")
        self.setting_button = QtWidgets.QPushButton(self.centralwidget)
        self.setting_button.setGeometry(QtCore.QRect(160, 10, 75, 30))
        self.setting_button.setObjectName("setting_button")
        self.repo_label = QtWidgets.QLabel(self.centralwidget)
        self.repo_label.setGeometry(QtCore.QRect(50, 580, 301, 16))
        self.repo_label.setObjectName("repo_label")
        self.ver_label = QtWidgets.QLabel(self.centralwidget)
        self.ver_label.setGeometry(QtCore.QRect(120, 560, 161, 20))
        self.ver_label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ver_label.setObjectName("ver_label")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(140, 60, 128, 128))
        self.graphicsView.setObjectName("graphicsView")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 320, 231, 30))
        self.plainTextEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.go_button = QtWidgets.QPushButton(self.centralwidget)
        self.go_button.setGeometry(QtCore.QRect(290, 320, 75, 30))
        self.go_button.setObjectName("go_button")
        self.ver_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.ver_label_2.setGeometry(QtCore.QRect(110, 280, 191, 20))
        self.ver_label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ver_label_2.setObjectName("ver_label_2")
        self.setting_button.raise_()
        self.exit_button.raise_()
        self.help_button.raise_()
        self.repo_label.raise_()
        self.ver_label.raise_()
        self.graphicsView.raise_()
        self.plainTextEdit.raise_()
        self.go_button.raise_()
        self.ver_label_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.exit_button.setText(_translate("MainWindow", "退出"))
        self.help_button.setText(_translate("MainWindow", "帮助"))
        self.setting_button.setText(_translate("MainWindow", "配置"))
        self.repo_label.setText(_translate(
            "MainWindow", "AstroGen - https://github.com/FiresJoeng/AstraGen"))
        self.ver_label.setText(_translate(
            "MainWindow", "Current Version: Demo 1.0"))
        self.plainTextEdit.setPlainText(
            _translate("MainWindow", "请输入企业关键词..."))
        self.go_button.setText(_translate("MainWindow", "生成报告"))
        self.ver_label_2.setText(_translate(
            "MainWindow", "Enter the keyword of enterprise."))
