import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, Controller, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from pydantic import SecretStr


def get_deepseek_api_clients():
    load_dotenv(override=True)
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not deepseek_api_key:
        raise ValueError('[Error] 请先在 ".env" 文件内设置 "DEEPSEEK_API_KEY"')
    DeepSeek_V3 = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        api_key=SecretStr(deepseek_api_key),
    )
    DeepSeek_R1 = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        model="deepseek-reasoner",
        api_key=SecretStr(deepseek_api_key),
    )
    return DeepSeek_V3, DeepSeek_R1


# 定义浏览器上下文配置
context_config = BrowserContextConfig(
    cookies_file="data/cookies.json",
    viewport_expansion=-1,
    browser_window_size={"width": 1280, "height": 720}
)

# 定义浏览器配置（无头模式）
browser_config = BrowserConfig(
    headless=True,
    new_context_config=context_config
)


def create_agents_context():
    # 创建一个共享的 Browser 实例
    browser = Browser(config=browser_config)
    # 基于这个浏览器实例创建一个共享的 BrowserContext
    context = BrowserContext(browser=browser, config=context_config)
    return context


def create_qcc_agent(keyword: str, agents_context: BrowserContext) -> Agent:
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("[Error] 搜索关键词不能为空！")
    qcc_url = f"https://www.qcc.com/weblogin?back=web%2Fsearch%3Fkey%3D{keyword}"

    # 创建 Controller，并利用闭包捕获 keyword
    qcc_controller = Controller()

    @qcc_controller.action("screenshot")
    async def screenshot(browser: Browser):
        try:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, "login_page.png")
            page = await browser.get_current_page()
            if not page:
                raise ValueError("[Error] 当前页面不可用")
            await page.screenshot(path=screenshot_path)
            feedback_msg = f"[Function] 成功保存截图至 {screenshot_path}"
            print(feedback_msg)
            return feedback_msg
        except Exception as e:
            error_msg = f"[Error] 获取登录页面失败: {str(e)}"
            print(error_msg)
            raise

    qcc_actions = [
        {"go_to_url": {"url": qcc_url}},
        {"wait": {"seconds": 1}},
        {"screenshot": {}},
    ]

    # 获取最新的 DeepSeek API 客户端
    DeepSeek_V3, _ = get_deepseek_api_clients()

    qcc_agent_prompt = '''
1. 如需登录，请等待30秒，直到用户完成登录并且网页跳转。否则，请忽略此步骤。
2. 请点击第一条搜索结果。
'''

    # 创建 Agent 实例，使用共享的 BrowserContext
    qcc_agent = Agent(
        browser_context=agents_context,
        initial_actions=qcc_actions,
        controller=qcc_controller,
        task=qcc_agent_prompt,
        llm=DeepSeek_V3,
        use_vision=False
    )
    return qcc_agent


def create_json_agent(keyword: str, agents_context: BrowserContext) -> Agent:
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("[Error] 搜索关键词不能为空！")

    # 创建 Controller，并利用闭包捕获 keyword
    json_controller = Controller()

    @json_controller.action("保存企业信息")
    async def 保存企业信息(browser: Browser, content: str):
        try:
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            extract_path = os.path.join(output_dir, f"{keyword}.json")
            with open(extract_path, "w", encoding="utf-8") as f:
                f.write(content)
            feedback_msg = f"[Function] 成功保存企业信息至 {extract_path}"
            print(feedback_msg)
            return feedback_msg
        except Exception as e:
            error_msg = f"[Error] 保存企业信息失败: {str(e)}"
            print(error_msg)
            raise

    json_actions = [
        {"extract_content": {
            "goal":
            '''
请总结页面中该企业的所有信息，整理归纳为以下JSON形式输出。
    ```
    {
      "company_name": "企业名称",
      "legal_representative": "法定代表人",
      "registered_address": "注册地址",
      "company_address": "经营地址",
      "establishment_date": "成立日期",
      "registered_capital": "注册资本",
      "paid_in_capital": "实缴资本",
      "primary_account_bank": "基本户开户行",
      "company_type": "企业类型",
      "industry": "国标行业",
      "current_year_credit_policy_guidance_enterprise_types": "我行当年授信政策指引企业类型",
      "business_scope": "经营范围",
      "shareholders": [
        {
          "name": "股东名称",
          "subscribed_capital": "认缴资本",
          "paid_in_capital": "实缴资本",
          "shareholding_ratio": "持股比例",
          "subscription_date": "认缴日期"
        }
      ],
      "actual_controller": [
        {
          "name": "实际控制人名称",
          "id": "身份证号码",
          "main_experience": [
            {
              "time": "时间",
              "company": "公司",
              "position": "职务"
            }
          ]
        }
      ],
      "fund_stats": "资本金到位情况",
      "shareholders_info": "股东情况介绍",
      "equity_structure": "股权结构图",
      "key_personnel": [
        {
          "name": "姓名"
        }
      ],
      "personal_credit": "个人品行及资信记录",
      "corporate_governance": "公司治理",
      "historical_evolution": "历史沿革",
      "development_certification": "开发资质"
    }
    ```
详细要求：
    (1) 参考模板中的所有键值对是你要在网页中获取的信息；
    (2) 模板中的所有键名及顺序必须严格一致，不能有任何变动；
    (3) 如果未能抓取到某个键对应的信息，请将该键的值填为 "未知"；
    (4) 对于类似下面这种数组形式的值，可根据实际企业信息添加多个对象，具体视网页提供信息的数量而定；
    (5) 请确保最终生成的 JSON 完全符合参考模板的结构和格式。
'''
        }}
    ]

    # 获取最新的 DeepSeek API 客户端
    DeepSeek_V3, _ = get_deepseek_api_clients()

    json_agent_prompt = '''
1. 调用"保存企业信息"函数。
2. 关闭浏览器。
'''

    # 创建 Agent 实例，使用共享的 BrowserContext
    json_agent = Agent(
        browser_context=agents_context,
        initial_actions=json_actions,
        controller=json_controller,
        task=json_agent_prompt,
        llm=DeepSeek_V3,
        use_vision=False
    )
    return json_agent


async def run_agents(keyword: str):
    # 创建共享的 BrowserContext
    agents_context = create_agents_context()
    qcc_agent = create_qcc_agent(keyword, agents_context)
    json_agent = create_json_agent(keyword, agents_context)
    try:
        await qcc_agent.run()
        await json_agent.run()
    except Exception as e:
        print("[Error] 运行出现异常:", str(e))
        raise
    finally:
        try:
            await agents_context.close()
            await agents_context.browser.close()
        except Exception as e:
            print("[Error] 关闭浏览器时发生错误:", str(e))


# 底层运行逻辑，测试用
if __name__ == "__main__":
    try:
        input_keyword = input("请输入搜索关键词 > ").strip()
        if not input_keyword:
            raise ValueError("[Error] 搜索关键词不能为空！")
        asyncio.run(run_agents(input_keyword))
    except Exception as e:
        print("[Error] 程序出现错误:", str(e))
