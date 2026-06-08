"""LLM gateway. Priority: Azure if configured, else Groq (free), else mock."""
import os
from app.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)


class LLMGateway:
    def __init__(self):
        self._client = None
        self.mode = "mock"
        if settings.azure_configured:
            from langchain_openai import AzureChatOpenAI
            self._client = AzureChatOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                azure_deployment=settings.azure_openai_chat_deployment,
                temperature=0.1,
            )
            self.mode = "azure"
        elif settings.groq_configured:
            os.environ["GROQ_API_KEY"] = settings.groq_api_key
            from langchain_groq import ChatGroq
            self._client = ChatGroq(model=settings.groq_model, temperature=0.1)
            self.mode = "groq"
        else:
            log.warning("No LLM key found, running in mock mode")

    def complete(self, prompt: str) -> str:
        if self._client is None:
            return "[mock answer] add GROQ_API_KEY in .env for real answers"
        return self._client.invoke(prompt).content


gateway = LLMGateway()
