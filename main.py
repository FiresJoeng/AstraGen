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

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from dotenv import load_dotenv
from ui import *

# 加载环境变量文件
load_dotenv()

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/SarasaMonoSC-Light.ttf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))
else:
    print("[Error] 加载自定义字体失败！")
    font_family = "Arial"

# 创建并显示欢迎界面
if __name__ == "__main__":
    start_window = windows.WelcomeUI()
    controls.FadeAnimations.fade_and_show(start_window)
    sys.exit(app.exec_())
