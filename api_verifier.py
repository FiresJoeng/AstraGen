import os
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from dotenv import load_dotenv
load_dotenv()


def verify_deepseek_api():
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not deepseek_api_key:
        raise ValueError('[Error] 请先在 ".env" 文件内设置 "DEEPSEEK_API_KEY"')

    DeepSeek_V3 = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        api_key=SecretStr(deepseek_api_key),
    )

    # 测试API调用
    try:
        DeepSeek_V3.invoke("Test")
        print("[Info] API Key验证成功")
        return DeepSeek_V3
    except Exception as e:
        raise ValueError(f'[Error] API KEY验证失败: {str(e)}')


if __name__ == "__main__":
    verify_deepseek_api()
