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
    browser_window_size={"width": 1280, "height": 720}
)

# 定义浏览器配置（无头模式）
browser_config = BrowserConfig(
    headless=True,
    new_context_config=context_config
)


def create_shared_browser_context():
    # 创建一个共享的 Browser 实例
    browser = Browser(config=browser_config)
    # 基于这个浏览器实例创建一个共享的 BrowserContext
    context = BrowserContext(browser=browser, config=context_config)
    return context


def create_qcc_agent(keyword: str, shared_context: BrowserContext) -> Agent:
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("[Error] 搜索关键词不能为空！")
    qcc_url = f"https://www.qcc.com/weblogin?back=web%2Fsearch%3Fkey%3D{keyword}"

    # 创建 Controller，并利用闭包捕获 keyword
    qcc_controller = Controller()

    @qcc_controller.action("screenshot")
    async def screenshot(browser: Browser):
        try:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, "login_page.png")
            page = await browser.get_current_page()
            if not page:
                raise ValueError("[Error] 当前页面不可用")
            await page.screenshot(path=screenshot_path)
            feedback_msg = f"[Function] 成功保存截图至 {screenshot_path}"
            print(feedback_msg)
            return feedback_msg
        except Exception as e:
            error_msg = f"[Error] 获取登录页面失败: {str(e)}"
            print(error_msg)
            raise

    default_actions = [
        {"go_to_url": {"url": qcc_url}},
        {"screenshot": {}},
    ]

    # 获取最新的 DeepSeek API 客户端
    DeepSeek_V3, _ = get_deepseek_api_clients()

    qcc_agent_prompt = '''
1. 如需登录，请等待30秒，直到用户完成登录并且网页跳转。否则，请忽略此步骤。

2. 请点击第一条搜索结果。
'''

    # 创建 Agent 实例，使用共享的 BrowserContext
    qcc_agent = Agent(
        browser_context=shared_context,
        initial_actions=default_actions,
        controller=qcc_controller,
        task=qcc_agent_prompt,
        llm=DeepSeek_V3,
        use_vision=False
    )
    return qcc_agent


def create_json_agent(keyword: str, shared_context: BrowserContext) -> Agent:
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("[Error] 搜索关键词不能为空！")

    # 创建 Controller，并利用闭包捕获 keyword
    json_controller = Controller()

    @json_controller.action("保存企业信息")
    async def 保存企业信息(browser: Browser, content: str):
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

    # 获取最新的 DeepSeek API 客户端
    DeepSeek_V3, _ = get_deepseek_api_clients()

    json_agent_prompt = '''
1. 请总结页面中该企业的所有信息，整理归纳为JSON形式输出。

2. 调用"保存企业信息"函数。

3. 关闭浏览器。
'''

    # 创建 Agent 实例，使用共享的 BrowserContext
    json_agent = Agent(
        browser_context=shared_context,
        controller=json_controller,
        task=json_agent_prompt,
        llm=DeepSeek_V3,
        use_vision=False
    )
    return json_agent


async def run_agents(keyword: str):
    # 创建共享的 BrowserContext
    shared_context = create_shared_browser_context()
    qcc_agent = create_qcc_agent(keyword, shared_context)
    json_agent = create_json_agent(keyword, shared_context)
    try:
        await qcc_agent.run()
        await json_agent.run()
    except Exception as e:
        print("[Error] 运行出现异常:", str(e))
        raise
    finally:
        try:
            await shared_context.close()
            await shared_context.browser.close()
        except Exception as e:
            print("[Error] 关闭浏览器时发生错误:", str(e))

if __name__ == "__main__":
    try:
        input_keyword = input("请输入搜索关键词 > ").strip()
        if not input_keyword:
            raise ValueError("[Error] 搜索关键词不能为空！")
        asyncio.run(run_agents(input_keyword))
    except Exception as e:
        print("[Error] 程序出现错误:", str(e))
