import os
from pathlib import Path
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

# 上传文件并获取 file-id 和 token 信息
file_path = Path("novel.txt")
file_object = client.files.create(file=file_path, purpose="file-extract")

# 输出文件 ID 和使用的 tokens 数量
print(f"Uploaded file ID: {file_object.id}")
print(f"Used tokens for upload: {file_object.bytes}")