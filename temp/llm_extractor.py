from dashscope import MultiModalConversation
import json

with open('input/prompts.json', 'r', encoding='utf-8') as f:
    prompts_json = json.load(f)

IMAGE = "input/营业执照.png"
PROMPT = prompts_json["prompt-qwen_extractor"]
MAPPING = None

response = MultiModalConversation.call(
    model="qwen-vl-plus",
    messages=[
        {"role": "user", "content": [
            {"image": IMAGE},
            {"text": PROMPT}
        ]}
    ]
)

print(response)
