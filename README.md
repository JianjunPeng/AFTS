# AFTS - Automated Futures Trading System

An automated futures trading system (experimental).

Current main functions:
- Read LLM provider/model/api_key from configuration file
- Read prompt files (system/scan/decide/loss) from the advisor phase
- (To be added later) Trading signal generation, backtesting, etc.

## Quick Start

```bash
# 1. Clone porject
git clone git@github.com:JianjunPeng/AFTS.git
cd afts

# 2. Creating a virtual environment
python -m venv .env
source .env/bin/activate

# 3. Install dependencies
pip install tqsdk xai-sdk sqlalchemy alembic

# 4. Prepare API key
Add the following line to the file .env/bin/activate: export XAI_API_KEY=xai-xxxx (enter your actual XAI API Key).

# 5. Run
python -m src.main
