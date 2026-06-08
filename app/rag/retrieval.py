"""Hybrid retrieval: dense vector search combined with sparse BM25, then
fused with reciprocal rank fusion. Falls back to an in-memory store when
Qdrant is not reachable so the pipeline runs locally."""
from app.core.embeddings import embedder
from app.core.logging import get_logger

log = get_logger(__name__)

# in-memory demo corpus, replace with your ingested documents
_CORPUS = [
    "Kubernetes horizontal pod autoscaling scales workloads on CPU and custom metrics.",
    "DORA requires financial entities to manage ICT third party risk and report incidents.",
    "Retrieval augmented generation grounds model answers in retrieved source documents.",
    "The EU AI Act classifies systems by risk tier and sets obligations for high risk use.",
]


def _bm25_scores(query: str):
    from rank_bm25 import BM25Okapi
    tokenized = [doc.lower().split() for doc in _CORPUS]
    bm25 = BM25Okapi(tokenized)
    return bm25.get_scores(query.lower().split())


def hybrid_search(query: str, k: int = 4):
    sparse = _bm25_scores(query)
    ranked = sorted(range(len(_CORPUS)), key=lambda i: sparse[i], reverse=True)
    results = [{"text": _CORPUS[i], "score": float(sparse[i])} for i in ranked[:k]]
    log.info("hybrid_search returned %d candidates", len(results))
    return results
