import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QLineEdit, QMessageBox, QDesktopWidget
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt


# 初始化全局 QApplication 对象并设置应用字体
app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("[Error] 加载自定义字体失败！")
    font_family = "Arial"


# 定义自定义消息框类，用于显示错误信息
class CustomMsgBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white; color: black;")
        self.setStandardButtons(QMessageBox.Close)
        self.button(QMessageBox.Close).setText("好的")
        self.button(QMessageBox.Close).setStyleSheet(
            "min-width: 60px; border: 1px solid gray; border-radius: 1px;"
        )

    # 窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = None


# 定义自定义输入框类，实现焦点和鼠标事件下的样式切换
class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.placeholder = placeholder
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            color: grey;
            border: 2px solid #d9d9d9;
            background-color: white;
            border-radius: 5px;
        """)

    def focusInEvent(self, event):
        self.setStyleSheet("""
            color: black;
            border: 2px solid #0077ED;
            background-color: white;
            border-radius: 5px;
        """)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if not self.text():
            self.setStyleSheet("""
                color: grey;
                border: 2px solid #d9d9d9;
                background-color: white;
                border-radius: 5px;
            """)
        else:
            self.setStyleSheet("""
                color: black;
                border: 2px solid #d9d9d9;
                background-color: white;
                border-radius: 5px;
            """)
        super().focusOutEvent(event)

    def enterEvent(self, event):
        if not self.hasFocus():
            self.setStyleSheet("""
                color: grey;
                border: 2px solid black;
                background-color: #f9f9f9;
                border-radius: 5px;
            """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.hasFocus():
            if not self.text():
                self.setStyleSheet("""
                    color: grey;
                    border: 2px solid #d9d9d9;
                    background-color: white;
                    border-radius: 5px;
                """)
            else:
                self.setStyleSheet("""
                    color: black;
                    border: 2px solid #d9d9d9;
                    background-color: white;
                    border-radius: 5px;
                """)
        super().leaveEvent(event)


# 定义主窗口类，包含界面组件及交互逻辑
class UI(QWidget):
    def __init__(self):
        super().__init__()

        # 窗口基础设置：无边框、标题、固定尺寸、背景样式和透明度
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('AstraGen 星核')
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.75)
        self.center()
        self._offset = None

        # 添加欢迎标签并设置样式
        self.welcome_label = QLabel('欢迎使用 - AstraGen 星核', self)
        self.welcome_label.setFont(QFont(app.font().family(), 14))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.adjustSize()
        self.welcome_label.move(
            (self.width() - self.welcome_label.width()) // 2, 35)

        # 添加退出按钮并绑定退出事件
        self.exit_button = QPushButton('×', self)
        self.exit_button.setGeometry(350, 10, 30, 25)
        self.exit_button.setStyleSheet("""
            background-color: transparent;
            color: white;
            border: none;
        """)
        self.exit_button.clicked.connect(QApplication.instance().quit)

        # 添加 API KEY 输入框
        self.search_entry = CustomLineEdit('请输入DeepSeek的API KEY', self)
        self.search_entry.setGeometry(50, 85, 200, 30)

        # 添加确认按钮并绑定搜索事件
        self.search_button = QPushButton('确认', self)
        self.search_button.setGeometry(270, 85, 80, 30)
        self.search_button.setStyleSheet("""
            background-color: #0077ED;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        self.search_button.clicked.connect(self.on_search)

    def center(self):
        """使窗口在屏幕上居中显示"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_search(self):
        """处理确认按钮点击事件，验证 API KEY 输入"""
        api_key = self.search_entry.text()
        if not api_key.strip():
            msg = CustomMsgBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error!")
            msg.setText("非法的输入内容!")
            msg.show()
        else:
            print(f"API KEY: {api_key}")

    # 窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = None


# 程序入口：创建并显示主窗口，启动应用事件循环
if __name__ == '__main__':
    window = UI()
    window.show()
    sys.exit(app.exec_())
