import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv

load_dotenv()

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/web/search?key={keyword}'

DeepSeek_V3 = ChatOpenAI(model='deepseek-chat')

async def main():
    default_actions = [
    {'go_to_url': {'url': qcc_url, 'delay': 3}}
    ]
    agent = Agent(
        task=f'''
1. 点击"其他方式登录"
''',
        initial_actions = default_actions,
        llm=DeepSeek_V3
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
