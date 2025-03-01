import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, Controller, ActionResult, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key:
    raise ValueError('请先设置DeepSeek API')

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/weblogin?back=web%2Fsearch%3Fkey%3D{keyword}'

# 定义浏览器上下文的配置
context_config = BrowserContextConfig(
    cookies_file="cookies/cookies.json",
    viewport_expansion=-1,
    browser_window_size={'width': 1024, 'height': 1024}
)

# 控制浏览器的核心行为和连接设置
browser_config = BrowserConfig(
    headless=True,
    new_context_config=context_config
)

browser_controller = Controller()


@browser_controller.action("获取登录二维码")
async def login_page(browser: Browser):
    screenshot_path = "screenshots/login_page.png"
    page = await browser.get_current_page()
    await page.screenshot(path=screenshot_path)
    return ActionResult(extracted_content=f'已保存截图到 {screenshot_path}')

default_actions = [
    {'go_to_url': {'url': qcc_url}},
]


async def qcc_agent():
    # 使用 BrowserConfig 实例化浏览器
    browser = Browser(config=browser_config)
    # 创建浏览器上下文时使用预先定义的上下文配置
    browser_context = BrowserContext(
        browser=browser,
        config=context_config
    )

    agent = Agent(
        browser_context=browser_context,
        initial_actions=default_actions,
        controller=browser_controller,
        task=(
            '''
            1. 如果提示需要登录，请调用"获取登录二维码"函数。之后保持等待，直到用户完成登录并且网页跳转，然后再进行下一步。
            2. 点击第一条搜索结果。
            3. 将页面中企业的所有信息整理归纳并以json形式导出。
            4. 关闭浏览器。
            '''
        ),
        llm=ChatOpenAI(
            base_url='https://api.deepseek.com/v1',
            model='deepseek-chat',
            api_key=SecretStr(api_key),
        ),
        use_vision=False
    )

    await agent.run()

try:
    asyncio.run(qcc_agent())
except Exception as e:
    print('Error: ', str(e))
