import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

keyword = input('请输入搜索关键词 > ')
aiqicha_url = f'https://www.aiqicha.com/s?q={keyword}'


llm = ChatOpenAI(model='deepseek-chat')

initial_actions = [ 
    {'open_tab': {'url': aiqicha_url}},
]


async def main():
    agent = Agent(
        task=f'''
请你选择第一个搜索结果,
''',
        initial_actions=initial_actions,
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
