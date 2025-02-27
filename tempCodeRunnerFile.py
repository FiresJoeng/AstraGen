# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-fa1ced0470b1481696afceb9a94865d6", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "请使用简体中文回答。"},
        {"role": "user", "content": "你好。"},
    ],
    stream=False
)

print(response.choices[0].message.content)