import os
from xai_sdk import Client
from xai_sdk.chat import system, user


api_key = os.getenv("XAI_API_KEY")
if not api_key:
    raise ValueError("XAI_API_KEY not found in environment variables!")
print("API Key loaded successfully:", api_key[:8])

with open('./model/prompt.md', 'r', encoding='utf-8') as fs:
    system_content = fs.read()

with open('./model/SCAN.md', 'r', encoding='utf-8') as fu:
    oper_content = fu.read()

with open('./usercase/autocase/case1.md', 'r', encoding='utf-8') as ud:
    data_content = ud.read()

user_content = oper_content + "So, analyze the following data:\n" + data_content

# Record the prompt for future reference
with open('./usercase/autocase/prompt_case1.md', 'w', encoding='utf-8') as f:
    f.write(system_content)
    f.write(user_content)


client = Client(api_key)

chat = client.chat.create(model="grok-4-1-fast-non-reasoning")
chat.append(system(system_content))
chat.append(user(user_content))

response = chat.sample()
print(response.content)
with open('./usercase/autocase/response_case1.md', 'w', encoding='utf-8') as f:
    f.write(response.content)
