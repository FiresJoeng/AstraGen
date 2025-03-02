import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, Controller, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY", "")
if not api_key:
    raise ValueError("请先设置DeepSeek API")

keyword = input("请输入搜索关键词 > ")
qcc_url = f"https://www.qcc.com/weblogin?back=web%2Fsearch%3Fkey%3D{keyword}"

# 定义浏览器上下文的配置
context_config = BrowserContextConfig(
    cookies_file="cookies/cookies.json",
    viewport_expansion=-1,
    browser_window_size={"width": 800, "height": 600}
)

# 控制浏览器的核心行为和连接设置
browser_config = BrowserConfig(
    headless=True,
    new_context_config=context_config
)

browser_controller = Controller()

DeepSeek_V3 = ChatOpenAI(
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    api_key=SecretStr(api_key),
)


@browser_controller.action("获取登录页面")
async def login_page(browser: Browser):
    screenshot_path = "screenshots/login_page.png"
    page = await browser.get_current_page()
    await page.screenshot(path=screenshot_path)

# 自定义一个 action 用于保存总结内容到文件


@browser_controller.action("保存总结到文件")
async def save_summary(browser: Browser, content: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "output.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"内容已保存到 {output_file}")

default_actions = [
    {"go_to_url": {"url": qcc_url}},
]

# 在原有任务的基础上，在最后一步调用自定义的保存函数
agent_prompt_1 = '''
1. 如果网页提示需要登录，请调用"获取登录页面"函数。之后持续等待30秒，直到用户完成登录并且网页跳转，然后再进行下一步。
2. 点击第一条搜索结果。
3. 使用"extract_content"操作将页面中企业的所有信息整理归纳并以JSON形式输出。
4. 调用"保存总结到文件"函数，将上一步的总结内容保存到 output/output.txt。
5. 关闭浏览器。
'''


async def qcc_agent():
    browser = Browser(config=browser_config)
    browser_context = BrowserContext(browser=browser, config=context_config)

    agent_1 = Agent(
        browser_context=browser_context,
        initial_actions=default_actions,
        controller=browser_controller,
        task=agent_prompt_1,
        llm=DeepSeek_V3,
        use_vision=False
    )

    try:
        await agent_1.run()
    finally:
        await browser_context.close()
        await browser.close()

try:
    asyncio.run(qcc_agent())
except Exception as e:
    print("Error: ", str(e))
