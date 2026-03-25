import json
from pathlib import Path
from typing import Optional

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        config_path = Path.cwd() / "afts.json"
        
        if not config_path.is_file():
            raise FileNotFoundError(f"File not found: {config_path}")

        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)

        # LLM section
        model_config = data.get("LLM") or {}
        self.provider: str = model_config.get("provider")
        self.model: str = model_config.get("model")
        self.api_key: str = model_config.get("api_key")

        for field in ("provider", "model", "api_key"):
            if not getattr(self, field):
                raise ValueError(f"Missing required configuration items: LLM.{field}")

        # Advisor section
        advisor_config = data.get("advisor") or {}
        if not isinstance(advisor_config, dict):
            raise ValueError("advisor must be an object")

        base_dir = Path.cwd()
        prompt_config = advisor_config.get("prompt") or {}
        if not isinstance(prompt_config, dict):
            raise ValueError("advisor.prompt must be an object")

        def read_prompt_file(key: str) -> str:
            rel_path = prompt_config.get(key) or advisor_config.get(key)
            if not rel_path:
                raise ValueError(f"Missing advisor configuration: prompt.{key}")
            full_path = (base_dir / rel_path).resolve()
            if not full_path.is_file():
                raise FileNotFoundError(f"File not found: {full_path}")
            with open(full_path, encoding="utf-8") as f:
                return f.read()

        self.advisor_system = read_prompt_file("system")
        self.advisor_scan = read_prompt_file("scan")
        self.advisor_decide = read_prompt_file("decide")
        self.advisor_loss = read_prompt_file("loss")

        datalenth_config = advisor_config.get("datalenth") or {}
        if not isinstance(datalenth_config, dict):
            raise ValueError("advisor.datalenth must be an object")

        self.advisor_datalenth_scan: Optional[int] = datalenth_config.get("scan")
        self.advisor_datalenth_decide: Optional[int] = datalenth_config.get("decide")
        self.advisor_datalenth_loss: Optional[int] = datalenth_config.get("loss")

        for key, value in (
            ("scan", self.advisor_datalenth_scan),
            ("decide", self.advisor_datalenth_decide),
            ("loss", self.advisor_datalenth_loss),
        ):
            if value is None:
                raise ValueError(f"Missing advisor configuration: datalenth.{key}")
            if not isinstance(value, int):
                raise ValueError(f"advisor.datalenth.{key} must be an integer")
            
        duration_config = advisor_config.get("duration") or {}
        if not isinstance(duration_config, dict):
            raise ValueError("advisor.duration must be an object")

        self.advisor_duration_scan: Optional[int] = duration_config.get("scan")
        self.advisor_duration_decide: Optional[int] = duration_config.get("decide")
        self.advisor_duration_loss: Optional[int] = duration_config.get("loss")

        for key, value in (
            ("scan", self.advisor_duration_scan),
            ("decide", self.advisor_duration_decide),
            ("loss", self.advisor_duration_loss),
        ):
            if value is None:
                raise ValueError(f"Missing advisor configuration: duration.{key}")
            if not isinstance(value, int):
                raise ValueError(f"advisor.duration.{key} must be an integer")

        # Database section
        db_config = data.get("database") or {}
        self.db_type: str = db_config.get("type", "sqlite")
        self.db_name: str = db_config.get("name", "afts.db")
        self.db_url: str = db_config.get("url", "sqlite:///./data/afts.db")

        # TqSdk section
        tqsdk_config = data.get("tqsdk") or {}
        if not isinstance(tqsdk_config, dict):
            raise ValueError("tqsdk must be an object")

        tqsdk_auth = tqsdk_config.get("auth") or {}
        if not isinstance(tqsdk_auth, dict):
            raise ValueError("tqsdk.auth must be an object")

        self.tqsdk_auth_username: str = tqsdk_auth.get("username")
        self.tqsdk_auth_password: str = tqsdk_auth.get("password")
        self.tqsdk_auth_demotrading: bool = bool(tqsdk_auth.get("demotrading", False))

        for field in ("tqsdk_auth_username", "tqsdk_auth_password"):
            if not getattr(self, field):
                raise ValueError(f"Missing required configuration items: tqsdk.auth.{field.split('_')[-1]}")

        tqsdk_account = tqsdk_config.get("account") or {}
        if not isinstance(tqsdk_account, dict):
            raise ValueError("tqsdk.account must be an object")

        self.tqsdk_account_broker: str = tqsdk_account.get("broker")
        self.tqsdk_account_userid: str = tqsdk_account.get("userid")
        self.tqsdk_account_password: str = tqsdk_account.get("password")

        for field in ("tqsdk_account_broker", "tqsdk_account_userid", "tqsdk_account_password"):
            if not getattr(self, field):
                raise ValueError(f"Missing required configuration items: tqsdk.account.{field.split('_')[-1]}")
        self.work_mode: str = data.get("work_mode", "LIVE").upper()
        if self.work_mode not in ("DEMO", "BACKTEST", "LIVE"):
            raise ValueError("Invalid work_mode: must be one of DEMO, BACKTEST, LIVE")

        # Logging section
        logging_config = data.get("logging") or {}
        self.log_level: str = logging_config.get("level", "INFO")
        self.log_file: str = logging_config.get("file", "afts.log")
        self.log_max_size: int = logging_config.get("maxBytes", 10*1024*1024)
        self.log_backup_count: int = logging_config.get("backupCount", 5)

        # Unittest section
        unittest_config = data.get("unittest") or {}
        self.unittest_default: str = unittest_config.get("default")
        self.unittest_scanPath: str = unittest_config.get("scanPath")
        self.unittest_decidePath: str = unittest_config.get("decidePath")
        self.unittest_lossPath: str = unittest_config.get("lossPath")

    def get_advisor_prompt(self, stage: str) -> str:
        prompts = {
            "system": self.advisor_system,
            "scan":   self.advisor_scan,
            "decide": self.advisor_decide,
            "loss":   self.advisor_loss
        }
        if stage not in prompts:
            raise ValueError(f"Unknown advisor stage: {stage}")
        return prompts[stage]

    @classmethod
    def get(cls):
        return cls()
