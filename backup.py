import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/web/search?key={keyword}'

default_actions = [
    {'go_to_url': {'url': qcc_url}}
]

api_key = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key:
    raise ValueError('DEEPSEEK_API_KEY is not set')


async def run_search():
    agent = Agent(
        task=(
            f'1. 前往“{qcc_url}”'
            '2. 如果弹出登录页，请等待用户扫码登录后跳转新的页面。否则，直接执行第3步'
            '3. 点击第一个搜索结果'
        ),
        llm=ChatOpenAI(
            base_url='https://api.deepseek.com/v1',
            model='deepseek-chat',
            api_key=SecretStr(api_key),
        ),
        use_vision=False
    )

    await agent.run()

asyncio.run(run_search())
