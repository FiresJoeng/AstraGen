# 导入依赖
from openai import OpenAI
import os
from pathlib import Path
import json


# 读取提示词
with open('input/prompts.json', 'r', encoding='utf-8') as f:
    prompts_json = json.load(f)

IMAGE_PATH = "input/营业执照.png"

SYSTEM_PROMPT = '''你是一名专业的营业执照信息提取助手。
请仔细分析用户上传的营业执照图片，准确提取以下信息：
- 公司名称
- 注册号
- 法定代表人
- 成立日期
请以Markdown格式返回。
如果缺失某项信息，请忽略该项。
不要添加多余的说明或内容。
'''

USER_PROMPT = prompts_json["prompt-qwen_extractor"]


# 主函数
def main():
    # 初始化客户端
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 上传图片文件，返回 file-id
    file_object = client.files.create(
        file=Path(IMAGE_PATH), purpose="file-extract"
    )
    file_id = file_object.id
    print(f"上传文件成功，file_id: {file_id}")

    # 调用 chat 接口，传入 file-id
    completion = client.chat.completions.create(
        model="qwen3-30b-a3b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"file-id://{file_id}"
                            }
                        },
                    {
                            "type": "text",
                            "text": USER_PROMPT
                            }
                ]
            }
        ],
        extra_body={"enable_thinking": False}
    )

    # 打印结果，使用标准 JSON 打印确保中文等正常显示
    print(json.dumps(completion.model_dump(), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
