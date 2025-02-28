from langchain_deepseek import ChatDeepSeek
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import sys

print(sys.version)
load_dotenv()

async def main():
    agent = Agent(
        task="link to 'google.com'",
        llm=ChatDeepSeek(model="deepseek-chat"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())