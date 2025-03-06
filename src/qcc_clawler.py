import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, Controller, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from pydantic import SecretStr


def get_deepseek_api_clients():
    load_dotenv(override=True)
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not deepseek_api_key:
        raise ValueError('[Error] 请先在 ".env" 文件内设置 "DEEPSEEK_API_KEY"')
    DeepSeek_V3 = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        api_key=SecretStr(deepseek_api_key),
    )
    DeepSeek_R1 = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        model="deepseek-reasoner",
        api_key=SecretStr(deepseek_api_key),
    )
    return DeepSeek_V3, DeepSeek_R1


# 定义浏览器上下文配置
context_config = BrowserContextConfig(
    cookies_file="data/cookies.json",
    viewport_expansion=-1,
    browser_window_size={"width": 800, "height": 600}
)

# 定义浏览器配置（无头模式）
browser_config = BrowserConfig(
    headless=True,
    new_context_config=context_config
)


def create_qcc_agent(keyword: str) -> Agent:
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("[Error] 搜索关键词不能为空！")
    qcc_url = f"https://www.qcc.com/weblogin?back=web%2Fsearch%3Fkey%3D{keyword}"
    default_actions = [{"go_to_url": {"url": qcc_url}}]
    qcc_agent_prompt = f'''
1. 调用"login_page"（获取登录页面）函数。
2. 等待30秒，直到用户完成登录并且网页跳转，再继续下一步。若当前已登录，则忽略此步骤，直接进行下一步。
3. 请点击第一条搜索结果。
4. 请总结页面中该企业的所有信息，整理归纳为JSON形式输出。
5. 调用"extract_json"（保存企业信息）函数。注意：只调用一次，然后立即继续下一步！
6. 关闭浏览器。
'''

    # 创建 Controller，并利用闭包捕获 keyword
    controller = Controller()

    @controller.action("获取登录页面")
    async def login_page(browser: Browser):
        try:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, "login_page.png")
            page = await browser.get_current_page()
            if not page:
                raise ValueError("当前页面不可用")
            await page.screenshot(path=screenshot_path)
            feedback_msg = f"[Function] 成功保存截图至 {screenshot_path}"
            print(feedback_msg)
            return feedback_msg
        except Exception as e:
            error_msg = f"[Error] 获取登录页面失败: {str(e)}"
            print(error_msg)
            raise

    @controller.action("保存企业信息")
    async def extract_json(browser: Browser, content: str):
        try:
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            extract_path = os.path.join(output_dir, f"{keyword}.json")
            with open(extract_path, "w", encoding="utf-8") as f:
                f.write(content)
            feedback_msg = f"[Function] 成功保存企业信息至 {extract_path}"
            print(feedback_msg)
            return feedback_msg
        except Exception as e:
            error_msg = f"[Error] 保存企业信息失败: {str(e)}"
            print(error_msg)
            raise

    # 创建浏览器实例与上下文
    browser = Browser(config=browser_config)
    browser_context = BrowserContext(browser=browser, config=context_config)

    # 获取最新的 DeepSeek API 客户端
    DeepSeek_V3, _ = get_deepseek_api_clients()

    # 创建 Agent 实例
    qcc_agent = Agent(
        browser_context=browser_context,
        initial_actions=default_actions,
        controller=controller,
        task=qcc_agent_prompt,
        llm=DeepSeek_V3,
        use_vision=False
    )
    return qcc_agent


async def run_agent(keyword: str):
    qcc_agent = create_qcc_agent(keyword)
    try:
        await qcc_agent.run()
    except Exception as e:
        print("[Error] qcc_agent 运行出现异常:", str(e))
        raise
    finally:
        try:
            await qcc_agent.browser_context.close()
            await qcc_agent.browser_context.browser.close()
        except Exception as e:
            print("[Error] 关闭浏览器时发生错误:", str(e))

if __name__ == "__main__":
    try:
        keyword = input("请输入搜索关键词 > ").strip()
        if not keyword:
            raise ValueError("[Error] 搜索关键词不能为空！")
        asyncio.run(run_agent(keyword))
    except Exception as e:
        print("[Error] 程序出现错误:", str(e))
