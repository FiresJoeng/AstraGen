import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QLineEdit, QMessageBox, QDesktopWidget
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPoint

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("加载自定义字体失败！")


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


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('AstraGen 星核')
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.70)
        self.center()
        self._offset = None

        self.welcome_label = QLabel('欢迎使用AstraGen 星核', self)
        self.welcome_label.setFont(QFont(app.font().family(), 14))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setGeometry(100, 35, 200, 30)

        self.exit_button = QPushButton('[->', self)
        self.exit_button.setGeometry(350, 10, 50, 25)
        self.exit_button.setStyleSheet("""
            background-color: transparent;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        self.exit_button.clicked.connect(QApplication.instance().quit)

        self.search_entry = CustomLineEdit('请输入Deepseek的API Key', self)
        self.search_entry.setGeometry(50, 85, 200, 30)

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
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_search(self):
        api_key = self.search_entry.text()
        if not api_key.strip():
            QMessageBox.warning(self, "Error!", "请输入有效的API Key")
        else:
            print(f"API Key: {api_key}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self._offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._offset)

    def mouseReleaseEvent(self, event):
        self._offset = None


if __name__ == '__main__':
    window = UI()
    window.show()
    sys.exit(app.exec_())
