from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon


class BlueButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            "background-color: #0077ED; color: white; border: none; border-radius: 5px; font-size: 16px;"
        )


class EntryBox(QLineEdit):
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


class LiteButton(QPushButton):
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


class MsgBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置窗口图标
        self.setWindowIcon(QIcon("img/icon_black.ico"))
        # 设置对话框样式
        self.setStyleSheet("background-color: white; color: black;")
        self.setStandardButtons(QMessageBox.Close)
        # 自定义关闭按钮文本和样式
        self.button(QMessageBox.Close).setText("好的")
        self.button(QMessageBox.Close).setStyleSheet(
            "min-width: 60px; border: 1px solid gray; border-radius: 1px;"
        )
        # 在初始化时设置位置
        self.adjustSize()
        self._center_window()

    def _center_window(self):
        from PyQt5.QtWidgets import QDesktopWidget
        if self.parent():
            parent_geometry = self.parent().frameGeometry()
            new_x = parent_geometry.center().x() - self.width() // 2
            new_y = parent_geometry.center().y() - self.height() // 2
        else:
            screen_geometry = QDesktopWidget().availableGeometry()
            new_x = screen_geometry.center().x() - self.width() // 2
            new_y = screen_geometry.center().y() - self.height() // 2
        self.move(new_x, new_y)

    def showEvent(self, event):
        super().showEvent(event)
        self._center_window()
