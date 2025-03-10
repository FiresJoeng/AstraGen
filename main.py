'''
TODO:
1. 修复所有窗口弹出不在最前的问题。
2. 简化现有代码，将冗余的类封装进.py从ui文件夹中调用。
3. GeneratorWindow的设计。
4. 制作go_button的禁用效果和重新启用效果。
5. 修复生成时窗口无响应的问题。
6. 设计帮助：help.html。
7. 设计配置，应当有：
    (1) 重新验证API的按钮
    (2) 登录页面截图
    (3) 模型选择
    (4) 是否无头模式
    (5) 清理企查查缓存按钮
8. 清除代码冗余部分，然后格式化，使其符合PEP 8标准。
'''

import sys
from PyQt5.QtWidgets import QApplication
from dotenv import load_dotenv
from ui import *

# 加载环境变量文件
load_dotenv()

app = QApplication(sys.argv)
controls.FontLoader.load_font(app, font_path="fonts/SarasaMonoSC-Light.ttf", fallback="Arial")

# 创建并显示欢迎界面
if __name__ == "__main__":
    start_window = windows.WelcomeUI()
    controls.FadeAnimations.fade_and_show(start_window)
    sys.exit(app.exec_())
