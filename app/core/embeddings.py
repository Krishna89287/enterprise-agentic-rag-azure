"""Embedding provider. Azure when configured, otherwise a local
sentence-transformers model so the app runs without cloud credentials."""
from app.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)


class Embedder:
    def __init__(self):
        self._azure = None
        self._local = None
        if settings.azure_configured:
            from langchain_openai import AzureOpenAIEmbeddings
            self._azure = AzureOpenAIEmbeddings(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                azure_deployment=settings.azure_openai_embed_deployment,
            )

    def embed(self, text: str):
        if self._azure is not None:
            return self._azure.embed_query(text)
        if self._local is None:
            from sentence_transformers import SentenceTransformer
            self._local = SentenceTransformer("all-MiniLM-L6-v2")
        return self._local.encode(text).tolist()


embedder = Embedder()
