from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatOpenAI(model='deepseek-chat')

async def main():
    agent = Agent(
        task='',
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
