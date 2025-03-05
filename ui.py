import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize


# 初始化应用程序并加载自定义字体
app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("[Error] 加载自定义字体失败！")
    font_family = "Arial"


# 定义启动屏幕类，负责显示启动动画和进度条
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self._is_closing = False

        # 设置窗口为无边框且置顶，固定窗口大小
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 150)

        # 居中显示窗口
        self.center()

        # 设置背景颜色和透明度
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.75)

        # 初始化界面控件和启动动画
        self.init_ui()
        self.start_animation()

    def init_ui(self):
        # 创建显示启动文本的标签并居中显示
        self.label = QLabel("极速启动中...", self)
        self.label.setStyleSheet("color: white; font-size: 18px;")
        self.label.adjustSize()
        self.label.move((self.width() - self.label.width()) // 2, 50)

        # 创建进度条的容器，并设置边框样式
        self.progress_container = QWidget(self)
        self.progress_container.setGeometry(50, 100, 300, 20)
        self.progress_container.setStyleSheet(
            "border: 2px solid white; border-radius: 5px; background-color: transparent;"
        )

        # 在容器中创建进度条填充部分，初始宽度设为0
        self.progress_fill = QWidget(self.progress_container)
        self.progress_fill.setGeometry(2, 2, 0, 16)
        self.progress_fill.setStyleSheet(
            "background-color: #0077ED; border-radius: 3px;")

    def start_animation(self):
        # 为进度条填充部分设置宽度动画
        self.animation = QPropertyAnimation(self.progress_fill, b"size")
        self.animation.setDuration(800)
        self.animation.setStartValue(self.progress_fill.size())
        self.animation.setEndValue(QSize(296, 16))
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.finished.connect(self.on_animation_finished)
        self.animation.start()

    def center(self):
        # 将窗口居中显示在屏幕上
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_animation_finished(self):
        # 动画结束后淡出窗口并打开主界面
        center_point = self.frameGeometry().center()
        self.fade_and_close(callback=lambda: self.open_main(center_point))

    def open_main(self, center_point):
        # 初始化主界面并显示
        self.main_window = UI(center_point)
        self.main_window.show()

    def fade_and_close(self, callback=None):
        # 执行淡出动画，并在动画结束后关闭窗口
        self._is_closing = True
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(200)
        self.fade_animation.setStartValue(self.windowOpacity())
        self.fade_animation.setEndValue(0)
        if callback:
            self.fade_animation.finished.connect(callback)
        self.fade_animation.finished.connect(lambda: QWidget.close(self))
        self.fade_animation.start()

    def closeEvent(self, event):
        # 重写关闭事件，确保窗口淡出后再关闭
        if not self._is_closing:
            event.ignore()
            self.fade_and_close()
        else:
            event.accept()


# 自定义消息框类，支持拖动并更改默认按钮文本
class CustomMsgBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white; color: black;")
        self.setStandardButtons(QMessageBox.Close)
        self.button(QMessageBox.Close).setText("好的")
        self.button(QMessageBox.Close).setStyleSheet(
            "min-width: 60px; border: 1px solid gray; border-radius: 1px;"
        )

    def mousePressEvent(self, event):
        # 记录鼠标点击时的偏移位置，实现拖动效果
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        # 实现消息框拖动效果
        if hasattr(self, "_offset") and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        # 重置偏移量
        if event.button() == Qt.LeftButton:
            self._offset = None

    def showEvent(self, event):
        # 显示时将消息框居中于父窗口
        if self.parent():
            parent_geometry = self.parent().frameGeometry()
            self_geometry = self.frameGeometry()
            new_x = parent_geometry.center().x() - self_geometry.width() // 2
            new_y = parent_geometry.center().y() - self_geometry.height() // 2
            self.move(new_x, new_y)
        super().showEvent(event)


# 自定义文本输入框类，添加聚焦和悬停时的样式效果
class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.placeholder = placeholder

        # 设置占位符文本及初始样式
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(
            "color: grey; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
        )

    def focusInEvent(self, event):
        # 聚焦时更新样式，突出显示输入框
        self.setStyleSheet(
            "color: black; border: 2px solid #0077ED; background-color: white; border-radius: 5px;"
        )
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # 失焦时根据是否有输入更新样式
        if not self.text():
            self.setStyleSheet(
                "color: grey; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
            )
        else:
            self.setStyleSheet(
                "color: black; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
            )
        super().focusOutEvent(event)

    def enterEvent(self, event):
        # 鼠标进入时（非聚焦状态）更新样式
        if not self.hasFocus():
            self.setStyleSheet(
                "color: grey; border: 2px solid black; background-color: #f9f9f9; border-radius: 5px;"
            )
        super().enterEvent(event)

    def leaveEvent(self, event):
        # 鼠标离开时恢复原有样式
        if not self.hasFocus():
            if not self.text():
                self.setStyleSheet(
                    "color: grey; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
                )
            else:
                self.setStyleSheet(
                    "color: black; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
                )
        super().leaveEvent(event)


# 定义主界面类，负责整个应用的主要交互
class UI(QWidget):
    def __init__(self, center_point=None):
        super().__init__()
        self._is_closing = False

        # 设置窗口为无边框并固定大小，同时设置初始透明度为0（用于淡入效果）
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("AstraGen 星核")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)

        # 根据传入中心点或自动居中显示窗口
        if center_point:
            self.move(center_point.x() - self.width() // 2,
                      center_point.y() - self.height() // 2)
        else:
            self.center()

        self._offset = None

        # 创建欢迎标签，并设置字体、颜色和居中显示
        self.welcome_label = QLabel("欢迎使用 - AstraGen 星核", self)
        self.welcome_label.setFont(QFont(app.font().family(), 14))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.adjustSize()
        self.welcome_label.move(
            (self.width() - self.welcome_label.width()) // 2, 50)

        # 创建退出按钮，点击后关闭窗口
        self.exit_button = QPushButton("×", self)
        self.exit_button.setGeometry(350, 10, 30, 25)
        self.exit_button.setStyleSheet(
            "background-color: transparent; color: white; border: none;")
        self.exit_button.clicked.connect(self.close)

        # 创建API KEY输入框及对应的确认按钮
        self.search_entry = CustomLineEdit("请输入DeepSeek的API KEY", self)
        self.search_entry.setGeometry(50, 100, 200, 30)

        self.search_button = QPushButton("验证", self)
        self.search_button.setGeometry(270, 100, 80, 30)
        self.search_button.setStyleSheet(
            "background-color: #0077ED; color: white; border: none; border-radius: 5px;"
        )
        self.search_button.clicked.connect(self.on_search)

        # 启动窗口淡入动画，使窗口逐渐显现
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(0.75)
        self.fade_in_animation.start()

    def center(self):
        # 将主窗口居中显示在屏幕上
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_search(self):
        # 处理搜索按钮点击事件，验证API KEY输入
        api_key = self.search_entry.text()
        if not api_key.strip():
            msg = CustomMsgBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error!")
            msg.setText("非法的输入内容!")
            msg.show()
        else:
            print(f"API KEY: {api_key}")

    def mousePressEvent(self, event):
        # 记录鼠标点击位置偏移，实现窗口拖动
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        # 拖动窗口时更新窗口位置
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        # 释放鼠标后重置偏移量
        if event.button() == Qt.LeftButton:
            self._offset = None

    def fade_and_close(self, callback=None):
        # 执行淡出动画，并在动画结束后关闭窗口
        self._is_closing = True
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(200)
        self.fade_animation.setStartValue(self.windowOpacity())
        self.fade_animation.setEndValue(0)
        if callback:
            self.fade_animation.finished.connect(callback)
        self.fade_animation.finished.connect(lambda: QWidget.close(self))
        self.fade_animation.start()

    def closeEvent(self, event):
        # 重写关闭事件，淡出窗口后退出应用
        if not self._is_closing:
            event.ignore()
            self.fade_and_close(
                callback=lambda: QApplication.instance().quit())
        else:
            event.accept()


# 程序入口：显示启动屏幕并启动主事件循环
if __name__ == "__main__":
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
