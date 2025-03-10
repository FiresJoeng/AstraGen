from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont, QFontDatabase


class FadeAnimations:
    @staticmethod
    def fade_in(widget, duration=200, start=0, end=0.75):
        """
        淡入动画：让 widget 的透明度从 start 变化到 end
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


class FontLoader:
    @staticmethod
    def load_font(app, font_path, fallback="Arial"):
        """
        加载自定义字体，若加载失败则使用 fallback 字体
        """
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app.setFont(QFont(font_family))
        else:
            print("[Error] 加载自定义字体失败！")
            app.setFont(QFont(fallback))
