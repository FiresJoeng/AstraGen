import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/web/search?key={keyword}'

DeepSeek_V3 = ChatOpenAI(
    model='deepseek-chat',
    api_key=SecretStr(os.getenv('DEEPSEEK_API_KEY')),
    base_url=os.getenv('DEEPSEEK_BASE_URL')
)

default_actions = [
    {'go_to_url': {'url': qcc_url}}
]

async def main():
    agent = Agent(
    task=f'''
    点击第一个搜索结果.
    ''',
    initial_actions=default_actions,
    llm=DeepSeek_V3,
)
    result = await agent.run()
    print(result)

asyncio.run(main())
