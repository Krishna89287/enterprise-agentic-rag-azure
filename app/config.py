from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_api_version: str = "2024-06-01"
    azure_openai_chat_deployment: str = "gpt-4o"
    azure_openai_embed_deployment: str = "text-embedding-3-large"

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_docs"

    log_level: str = "INFO"
    enable_guardrails: bool = True

    @property
    def azure_configured(self) -> bool:
        return bool(self.azure_openai_endpoint and self.azure_openai_api_key)

    @property
    def groq_configured(self) -> bool:
        return bool(self.groq_api_key)


settings = Settings()
