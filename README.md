# AFTS - Automated Futures Trading System

一个自动化的金融交易辅助系统（实验性质）。

目前主要功能：
- 从配置文件读取 LLM provider / model / api_key
- 读取 advisor 阶段的 prompt 文件（system / scan / decide / stop）
- （后续会加上）交易信号生成、回测等

## 快速开始

```bash
# 1. 克隆项目
git clone git@github.com:JianjunPeng/AFTS.git
cd afts

# 2. 创建虚拟环境（推荐）
python -m venv .env
source .env/bin/activate

# 3. 安装依赖
pip install tqsdk xai-sdk

# 4. 准备API key
在文件 .env/bin/activate 增加 export XAI_API_KEY=xai-xxxx（填写你的真实 XAI API Key）

# 5. 运行
python -m src.main
