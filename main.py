'''
TODO:
1. 修复所有窗口弹出不在最前的问题。
2. 简化现有代码，将冗余的类封装进.py从ui文件夹中调用。
3. GeneratorWindow的设计。
4. 增加预制按钮。
5. 制作go_button的禁用效果和重新启用效果。
6. 修复生成时窗口无响应的问题。
7. 设计帮助：help.html。
8. 设计配置，应当有：
    (1) 重新验证API的按钮
    (2) 登录页面截图
    (3) 模型选择
    (4) 是否无头模式
    (5) 清理企查查缓存按钮
'''


import asyncio
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
    QDesktopWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from dotenv import load_dotenv, set_key, find_dotenv
from src import *

# 加载环境变量文件
load_dotenv()

# 初始化应用程序，并加载自定义字体
app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    # 获取加载成功后的字体族名，并设置应用字体
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("[Error] 加载自定义字体失败！")
    font_family = "Arial"


# 预制按钮类
class BlueButton(QPushButton):
    """
    蓝色预制按钮，适用于验证按钮和生成报告按钮
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            "background-color: #0077ED; color: white; border: none; border-radius: 5px; font-size: 16px;"
        )


class LiteButton(QPushButton):
    """
    轻量预制按钮，用于主界面右上角的配置、帮助和退出按钮
    """
    default_style = """
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

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(LiteButton.default_style)


# 鼠标拖动窗口
class MouseEvents:
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 记录鼠标点击时相对于窗口的偏移量
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, "_offset") and event.buttons() == Qt.LeftButton:
            # 拖动窗口
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 重置偏移量
            self._offset = None


# 淡入淡出动画
class FadeAnimations:
    @staticmethod
    def fade_in(widget, duration=200, start=0, end=0.75):
        """
        淡入动画：让widget的透明度从start变化到end
        """
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.start()
        widget._fade_in_animation = animation
        return animation

    @staticmethod
    def fade_and_close(widget, callback=None, duration=200):
        """
        淡出并关闭窗口的动画
        """
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(widget.windowOpacity())
        animation.setEndValue(0)
        if callback:
            animation.finished.connect(callback)
        animation.finished.connect(lambda: QWidget.close(widget))
        animation.start()
        widget._fade_animation = animation

    @staticmethod
    def fade_and_show(widget, duration=200):
        """
        淡入并显示窗口的动画
        """
        widget.show()
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0)
        animation.setEndValue(0.75)
        animation.start()
        widget._fade_animation = animation

    @staticmethod
    def fade_and_hide(widget, callback=None, duration=200):
        """
        淡出并隐藏窗口的动画
        """
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(widget.windowOpacity())
        animation.setEndValue(0)
        if callback:
            animation.finished.connect(callback)
        animation.finished.connect(widget.hide)
        animation.start()
        widget._fade_animation = animation


