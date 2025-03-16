from src import *
import asyncio
from PyQt5.QtCore import QThread, pyqtSignal


class ReportGenerator(QThread):
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def run(self):
        try:
            # 运行异步爬虫任务
            asyncio.run(qcc_crawler.run_agents(self.keyword))
        except Exception as e:
            self.error_occurred.emit("主机尝试与DeepSeek服务器连接时发生错误: " + str(e))
            return
        try:
            # 生成报告任务（假设 docx_filler.generate_report 为耗时操作）
            docx_filler.generate_report(self.keyword)
        except Exception as e:
            self.error_occurred.emit("由于DeepSeek服务器解析问题，未能如期提取企业信息: " + str(e))
            return
        # 如果所有任务执行成功，则发送完成信号
        self.finished.emit()


# 如需调试，在此添加入口逻辑
if __name__ == "__main__":
    pass
