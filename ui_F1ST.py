import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("[Error] 加载自定义字体失败！")
    font_family = "Arial"


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self._is_closing = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 150)
        self.center()
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.75)
        self.init_ui()
        self.start_animation()

    def init_ui(self):
        self.label = QLabel("极速启动中...", self)
        self.label.setStyleSheet("color: white; font-size: 18px;")
        self.label.adjustSize()
        self.label.move((self.width() - self.label.width()) // 2, 50)

        self.progress_container = QWidget(self)
        self.progress_container.setGeometry(50, 100, 300, 20)
        self.progress_container.setStyleSheet(
            "border: 2px solid white; border-radius: 5px; background-color: transparent;"
        )

        self.progress_fill = QWidget(self.progress_container)
        self.progress_fill.setGeometry(2, 2, 0, 16)
        self.progress_fill.setStyleSheet(
            "background-color: #0077ED; border-radius: 3px;")

    def start_animation(self):
        self.animation = QPropertyAnimation(self.progress_fill, b"size")
        self.animation.setDuration(800)
        self.animation.setStartValue(self.progress_fill.size())
        self.animation.setEndValue(QSize(296, 16))
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.finished.connect(self.on_animation_finished)
        self.animation.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_animation_finished(self):
        center_point = self.frameGeometry().center()
        self.fade_and_close(callback=lambda: self.open_main(center_point))

    def open_main(self, center_point):
        self.main_window = UI(center_point)
        self.main_window.show()

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
            self.fade_and_close()
        else:
            event.accept()


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
        self.placeholder = placeholder
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


class UI(QWidget):
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

        self.welcome_label = QLabel("欢迎使用 - AstraGen 星核", self)
        self.welcome_label.setFont(QFont(app.font().family(), 14))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.adjustSize()
        self.welcome_label.move(
            (self.width() - self.welcome_label.width()) // 2, 50)

        self.exit_button = QPushButton("×", self)
        self.exit_button.setGeometry(350, 10, 30, 25)
        self.exit_button.setStyleSheet(
            "background-color: transparent; color: white; border: none;")
        self.exit_button.clicked.connect(self.close)

        self.search_entry = CustomLineEdit("请输入DeepSeek的API KEY", self)
        self.search_entry.setGeometry(50, 100, 200, 30)

        self.search_button = QPushButton("确认", self)
        self.search_button.setGeometry(270, 100, 80, 30)
        self.search_button.setStyleSheet(
            "background-color: #0077ED; color: white; border: none; border-radius: 5px;"
        )
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


if __name__ == "__main__":
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
