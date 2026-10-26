
import json
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")

if not API_KEY or not BASE_URL:
    raise RuntimeError("请先设置环境变量 API_KEY 和 BASE_URL")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 定义模型可以调用的工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气（模拟数据）",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_page_content",
            "description": "读取指定网页 URL，提取网页中的文本内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "需要读取的网页 URL"
                    }
                },
                "required": ["url"]
            }
        }
    }
]


# 工具一：查询天气
def get_weather(city):
    weather_data = {
        "北京": {"temperature": 8, "condition": "多云"},
        "上海": {"temperature": 15, "condition": "晴"},
        "广州": {"temperature": 22, "condition": "阵雨"},
    }

    data = weather_data.get(
        city,
        {"temperature": "未知", "condition": "未知"}
    )

    return json.dumps(data, ensure_ascii=False)


# 工具二：读取网页内容
def get_page_content(url):
    try:
        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # 删除无关标签
        for tag in soup.select(
            "script, style, nav, header, footer, iframe, noscript"
        ):
            tag.decompose()

        # 提取正文
        text = (
            soup.body.get_text(separator=" ", strip=True)
            if soup.body else ""
        )

        return text[:5000]

    except requests.RequestException as e:
        return f"网页读取失败：{str(e)}"


# 工具名到 Python 函数的映射
tool_functions = {
    "get_weather": get_weather,
    "get_page_content": get_page_content
}


SYSTEM_PROMPT = """
你是一个友好的 AI 助手。
你可以查询天气，也可以读取网页内容。
当用户提供 URL 并要求读取或总结时，调用 get_page_content。
天气工具返回的是模拟数据，不是真实天气。
请记住当前聊天过程中用户告诉你的信息。
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print(f"[人设] {SYSTEM_PROMPT}")
print("输入消息开始聊天，输入 q 退出\n")


while True:
    user_input = input("你: ")

    if user_input.strip() == "q":
        break

    if not user_input.strip():
        continue

    messages.append({
        "role": "user",
        "content": user_input
    })

    # 允许连续多轮工具调用
    for _ in range(10):
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=tools
        )

        assistant_message = response.choices[0].message

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        if not assistant_message.tool_calls:
            print(f"AI: {assistant_message.content}\n")
            break

        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name

            try:
                args = json.loads(
                    tool_call.function.arguments
                )

                func = tool_functions.get(function_name)

                if func is None:
                    result = f"未知工具：{function_name}"
                else:
                    result = func(**args)

            except (ValueError, TypeError, KeyError) as e:
                result = f"工具调用失败：{str(e)}"

            print(
                f"  [调用工具] {function_name}({args if 'args' in locals() else ''}) => "
                f"{result[:200]}"
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
    else:
        print("AI: 工具调用次数达到上限，请换个问题。\n")
