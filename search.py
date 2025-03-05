import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGraphicsView, QDesktopWidget, QGraphicsScene, QGraphicsPixmapItem
)
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation

# 初始化应用程序并加载自定义字体
app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("[Error] 加载自定义字体失败！")
    font_family = "Arial"


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self._is_closing = False

        # 设置无边框窗口、固定大小以及背景风格（风格与ui.py一致，尺寸可调整）
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("MainWindow")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)

        # 居中显示窗口
        self.center()

        # 初始化控件
        self.init_ui()

        # 启动淡入动画
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(0.75)
        self.fade_in_animation.start()

        # 拖拽相关变量
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

        # 中部图形视图（可用于显示LOGO或图片）
        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setGeometry(140, 100, 128, 128)
        self.graphicsView.setStyleSheet(
            "background-color: transparent; border: none;")
        scene = QGraphicsScene(self)
        pixmap = QPixmap("icon.png")
        if not pixmap.isNull():
            item = QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            # 居中图标
            item.setPos((self.graphicsView.width() - pixmap.width()) / 2,
                        (self.graphicsView.height() - pixmap.height()) / 2)
        else:
            print("[Error] icon.png 加载失败！")
        self.graphicsView.setScene(scene)

        # 标签：英文说明标签，自适应尺寸且水平居中
        self.title_label = QLabel("AstraGen - 星核", self)
        self.title_label.setStyleSheet("color: white;font-size: 32px;")
        self.title_label.adjustSize()
        self.title_label.move(
            (self.width() - self.title_label.width()) // 2, 250)

        # 输入框：使用 QLineEdit 限制为单行，并设置 placeholder（文字颜色保持黑色）
        self.search_entry = QLineEdit(self)
        self.search_entry.setGeometry(50, 320, 200, 30)
        self.search_entry.setPlaceholderText("请输入企业关键词...")
        self.search_entry.setStyleSheet(
            "color: black; border: 2px solid #d9d9d9; background-color: white; border-radius: 5px;"
        )

        # “生成报告”按钮（与输入框左右留白一致）
        self.go_button = QPushButton("生成报告", self)
        self.go_button.setGeometry(270, 320, 80, 30)
        self.go_button.setStyleSheet(
            "background-color: #0077ED; color: white; border: none; border-radius: 5px; font-size: 16px;"
        )
        self.go_button.clicked.connect(self.on_go)

        # 底部版本信息标签（自适应尺寸并居中）
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
        """使窗口居中显示"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_go(self):
        """处理生成报告按钮点击事件"""
        keyword = self.search_entry.text().strip()
        if not keyword:
            print("请输入有效的企业关键词！")
        else:
            print(f"生成报告，企业关键词：{keyword}")
            # 后续生成报告的逻辑可以在此添加

    def on_help(self):
        """处理帮助按钮点击事件"""
        print("帮助：将在后续的版本解锁！")
        # 可弹出帮助对话框或执行其他操作

    def on_setting(self):
        """处理配置按钮点击事件"""
        print("配置：将在后续的版本解锁！")
        # 可打开配置窗口或执行其他操作

    def fade_and_close(self, callback=None):
        """执行淡出动画后关闭窗口"""
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
        """记录鼠标点击位置，实现窗口拖动"""
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        """拖动窗口时更新窗口位置"""
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        """释放鼠标后重置偏移量"""
        if event.button() == Qt.LeftButton:
            self._offset = None

    def closeEvent(self, event):
        """重写关闭事件，实现淡出效果后退出"""
        if not self._is_closing:
            event.ignore()
            self.fade_and_close(
                callback=lambda: QApplication.instance().quit())
        else:
            event.accept()


if __name__ == "__main__":
    window = MainUI()
    window.show()
    sys.exit(app.exec_())
