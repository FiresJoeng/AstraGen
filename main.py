'''
TODO:
1. 修复所有窗口弹出不在最前的问题。
2. 使仓库链接可被点击。
3. 修复生成时窗口无响应的问题。
4. 制作go_button的禁用效果和重新启用效果。
5. 修复生成时窗口无响应的问题。
6. 设计帮助：help.html。
7. 设计配置，应当有：
    (1) 重新验证API的按钮
    (2) 访问页面截图
    (3) 模型选择
    (4) 是否无头模式
    (5) 清理企查查缓存按钮
'''


import sys
from PyQt5.QtWidgets import QApplication
from dotenv import load_dotenv
from ui import *


load_dotenv()

app = QApplication(sys.argv)
controls.FontLoader.load_font(
    app, font_path="fonts/SarasaMonoSC-Light.ttf", fallback="Arial")


# 底层运行逻辑
if __name__ == "__main__":
    start_window = windows.WelcomeUI()
    controls.FadeAnimations.fade_and_show(start_window)
    sys.exit(app.exec_())
