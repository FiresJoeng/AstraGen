# src/__init__.py

"""
自动化处理工具包

作者: GitHub @FiresJoeng
版本: 1.0 Demo
"""

__author__ = "GitHub @FiresJoeng"
__version__ = "1.0 Demo"

__all__ = [
    'api_verifier',
    'docx_filler',
    'qcc_crawler'
]

# 显式导入核心模块
from . import api_verifier
from . import docx_filler
from . import qcc_crawler
