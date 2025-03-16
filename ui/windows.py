import asyncio
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QDesktopWidget, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from dotenv import set_key, find_dotenv
from src import *
from ui.widgets import BlueButton, LiteButton, EntryBox, MsgBox
from ui.controls import FadeAnimations, MouseEvents


class MainUI(MouseEvents, QWidget):
    """
    主界面，包含配置、帮助、退出等按钮，以及报告生成的入口
    """

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("AstraGen - 银行信贷报告一键生成")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)
        self.center()
        self.init_ui()
        FadeAnimations.fade_in(self)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        # 配置按钮
        self.setting_button = LiteButton("配置", self)
        self.setting_button.setGeometry(160, 10, 75, 30)
        self.setting_button.clicked.connect(self.on_setting)

        # 帮助按钮
        self.help_button = LiteButton("帮助", self)
        self.help_button.setGeometry(240, 10, 75, 30)
        self.help_button.clicked.connect(self.on_help)

        # 退出按钮
        self.exit_button = LiteButton("退出", self)
        self.exit_button.setGeometry(320, 10, 75, 30)
        self.exit_button.clicked.connect(self.close_window)

        # 图形视图
        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setGeometry(140, 100, 128, 128)
        self.graphicsView.setStyleSheet(
            "background-color: transparent; border: none;")
        scene = QGraphicsScene(self)
        pixmap = QPixmap("img/icon.png")
        if not pixmap.isNull():
            item = QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            item.setPos(
                (self.graphicsView.width() - pixmap.width()) / 2,
                (self.graphicsView.height() - pixmap.height()) / 2
            )
        else:
            print("[Error] icon.png 加载失败！")
        self.graphicsView.setScene(scene)

        # 标题标签
        self.title_label = QLabel("AstraGen - 星核", self)
        self.title_label.setStyleSheet("color: white; font-size: 32px;")
        self.title_label.adjustSize()
        self.title_label.move(
            (self.width() - self.title_label.width()) // 2, 250)

        # 企业关键词输入框
        self.keyword_entry = EntryBox("请输入企业关键词...", self)
        self.keyword_entry.setGeometry(50, 320, 200, 30)

        # 生成报告按钮
        self.go_button = BlueButton("生成报告", self)
        self.go_button.setGeometry(270, 320, 80, 30)
        self.go_button.clicked.connect(self.generate_report)

        # 版本标签
        self.ver_label = QLabel("AstraGen - Demo 1.0", self)
        self.ver_label.setStyleSheet("color: white;")
        self.ver_label.adjustSize()
        self.ver_label.move((self.width() - self.ver_label.width()) // 2, 560)

        # 项目仓库链接标签
        self.repo_button = LiteButton(
            "https://github.com/FiresJoeng/AstraGen", self)
        self.repo_button.adjustSize()
        self.repo_button.move(
            (self.width() - self.repo_button.width()) // 2, 580)
        self.repo_button.clicked.connect(self.go_to_repo)

    def go_to_repo(self):
        import webbrowser
        webbrowser.open("https://github.com/FiresJoeng/AstraGen")

    def generate_report(self):
        keyword = self.keyword_entry.text().strip()
        if not keyword:
            msg = MsgBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error!")
            msg.setText("请输入有效的企业关键词!")
            msg.show()
        else:
            try:
                asyncio.run(qcc_crawler.run_agents(keyword))
            except Exception as agents_error:
                msg = MsgBox(self)
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error!")
                msg.setText("主机尝试与DeepSeek服务器连接时, 发生了一个网络错误: " +
                            str(agents_error))
                msg.show()
            try:
                docx_filler.generate_report(keyword)
                msg = MsgBox(self)
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Succeeded!")
                msg.setText(f'关于"{keyword}"的信贷报告已经填充完毕!')
                msg.show()
            except Exception as filler_error:
                msg = MsgBox(self)
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error!")
                msg.setText("由于DeepSeek服务器拥挤, 未能如期获取企业信息: " +
                            str(filler_error))
                msg.show()

    def on_help(self):
        msg = MsgBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("帮助")
        msg.setText("帮助：将在后续版本解锁！")
        msg.show()

    def on_setting(self):
        msg = MsgBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("配置")
        msg.setText("配置：将在后续版本解锁！")
        msg.show()

    def close_window(self):
        FadeAnimations.fade_and_close(
            self, callback=lambda: QApplication.instance().quit())


class VerifyProgessBar(MouseEvents, QWidget):
    """
    验证进度条界面：显示连接至服务器的状态，并执行验证逻辑
    """

    def __init__(self, welcome_ui):
        super().__init__(None)
        self.welcome_ui = welcome_ui
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setWindowTitle("AstraGen 星核 - 连接中...")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)
        self.center()

        self.label = QLabel("连接至DeepSeek服务器...", self)
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
            "background-color: #0077ED; border: none;")
        self.progress_fill.setGeometry(2, 2, 0, 16)
        self.first_target_width = int(296 * 0.4)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
        FadeAnimations.fade_in(self, start=0, end=0.75)
        QTimer.singleShot(0, self.start_first_animation)

    def start_first_animation(self):
        self.first_animation = QPropertyAnimation(self.progress_fill, b"size")
        self.first_animation.setDuration(150)
        self.first_animation.setStartValue(self.progress_fill.size())
        self.first_animation.setEndValue(QSize(self.first_target_width, 16))
        self.first_animation.setEasingCurve(QEasingCurve.Linear)
        self.first_animation.finished.connect(self.start_verification)
        self.first_animation.start()

    def start_verification(self):
        try:
            api_verifier.verify_deepseek_api()
            self.label.setText("验证成功! 极速启动中...")
            self.label.adjustSize()
            self.label.move((self.width() - self.label.width()) // 2, 50)
            self.start_second_animation()
        except Exception as e:
            FadeAnimations.fade_and_close(
                self, callback=lambda e=str(e): self.verification_failed(e)
            )

    def verification_failed(self, error_message):
        if self.welcome_ui:
            FadeAnimations.fade_and_show(self.welcome_ui)
            msg = MsgBox(self.welcome_ui)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error!")
            msg.setText(error_message)
            msg.show()

    def start_second_animation(self):
        current_size = self.progress_fill.size()
        target_size = QSize(296, 16)
        self.second_animation = QPropertyAnimation(self.progress_fill, b"size")
        self.second_animation.setDuration(400)
        self.second_animation.setStartValue(current_size)
        self.second_animation.setEndValue(target_size)
        self.second_animation.setEasingCurve(QEasingCurve.Linear)
        self.second_animation.finished.connect(self.open_main_ui)
        self.second_animation.start()

    def open_main_ui(self):
        FadeAnimations.fade_and_close(self, callback=self.launch_main_ui)

    def launch_main_ui(self):
        main_ui = MainUI()
        main_ui.show()


class WelcomeUI(MouseEvents, QWidget):
    """
    欢迎界面，包含 API KEY 输入和验证逻辑
    """

    def __init__(self, center_point=None):
        super().__init__()
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("AstraGen 星核 - 欢迎页面")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)

        if center_point:
            self.move(center_point.x() - self.width() // 2,
                      center_point.y() - self.height() // 2)
        else:
            self.center()

        self.welcome_label = QLabel("欢迎使用 - AstraGen 星核", self)
        # 使用全局字体，保证加载自定义字体后的字体被应用
        self.welcome_label.setFont(
            QFont(QApplication.instance().font().family(), 14))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.adjustSize()
        self.welcome_label.move(
            (self.width() - self.welcome_label.width()) // 2, 50)

        self.exit_button = LiteButton("×", self)
        self.exit_button.setGeometry(350, 10, 30, 25)
        self.exit_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 20px;
            }
            QPushButton:hover {
                color: gray;
            }
        """)
        self.exit_button.clicked.connect(self.close_window)

        self.api_entry = EntryBox("请输入DeepSeek的API KEY", self)
        self.api_entry.setGeometry(50, 100, 200, 30)
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.api_entry.setText(api_key)

        self.verify_button = BlueButton("验证", self)
        self.verify_button.setGeometry(270, 100, 80, 30)
        self.verify_button.clicked.connect(self.show_verifing)

        FadeAnimations.fade_in(self)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_verifing(self):
        api_key = self.api_entry.text().strip()
        if not api_key:
            msg = MsgBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error!")
            msg.setText("非法的输入内容!")
            msg.show()
        else:
            dotenv_path = find_dotenv()
            if not dotenv_path:
                dotenv_path = ".env"
            set_key(dotenv_path, "DEEPSEEK_API_KEY", api_key)
            os.environ["DEEPSEEK_API_KEY"] = api_key

            def after_fade():
                self.connect_window = VerifyProgessBar(welcome_ui=self)
                self.connect_window.show()

            FadeAnimations.fade_and_hide(self, callback=after_fade)

    def close_window(self):
        FadeAnimations.fade_and_close(
            self, callback=lambda: QApplication.instance().quit())
