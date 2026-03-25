import os
#from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import system, user


import os

folder = '.'          # 当前目录  或写成 r"C:\test\cases"
# folder = "cases_folder"

case_files = [
    f for f in os.listdir(folder)
    if f.startswith('case') and os.path.isfile(os.path.join(folder, f))
]

# 得到文件名列表后，批量处理并保存为 result_case 开头
for old_name in case_files:
    # 读取原文件内容（假设是文本文件）
    old_path = os.path.join(folder, old_name)
    with open(old_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修改内容（你自己的逻辑）
    new_content = content.replace("旧", "新")   # 示例修改

    # 构造新文件名
    new_name = "result_" + old_name           # result_casexxx...
    new_path = os.path.join(folder, new_name)

    # 保存
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"已处理: {old_name} → {new_name}")



api_key = os.getenv("XAI_API_KEY")
if not api_key:
    raise ValueError("XAI_API_KEY not found in environment variables!")
print("API Key loaded successfully:", api_key[:8], "...", api_key[-8:0])

with open('./advisor/SYSTEM.md', 'r', encoding='utf-8') as fs:
    system_content = fs.read()

with open('./advisor/SCAN.md', 'r', encoding='utf-8') as fu:
    oper_content = fu.read()

with open('./usercase/autocase/SCAN/case1.md', 'r', encoding='utf-8') as ud:
    data_content = ud.read()

user_content = oper_content + "So, analyze the following data:\n" + data_content

# 写入新文件
with open('new_prompt.txt', 'w', encoding='utf-8') as f:
    f.write(system_content)
    f.write(user_content)


client = Client(api_key)

chat = client.chat.create(model="grok-4-1-fast-non-reasoning")
chat.append(system(system_content))
chat.append(user(user_content))

response = chat.sample()
print(response.content)
