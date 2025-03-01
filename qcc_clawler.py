import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.browser.browser import Browser
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


async def login_page(agent: Agent):
    screenshot_path = "screenshot/login_page.png"
    page = agent.browser_context.page
    await page.screenshot(path=screenshot_path)
    return screenshot_path


async def qcc_agent():
    default_actions = [
        {'go_to_url': {'url': qcc_url}},
    ]
    agent = Agent(
        browser_context=BrowserContext(
            config=browser_config, browser=Browser()),
        initial_actions=default_actions,
        custom_functions={
            "login": login_page
        },
        task=(
            '''
            1. 如果提示需要登录，请调用"login"函数。然后持续等待，直到用户完成登录并使得网页自动跳转，然后再进行下一步。否则，请直接进行下一步。
            2. 点击第一条搜索结果。
            3. 总结该企业的信息。
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
    result = await agent.run()
    print(result)


try:
    asyncio.run(qcc_agent())
except Exception as e:
    print('Error: ', str(e))