# 预制 输入框
class EntryBox(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(
            "color: grey; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
        )

    def focusInEvent(self, event):
        # 聚焦时改变样式
        self.setStyleSheet(
            "color: black; border: 2px solid #0077ED; background-color: white; border-radius: 5px;"
        )
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # 失焦时根据是否有文本内容改变样式
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
        # 鼠标进入时改变样式（未聚焦）
        if not self.hasFocus():
            self.setStyleSheet(
                "color: grey; border: 2px solid black; background-color: #f9f9f9; border-radius: 5px;"
            )
        super().enterEvent(event)

    def leaveEvent(self, event):
        # 鼠标离开时恢复原始样式
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


# 预制 消息弹窗
class MsgBox(MouseEvents, QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置窗口图标
        self.setWindowIcon(QIcon("img/icon.ico"))
        # 设置对话框样式
        self.setStyleSheet("background-color: white; color: black;")
        self.setStandardButtons(QMessageBox.Close)
        # 自定义关闭按钮文本和样式
        self.button(QMessageBox.Close).setText("好的")
        self.button(QMessageBox.Close).setStyleSheet(
            "min-width: 60px; border: 1px solid gray; border-radius: 1px;"
        )

        # 在初始化时设置位置
        self.adjustSize()  # 确保窗口大小正确
        self._center_window()

    def _center_window(self):
        """将窗口居中显示"""
        if self.parent():
            # 相对于父窗口居中
            parent_geometry = self.parent().frameGeometry()
            new_x = parent_geometry.center().x() - self.width() // 2
            new_y = parent_geometry.center().y() - self.height() // 2
        else:
            # 相对于屏幕居中
            screen_geometry = QDesktopWidget().availableGeometry()
            new_x = screen_geometry.center().x() - self.width() // 2
            new_y = screen_geometry.center().y() - self.height() // 2
        self.move(new_x, new_y)

    def showEvent(self, event):
        """确保窗口显示时保持居中"""
        super().showEvent(event)
        self._center_window()


# 欢迎界面
class WelcomeUI(MouseEvents, QWidget):
    """
    欢迎界面，包含API KEY输入和验证逻辑
    """

    def __init__(self, center_point=None):
        super().__init__()
        # 设置窗口图标
        self.setWindowIcon(QIcon("img/icon.ico"))
        # 设置窗口无边框和基本属性
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("AstraGen 星核 - 欢迎页面")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)

        # 如果提供了中心点，则移动窗口到该位置，否则居中显示
        if center_point:
            self.move(center_point.x() - self.width() // 2,
                      center_point.y() - self.height() // 2)
        else:
            self.center()

        # 欢迎标签
        self.welcome_label = QLabel("欢迎使用 - AstraGen 星核", self)
        self.welcome_label.setFont(QFont(app.font().family(), 14))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.adjustSize()
        self.welcome_label.move(
            (self.width() - self.welcome_label.width()) // 2, 50
        )

        # 退出按钮
        self.exit_button = QPushButton("×", self)
        self.exit_button.setGeometry(350, 10, 30, 25)
        self.exit_button.setStyleSheet(
            "background-color: transparent; color: white; border: none;"
        )
        self.exit_button.clicked.connect(self.close_window)

        # API KEY输入框
        self.api_entry = EntryBox("请输入DeepSeek的API KEY", self)
        self.api_entry.setGeometry(50, 100, 200, 30)
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.api_entry.setText(api_key)

        # 验证按钮（使用BlueButton预制类）
        self.verify_button = BlueButton("验证", self)
        self.verify_button.setGeometry(270, 100, 80, 30)
        self.verify_button.clicked.connect(self.show_verifing)

        # 执行淡入动画显示窗口
        FadeAnimations.fade_in(self)

    def center(self):
        """
        将窗口居中显示
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_verifing(self):
        """
        API KEY验证逻辑：
        1. 检查输入是否为空
        2. 保存API KEY到环境变量文件中
        3. 执行淡出动画，并启动验证进度条界面
        """
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

            # 动画结束后显示验证进度条窗口
            def after_fade():
                self.connect_window = VerifyProgessBar(welcome_ui=self)
                self.connect_window.show()

            FadeAnimations.fade_and_hide(self, callback=after_fade)

    def close_window(self):
        """
        点击退出按钮时，通过淡出动画退出应用
        """
        FadeAnimations.fade_and_close(
            self, callback=lambda: QApplication.instance().quit())


# 验证进度条界面
class VerifyProgessBar(MouseEvents, QWidget):
    """
    验证进度条界面：
    显示连接至服务器的状态，并执行验证逻辑
    """

    def __init__(self, welcome_ui):
        super().__init__(None)
        self.welcome_ui = welcome_ui
        # 设置窗口图标
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.setWindowTitle("AstraGen 星核 - 连接中...")
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)
        self.center()

        # 状态标签
        self.label = QLabel("连接至DeepSeek服务器...", self)
        self.label.setStyleSheet("color: white; font-size: 18px;")
        self.label.adjustSize()
        self.label.move((self.width() - self.label.width()) // 2, 50)

        # 进度条容器
        self.progress_container = QWidget(self)
        self.progress_container.setGeometry(50, 100, 300, 20)
        self.progress_container.setStyleSheet(
            "border: 2px solid white; border-radius: 5px; background-color: transparent;"
        )
        # 进度条填充部分
        self.progress_fill = QWidget(self.progress_container)
        self.progress_fill.setStyleSheet(
            "background-color: #0077ED; border: none; border-radius: none;"
        )
        self.progress_fill.setGeometry(2, 2, 0, 16)
        self.first_target_width = int(296 * 0.4)

    def center(self):
        """
        将窗口居中显示
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        """
        显示窗口时执行淡入动画，并启动第一个动画阶段
        """
        super().showEvent(event)
        FadeAnimations.fade_in(self, start=0, end=0.75)
        QTimer.singleShot(0, self.start_first_animation)

    def start_first_animation(self):
        """
        第一个动画：进度条从0扩展到目标宽度的40%
        """
        self.first_animation = QPropertyAnimation(self.progress_fill, b"size")
        self.first_animation.setDuration(150)
        self.first_animation.setStartValue(self.progress_fill.size())
        self.first_animation.setEndValue(QSize(self.first_target_width, 16))
        self.first_animation.setEasingCurve(QEasingCurve.Linear)
        self.first_animation.finished.connect(self.start_verification)
        self.first_animation.start()

    def start_verification(self):
        """
        开始验证API的过程，并根据结果更新状态
        """
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
        """
        验证失败时，显示错误消息，并重新显示欢迎界面
        """
        if self.welcome_ui:
            FadeAnimations.fade_and_show(self.welcome_ui)
            msg = MsgBox(self.welcome_ui)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error!")
            msg.setText(error_message)
            msg.show()

    def start_second_animation(self):
        """
        第二个动画：进度条扩展到完整宽度
        """
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
        """
        淡出当前窗口，并启动主界面
        """
        FadeAnimations.fade_and_close(self, callback=self.launch_main_ui)

    def launch_main_ui(self):
        """
        创建并显示主界面
        """
        main_ui = MainUI()
        main_ui.show()


# 主界面
class MainUI(MouseEvents, QWidget):
    """
    主界面，包含配置、帮助、退出等按钮，以及报告生成的入口
    """

    def __init__(self):
        super().__init__()
        # 设置窗口图标
        self.setWindowIcon(QIcon("img/icon.ico"))
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("AstraGen - 银行信贷报告一键生成")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)
        self.center()

        # 初始化UI组件
        self.init_ui()

        # 执行淡入动画显示窗口
        FadeAnimations.fade_in(self)

    def init_ui(self):
        """
        初始化主界面的所有控件
        """
        # 配置按钮（使用LiteButton预制类）
        self.setting_button = LiteButton("配置", self)
        self.setting_button.setGeometry(160, 10, 75, 30)
        self.setting_button.clicked.connect(self.on_setting)

        # 帮助按钮（使用LiteButton预制类）
        self.help_button = LiteButton("帮助", self)
        self.help_button.setGeometry(240, 10, 75, 30)
        self.help_button.clicked.connect(self.on_help)

        # 退出按钮（使用LiteButton预制类），点击时通过fade_and_close退出应用
        self.exit_button = LiteButton("退出", self)
        self.exit_button.setGeometry(320, 10, 75, 30)
        self.exit_button.clicked.connect(self.close_window)

        # 图形视图，显示图标
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
        self.title_label.setStyleSheet("color: white;font-size: 32px;")
        self.title_label.adjustSize()
        self.title_label.move(
            (self.width() - self.title_label.width()) // 2, 250
        )

        # 企业关键词输入框
        self.keyword_entry = EntryBox("请输入企业关键词...", self)
        self.keyword_entry.setGeometry(50, 320, 200, 30)

        # 生成报告按钮（使用BlueButton预制类）
        self.go_button = BlueButton("生成报告", self)
        self.go_button.setGeometry(270, 320, 80, 30)
        self.go_button.clicked.connect(self.generate_report)

        # 版本标签
        self.ver_label = QLabel("AstraGen - Demo 1.0", self)
        self.ver_label.setStyleSheet("color: white;")
        self.ver_label.adjustSize()
        self.ver_label.move((self.width() - self.ver_label.width()) // 2, 560)

        # 项目仓库链接标签
        self.repo_label = QLabel(
            "https://github.com/FiresJoeng/AstraGen", self)
        self.repo_label.setStyleSheet("color: white;")
        self.repo_label.adjustSize()
        self.repo_label.move(
            (self.width() - self.repo_label.width()) // 2, 580
        )

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
                asyncio.run(qcc_crawler.run_agent(keyword))
                docx_filler.generate_report(keyword)
            except Exception as e:
                msg = MsgBox(self)
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error!")
                msg.setText("发生了一个致命错误: " + str(e))
                msg.show()

    def on_help(self):
        print("帮助：将在后续版本解锁！")

    def on_setting(self):
        print("配置：将在后续版本解锁！")

    def close_window(self):
        FadeAnimations.fade_and_close(
            self, callback=lambda: QApplication.instance().quit())


# 直接运行的底层逻辑
if __name__ == "__main__":
    start_window = WelcomeUI()
    start_window.show()
    sys.exit(app.exec_())
