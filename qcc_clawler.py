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
qcc_url = f'https://www.qcc.com/web/search?key={keyword}'

browser_config = BrowserContextConfig(
    cookies_file="cookies/cookies.json",
    browser_window_size={'width': 1280, 'height': 1100},
    locale='zh-CN',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
)


async def qcc_agent():

    default_actions = [
        {'go_to_url': {'url': qcc_url}},
    ]

    agent = Agent(

        browser_context=BrowserContext(
            config=browser_config, browser=Browser()),

        initial_actions=default_actions,

        task=(
            '''
            1. 检查当前网页是否存在二维码，若存在，则等待用户扫码跳转新页面，然后执行第2步；若不存在，则直接执行第2步。
            2. 点击第1条搜索结果。
            3. 检查当前网页是否存在二维码，若存在，则等待用户扫码跳转新页面，然后执行第4步；若不存在，则直接执行第4步。
            4. 总结该企业的信息。
            5. 关闭浏览器。
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
