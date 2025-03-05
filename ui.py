import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
    QDesktopWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from dotenv import load_dotenv, set_key, find_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化应用程序并加载自定义字体
app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("[Error] 加载自定义字体失败！")
    font_family = "Arial"


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
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, "_offset") and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = None

    def showEvent(self, event):
        if self.parent():
            parent_geometry = self.parent().frameGeometry()
            self_geometry = self.frameGeometry()
            new_x = parent_geometry.center().x() - self_geometry.width() // 2
            new_y = parent_geometry.center().y() - self_geometry.height() // 2
            self.move(new_x, new_y)
        super().showEvent(event)


class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(
            "color: grey; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
        )

    def focusInEvent(self, event):
        self.setStyleSheet(
            "color: black; border: 2px solid #0077ED; background-color: white; border-radius: 5px;"
        )
        super().focusInEvent(event)

    def focusOutEvent(self, event):
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
        if not self.hasFocus():
            self.setStyleSheet(
                "color: grey; border: 2px solid black; background-color: #f9f9f9; border-radius: 5px;"
            )
        super().enterEvent(event)

    def leaveEvent(self, event):
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


class WelcomeUI(QWidget):
    def __init__(self, center_point=None):
        super().__init__()
        self._is_closing = False
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("AstraGen 星核")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)

        if center_point:
            self.move(center_point.x() - self.width() // 2,
                      center_point.y() - self.height() // 2)
        else:
            self.center()

        self._offset = None

        # 欢迎标签
        self.welcome_label = QLabel("欢迎使用 - AstraGen 星核", self)
        self.welcome_label.setFont(QFont(app.font().family(), 14))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.adjustSize()
        self.welcome_label.move(
            (self.width() - self.welcome_label.width()) // 2, 50)

        # 退出按钮
        self.exit_button = QPushButton("×", self)
        self.exit_button.setGeometry(350, 10, 30, 25)
        self.exit_button.setStyleSheet(
            "background-color: transparent; color: white; border: none;")
        self.exit_button.clicked.connect(self.close)

        # 预填充 API KEY（从 .env 中读取）
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.search_entry = CustomLineEdit("请输入DeepSeek的API KEY", self)
        self.search_entry.setGeometry(50, 100, 200, 30)
        self.search_entry.setText(api_key)

        self.search_button = QPushButton("验证", self)
        self.search_button.setGeometry(270, 100, 80, 30)
        self.search_button.setStyleSheet(
            "background-color: #0077ED; color: white; border: none; border-radius: 5px;")
        self.search_button.clicked.connect(self.on_search)

        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(0.75)
        self.fade_in_animation.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_search(self):
        api_key = self.search_entry.text().strip()
        if not api_key:
            msg = CustomMsgBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error!")
            msg.setText("非法的输入内容!")
            msg.show()
        else:
            # 保存 API KEY 到 .env 文件
            dotenv_path = find_dotenv()
            if not dotenv_path:
                dotenv_path = ".env"
            set_key(dotenv_path, "DEEPSEEK_API_KEY", api_key)
            os.environ["DEEPSEEK_API_KEY"] = api_key

            self.hide()
            # VerifyWindow 独立显示，不指定父控件
            self.connect_window = VerifyWindow(welcome_ui=self)
            self.connect_window.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = None

    def fade_and_close(self, callback=None):
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
        if not self._is_closing:
            event.ignore()
            self.fade_and_close(
                callback=lambda: QApplication.instance().quit())
        else:
            event.accept()


class VerifyWindow(QWidget):
    def __init__(self, welcome_ui):
        super().__init__(None)
        self.welcome_ui = welcome_ui
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.75)
        self.center()
        self._offset = None

        self.label = QLabel("连接至服务器...", self)
        self.label.setStyleSheet("color: white; font-size: 18px;")
        self.label.adjustSize()
        self.label.move((self.width() - self.label.width()) // 2, 50)

        self.progress_container = QWidget(self)
        self.progress_container.setGeometry(50, 100, 300, 20)
        self.progress_container.setStyleSheet(
            "border: 2px solid white; border-radius: 5px; background-color: transparent;"
        )
        self.progress_fill = QWidget(self.progress_container)
        self.progress_fill.setStyleSheet(
            "background-color: #0077ED; border: none; border-radius: none;")
        self.progress_fill.setGeometry(2, 2, 0, 16)

        # 40%对应的宽度
        self.first_target_width = int(296 * 0.4)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = None

    def showEvent(self, event):
        super().showEvent(event)
        # 窗口显示后启动第一段动画
        QTimer.singleShot(0, self.start_first_animation)

    def start_first_animation(self):
        self.first_animation = QPropertyAnimation(self.progress_fill, b"size")
        self.first_animation.setDuration(300)
        self.first_animation.setStartValue(self.progress_fill.size())
        self.first_animation.setEndValue(QSize(self.first_target_width, 16))
        self.first_animation.setEasingCurve(QEasingCurve.Linear)
        self.first_animation.finished.connect(self.start_verification)
        self.first_animation.start()

    def start_verification(self):
        try:
            from api_verifier import verify_deepseek_api
            verify_deepseek_api()  # 仅调用 API 验证
            # 验证成功后更新标签文字
            self.label.setText("验证成功! 极速启动中...")
            self.label.adjustSize()
            self.label.move((self.width() - self.label.width()) // 2, 50)
            self.start_second_animation()
        except Exception as e:
            self.close()
            if self.welcome_ui:
                self.welcome_ui.show()
                msg = CustomMsgBox(self.welcome_ui)
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error!")
                msg.setText(str(e))
                msg.show()

    def start_second_animation(self):
        current_size = self.progress_fill.size()
        target_size = QSize(296, 16)
        self.second_animation = QPropertyAnimation(self.progress_fill, b"size")
        self.second_animation.setDuration(100)
        self.second_animation.setStartValue(current_size)
        self.second_animation.setEndValue(target_size)
        self.second_animation.setEasingCurve(QEasingCurve.Linear)
        self.second_animation.finished.connect(self.open_main_ui)
        self.second_animation.start()

    def open_main_ui(self):
        self.close()
        main_ui = MainUI()
        main_ui.show()


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self._is_closing = False
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("MainWindow")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)
        self.center()
        self.init_ui()

        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(0.75)
        self.fade_in_animation.start()

        self._offset = None

    def init_ui(self):
        top_button_style = """
        QPushButton {
            background-color: transparent;
            color: white;
            border: none;
            text-decoration: underline;
            font-size: 16px;
        }
        QPushButton:hover {
            color: #0077ED;
        }
        """
        # 右上角三个按钮：配置、帮助、退出
        self.setting_button = QPushButton("配置", self)
        self.setting_button.setGeometry(160, 10, 75, 30)
        self.setting_button.setStyleSheet(top_button_style)
        self.setting_button.clicked.connect(self.on_setting)

        self.help_button = QPushButton("帮助", self)
        self.help_button.setGeometry(240, 10, 75, 30)
        self.help_button.setStyleSheet(top_button_style)
        self.help_button.clicked.connect(self.on_help)

        self.exit_button = QPushButton("退出", self)
        self.exit_button.setGeometry(320, 10, 75, 30)
        self.exit_button.setStyleSheet(top_button_style)
        self.exit_button.clicked.connect(self.close)

        # 中部图形视图（用于显示 LOGO 或图片）
        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setGeometry(140, 100, 128, 128)
        self.graphicsView.setStyleSheet(
            "background-color: transparent; border: none;")
        scene = QGraphicsScene(self)
        pixmap = QPixmap("icon.png")
        if not pixmap.isNull():
            item = QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            item.setPos((self.graphicsView.width() - pixmap.width()) / 2,
                        (self.graphicsView.height() - pixmap.height()) / 2)
        else:
            print("[Error] icon.png 加载失败！")
        self.graphicsView.setScene(scene)

        # 主标题标签
        self.title_label = QLabel("AstraGen - 星核", self)
        self.title_label.setStyleSheet("color: white;font-size: 32px;")
        self.title_label.adjustSize()
        self.title_label.move(
            (self.width() - self.title_label.width()) // 2, 250)

        # 输入框：企业关键词
        self.search_entry = QLineEdit(self)
        self.search_entry.setGeometry(50, 320, 200, 30)
        self.search_entry.setPlaceholderText("请输入企业关键词...")
        self.search_entry.setStyleSheet(
            "color: black; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
        )

        # “生成报告”按钮
        self.go_button = QPushButton("生成报告", self)
        self.go_button.setGeometry(270, 320, 80, 30)
        self.go_button.setStyleSheet(
            "background-color: #0077ED; color: white; border: none; border-radius: 5px; font-size: 16px;"
        )
        self.go_button.clicked.connect(self.on_go)

        # 底部版本信息标签
        self.ver_label = QLabel("AstraGen - Demo 1.0", self)
        self.ver_label.setStyleSheet("color: white;")
        self.ver_label.adjustSize()
        self.ver_label.move((self.width() - self.ver_label.width()) // 2, 560)

        self.repo_label = QLabel(
            "https://github.com/FiresJoeng/AstraGen", self)
        self.repo_label.setStyleSheet("color: white;")
        self.repo_label.adjustSize()
        self.repo_label.move(
            (self.width() - self.repo_label.width()) // 2, 580)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_go(self):
        keyword = self.search_entry.text().strip()
        if not keyword:
            print("请输入有效的企业关键词！")
        else:
            print(f"生成报告，企业关键词：{keyword}")
            # 生成报告逻辑后续实现

    def on_help(self):
        print("帮助：将在后续版本解锁！")

    def on_setting(self):
        print("配置：将在后续版本解锁！")

    def fade_and_close(self, callback=None):
        self._is_closing = True
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(200)
        self.fade_animation.setStartValue(self.windowOpacity())
        self.fade_animation.setEndValue(0)
        if callback:
            self.fade_animation.finished.connect(callback)
        self.fade_animation.finished.connect(lambda: QWidget.close(self))
        self.fade_animation.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = None

    def closeEvent(self, event):
        if not self._is_closing:
            event.ignore()
            self.fade_and_close(
                callback=lambda: QApplication.instance().quit())
        else:
            event.accept()


if __name__ == "__main__":
    welcome = WelcomeUI()
    welcome.show()
    sys.exit(app.exec_())
