import os
from openai import OpenAI

# 从环境变量中获取 DashScope API Key
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("Please set the DASHSCOPE_API_KEY environment variable.")

# 创建 OpenAI 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 流式对话
def stream_chat(file_id):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "system", "content": f"fileid://{file_id}"},
    ]

    total_tokens_used = 0

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting the chat.")
            break

        messages.append({"role": "user", "content": user_input})

        completion = client.chat.completions.create(
            model="qwen-long",
            messages=messages,
            stream=True,
            stream_options={"include_usage": True}
        )

        print("Assistant:", end=" ", flush=True)
        for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices:
                if hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta:
                    if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                        print(chunk.choices[0].delta.content, end="", flush=True)
            if hasattr(chunk, 'usage') and chunk.usage is not None:
                total_tokens_used += chunk.usage.total_tokens
        print()  # 换行

        print(f"Total tokens used: {total_tokens_used}\n")

if __name__ == "__main__":
    file_id = input("Please enter the file ID: ")
    stream_chat(file_id)