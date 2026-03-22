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

        # LLM part
        model_config = data.get("LLM") or {}
        self.provider: str = model_config.get("provider")
        self.model: str = model_config.get("model")
        self.api_key: str = model_config.get("api_key")

        for field in ("provider", "model", "api_key"):
            if not getattr(self, field):
                raise ValueError(f"Missing required configuration items: LLM.{field}")

        # advisor part
        advisor = data.get("advisor") or {}
        if not isinstance(advisor, dict):
            raise ValueError("advisor must be an object")

        base_dir = Path.cwd()

        def read_prompt_file(key: str) -> str:
            rel_path = advisor.get(key)
            if not rel_path:
                raise ValueError(f"Missing advisor configuration: {key}")
            full_path = (base_dir / rel_path).resolve()
            if not full_path.is_file():
                raise FileNotFoundError(f"File not found: {full_path}")
            with open(full_path, encoding="utf-8") as f:
                return f.read().strip()

        self.advisor_system = read_prompt_file("system")
        self.advisor_scan   = read_prompt_file("scan")
        self.advisor_decide = read_prompt_file("decide")
        self.advisor_stop   = read_prompt_file("stop")

#    @property
#    def provider(self) -> str:
#        return self.provider
#
#    @property
#    def model(self) -> str:
#        return self.model
#
#    @property
#    def api_key(self) -> str:
#        return self.api_key

    def get_advisor_prompt(self, stage: str) -> str:
        prompts = {
            "system": self.advisor_system,
            "scan":   self.advisor_scan,
            "decide": self.advisor_decide,
            "stop":   self.advisor_stop
        }
        if stage not in prompts:
            raise ValueError(f"Unknown advisor stage: {stage}")
        return prompts[stage]

    @classmethod
    def get(cls):
        return cls()
