import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv

load_dotenv()

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/web/search?key={keyword}'

DeepSeek_V3 = ChatOpenAI(
    model='deepseek-chat',
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url=os.getenv('DEEPSEEK_BASE_URL')
)

default_actions = [
    {'go_to_url': {'url': qcc_url}}
]

agent = Agent(
    task=f'''
点击“其他方式登录”
''',
    initial_actions=default_actions,
    llm=DeepSeek_V3,
)


async def main():
    await agent.run()

asyncio.run(main())
