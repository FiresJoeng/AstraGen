# ui/__init__.py

"""
Qt5界面包

作者: GitHub @FiresJoeng
版本: 1.0 Demo
"""

__author__ = "GitHub @FiresJoeng"
__version__ = "1.0 Demo"

__all__ = [
    'controls',
    'widgets',
    'windows'
]

# 显式导入核心模块
from . import controls
from . import widgets
from . import windows
