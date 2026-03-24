import os
import json

from ..config   import Config
from ..logging  import Logger

from xai_sdk import Client
from xai_sdk.chat import system, user

class LLM:
    def __init__(self):
        config = Config.get()

        self.system = config.get_advisor_prompt("system")
        self.scan = config.get_advisor_prompt("scan")
        self.decide = config.get_advisor_prompt("decide")
        self.loss = config.get_advisor_prompt("loss")

        api_key = os.getenv(config.api_key)
        if not api_key:
            raise ValueError(config.api_key + "not found in environment variables!")

        Logger.get().info("API Key loaded successfully: %s...", api_key[:16])
        Logger.get().info("Model: %s", config.model)

        self.client = Client(api_key)
        self.chat = self.client.chat.create(model=config.model)
        # Pre-configure system prompt for the chat session
        self.chat.append(system(self.system))


    def ClearUserMessages(self):
        """
        Helper method to clear user messages while keeping system prompt
        """
        while self.chat.messages and self.chat.messages[-1].role != "system":
            self.chat.messages.pop()


    def ParseModelResponse(self, text: str) -> dict:
        """
        Model is expected to return a JSON string that can be parsed into a dict with the specified structure
        Remove code block markers (```json ... ```) if present, and strip leading/trailing whitespace
        """
        start = text.find('{')
        end = text.rfind('}') + 1

        if start == -1 or end == 0:
            return {}

        cleaned = text[start:end]
        Logger.get().info("Cleaned response: \n" + cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {}


    def Scan(self, text: str) -> dict:
        """
        Input: a piece of text (usually market/price description)
        Output: a json dict with fixed structure
        """
        # Before calling the model, we clear any previous user messages to ensure a clean state
        self.ClearUserMessages()

        # Generate the content for the model by combining the scan prompt with the input text
        content = self.scan + "So, analyze the following data:\n" + text

        # Require for saving the user message for debugging and traceability
        Logger.get().debug("User input for Scan:\n" + text)

        self.chat.append(user(content))
        response = self.chat.sample()
        # Require for saving the model response for debugging and traceability
        Logger.get().debug("Model response for Scan:\n" + response.content)

        result = self.ParseModelResponse(response.content)

        # Make sure to return a fixed structure (even if the model output is incorrect, fill in default values)
        return {
            "hasRange": result.get("hasRange", False),
            "upper": result.get("upper", "0"),
            "lower": result.get("lower", "0"),
            "count": result.get("count", 0),
            "type": result.get("type", "none")
        }


    def Decide(self, text: str) -> dict:
        """
        待实现：目前返回空结构，后面根据需求补充
        """
        # 类似 Scan 的调用逻辑，但使用 decide prompt
        return {
            "action": "wait",
            "reason": "待实现",
            "confidence": 0.0
        }


    def Loss(self, text: str) -> dict:
        """
        待实现：目前返回空结构，后面补充止损/风控逻辑
        """
        return {
            "should_stop": False,
            "reason": "待实现",
            "risk_level": "low"
        }


# For testing purposes
if __name__ == "__main__":
    with open(Config.get().unittest_default, "r", encoding="utf-8") as f:
        sample_text = f.read()

    llm = LLM()
    result = llm.Scan(sample_text)
    print(result)