from ..config.config import Config

# 获取配置实例（单例，所以随便哪调用都一样）
config = Config.get()           # 或者直接 Config() 也行，看你喜欢

# 使用方式
print(config.provider)          # "xai"
print(config.model)             # "grok-4-1-fast-non-reasoning"
print(config.api_key)           # "XAI_API_KEY" 或实际的密钥

# 如果要用 advisor 的 prompt
system_prompt = config.get_advisor_prompt("system")
scan_prompt   = config.get_advisor_prompt("scan")

print(system_prompt)            # 会输出 ./advisor/prompt.md 里的内容