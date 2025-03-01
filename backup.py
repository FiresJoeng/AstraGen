import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key:
    raise ValueError('DEEPSEEK_API_KEY is not set')

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/web/search?key={keyword}'


async def qcc_agent():

    default_actions = [
        {'go_to_url': {'url': qcc_url}},
    ]

    agent = Agent(
        task=(
            '1. 若提示登录，请将登录二维码保存在screenshots文件夹下'
        ),
        initial_actions=default_actions,
        llm=ChatOpenAI(
            base_url='https://api.deepseek.com/v1',
            model='deepseek-chat',
            api_key=SecretStr(api_key),
        ),
        use_vision=False
    )

    await agent.run()

asyncio.run(qcc_agent())
