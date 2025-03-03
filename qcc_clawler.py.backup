import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, Controller, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()


deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
if not deepseek_api_key:
    raise ValueError('请先在".env"文件内设置"DEEPSEEK_API_KEY"')

DeepSeek_V3 = ChatOpenAI(
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    api_key=SecretStr(deepseek_api_key),
)

keyword = input("请输入搜索关键词 > ")
qcc_url = f"https://www.qcc.com/weblogin?back=web%2Fsearch%3Fkey%3D{keyword}"

# 定义浏览器上下文的配置
context_config = BrowserContextConfig(
    cookies_file="cookies/cookies.json",
    viewport_expansion=-1,
    browser_window_size={"width": 800, "height": 600}
)

# 控制浏览器是否为无头模式, 连接浏览器上下文配置
browser_config = BrowserConfig(
    headless=True,
    new_context_config=context_config
)

browser_controller = Controller()


@browser_controller.action("获取登录页面")
async def login_page(browser: Browser):
    screenshot_path = "screenshots/login_page.png"
    page = await browser.get_current_page()
    await page.screenshot(path=screenshot_path)
    feedback_msg = f"[Function] Successfully Saved to {screenshot_path}."
    print(feedback_msg)
    return feedback_msg


@browser_controller.action("保存企业信息")
async def extract_json(browser: Browser, content: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    extract_path = os.path.join(output_dir, f"{keyword}.json")
    with open(extract_path, "w", encoding="utf-8") as f:
        f.write(content)
    feedback_msg = f"[Function] Successfully Saved to {extract_path}."
    print(feedback_msg)
    return feedback_msg

default_actions = [
    {"go_to_url": {"url": qcc_url}},
]

qcc_agent_prompt = f'''
1. 如果网页提示需要登录，请调用"login_page"（获取登录页）函数。如果网页不需要登录，请直接跳到第3步。
2. 之后重复等待30秒，直到用户完成登录并且网页跳转，再继续下一步。
3. 请点击第一条搜索结果。
4. 请总结页面中该企业的所有信息，整理归纳为JSON形式输出。
5. 调用"extract_json"（保存企业信息）函数。注意：只调用一次，然后立即继续下一步！
6. 关闭浏览器。
'''


async def agents():
    browser = Browser(config=browser_config)
    browser_context = BrowserContext(browser=browser, config=context_config)

    qcc_agent = Agent(
        browser_context=browser_context,
        initial_actions=default_actions,
        controller=browser_controller,
        task=qcc_agent_prompt,
        llm=DeepSeek_V3,
        use_vision=False
    )

    try:
        await qcc_agent.run()
    finally:
        await browser_context.close()
        await browser.close()

try:
    asyncio.run(agents())
except Exception as e:
    print("Error: ", str(e))
