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

        def read_prompt_file(key: str) -> str:
            rel_path = advisor_config.get(key)
            if not rel_path:
                raise ValueError(f"Missing advisor configuration: {key}")
            full_path = (base_dir / rel_path).resolve()
            if not full_path.is_file():
                raise FileNotFoundError(f"File not found: {full_path}")
            with open(full_path, encoding="utf-8") as f:
                return f.read()

        self.advisor_system = read_prompt_file("system")
        self.advisor_scan   = read_prompt_file("scan")
        self.advisor_decide = read_prompt_file("decide")
        self.advisor_loss   = read_prompt_file("loss")

        # Database section
        db_config = data.get("database") or {}
        self.db_type: str = db_config.get("type")
        self.db_name: str = db_config.get("name")

        # Logging section
        logging_config = data.get("logging") or {}
        self.log_level: str = logging_config.get("level")
        self.log_file: str = logging_config.get("file")

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
