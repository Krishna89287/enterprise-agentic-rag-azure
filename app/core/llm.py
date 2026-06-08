"""LLM gateway. Wraps Azure OpenAI behind a single entrypoint so routing,
retries, cost tracking and model fallback all live in one place."""
from app.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)


class LLMGateway:
    def __init__(self):
        self._client = None
        if settings.azure_configured:
            from langchain_openai import AzureChatOpenAI
            self._client = AzureChatOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                azure_deployment=settings.azure_openai_chat_deployment,
                temperature=0.1,
            )
        else:
            log.warning("Azure not configured, LLM gateway running in mock mode")

    def complete(self, prompt: str) -> str:
        if self._client is None:
            return "[mock answer] configure Azure OpenAI in .env to get real responses"
        return self._client.invoke(prompt).content


gateway = LLMGateway()
