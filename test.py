import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv

load_dotenv()

keyword = input('请输入搜索关键词 > ')
qcc_url = f'https://www.qcc.com/web/search?key={keyword}'

DeepSeek_V3 = ChatOpenAI(model='deepseek-chat')

browser_config = BrowserConfig(
    headless=False,
    disable_security=False
)

browser = Browser(config = browser_config)

async def main():
    agent = Agent(
        task=f'''
1. 导航到指定网址：{qcc_url}
2. 识别并点击第一个搜索结果
''',
        llm=DeepSeek_V3, 
    )
    result = await agent.run()
    print(result)
    await browser.close()

asyncio.run(main())
