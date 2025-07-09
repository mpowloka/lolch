from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

class LLMClient:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7, max_retries: int = 2):
        self.chat_model = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_retries=max_retries
        )

    def call(self, prompt: str, system_msg: str | None = None) -> str:
        messages = []
        if system_msg:
            messages.append({"role": "system", "content": system_msg})
        messages.append(HumanMessage(content=prompt))

        response = self.chat_model(messages)
        return response.content.strip()
