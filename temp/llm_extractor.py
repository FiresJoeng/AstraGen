import dashscope
from dashscope import MultiModalConversation
import json
import os

# 设置API密钥
dashscope.api_key = 'sk-14331395469f4d7191d881376f77e137'

# 读取提示词
with open('input/prompts.json', 'r', encoding='utf-8') as f:
    prompts_json = json.load(f)

IMAGE_PATH = "input/营业执照.png"
SYSTEM_PROMPT = prompts_json["system_prompt-qwen_extractor"]
USER_PROMPT = prompts_json["user_prompt-qwen_extractor"]


# 调用模型
response = MultiModalConversation.call(
    model="qwen-vl-plus",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": [{"image": IMAGE_PATH}, {"text": USER_PROMPT}]
        }
    ]
)


# 提取并保存
try:
    response_data = json.loads(str(response))
    extracted_text = response_data["output"]["choices"][0]["message"]["content"][0]["text"]
    # 移除可能存在的格式标记
    extracted_text = extracted_text.replace('```json', '').replace('```', '').strip()

    base_filename = os.path.splitext(os.path.basename(IMAGE_PATH))[0]
    output_filename = f"output/{base_filename}.json"

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(extracted_text)

    print(f"[提示] 已将提取的内容保存至 {output_filename}")

except (json.JSONDecodeError, KeyError, IndexError) as e:
    print(f"[错误] 提取内容时发生了一个错误: {e}")
except IOError as e:
    print(f"[错误] 保存到 {output_filename} 时发生了一个错误: {e}")
