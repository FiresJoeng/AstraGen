import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, Controller, ActionResult
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key:
    raise ValueError('DEEPSEEK_API_KEY is not set')

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/weblogin?back=web%2Fsearch%3Fkey%3D{keyword}'

browser_config = BrowserContextConfig(
    cookies_file="cookies/cookies.json"
)

browser_controller = Controller()

@browser_controller.action("获取登录二维码")
async def login_page(browser: Browser):
    screenshot_path = "screenshots/login_page.png"
    page = await browser.get_current_page()
    await page.screenshot(path=screenshot_path)
    return ActionResult(extracted_content=f'已保存截图到 {screenshot_path}')


async def qcc_agent():
    default_actions = [
        {'go_to_url': {'url': qcc_url}},
    ]
    agent = Agent(
        browser_context=BrowserContext(
            config=browser_config, browser=Browser()),
        initial_actions=default_actions,
        controller=browser_controller,
        task=(
            '''
            1. 如果提示需要登录，请调用"获取登录二维码"函数。之后保持等待，直到用户完成登录并且网页跳转，然后再进行下一步。
            2. 点击第一条搜索结果。
            3. 使用"extract_content"方法，将页面中企业的所有信息整理归纳并以json形式导出。
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
