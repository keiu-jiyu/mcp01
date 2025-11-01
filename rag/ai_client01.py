import json
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Message
from dotenv import load_dotenv
import os

load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def call_add(a: float, b: float) -> float:
    """调用 add 工具"""
    return a + b


def chat_with_ai(user_message: str):
    """与通义千问聊天 - 支持工具调用"""
    print(f"\n👤 用户: {user_message}\n")

    messages = [
        Message(role="user", content=user_message)
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "add",
                "description": "两个数字相加",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            }
        }
    ]

    try:
        response = Generation.call(
            model="qwen-max",
            api_key=DASHSCOPE_API_KEY,
            messages=messages,
            tools=tools
        )

        print(f"📊 AI 响应状态码: {response.status_code}")

        if response.output.choices[0].finish_reason == "tool_calls":
            print("🔧 AI 决定调用工具\n")

            tool_calls = response.output.choices[0].message.tool_calls

            for tool_call in tool_calls:
                # ✅ 改成字典访问
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])
                tool_id = tool_call["id"]

                print(f"🛠️ 调用工具: {tool_name}")
                print(f"📥 参数: {tool_args}\n")

                if tool_name == "add":
                    result = call_add(tool_args["a"], tool_args["b"])
                    print(f"✅ 工具结果: {result}\n")

                    messages.append(Message(
                        role="assistant",
                        content=response.output.choices[0].message.content,
                        tool_calls=tool_calls
                    ))

                    messages.append(Message(
                        role="tool",
                        content=json.dumps({"result": result}),
                        tool_call_id=tool_id
                    ))

                    response2 = Generation.call(
                        model="qwen-max",
                        api_key=DASHSCOPE_API_KEY,
                        messages=messages,
                        tools=tools
                    )

                    print(f"🤖 最终答案: {response2.output.choices[0].message.content}\n")
        else:
            print(f"🤖 AI: {response.output.choices[0].message.content}\n")

    except Exception as e:
        import traceback
        print(f"❌ 错误: {type(e).__name__}: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    chat_with_ai("计算 5 加 3")
