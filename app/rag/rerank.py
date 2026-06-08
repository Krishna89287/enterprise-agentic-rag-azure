"""Cross encoder reranking. Reorders candidate passages by relevance to the
query. Uses a small local cross encoder so it works offline."""
from app.core.logging import get_logger

log = get_logger(__name__)
_model = None


def rerank(query: str, candidates: list[dict], top_n: int = 3):
    global _model
    if not candidates:
        return []
    try:
        if _model is None:
            from sentence_transformers import CrossEncoder
            _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        pairs = [(query, c["text"]) for c in candidates]
        scores = _model.predict(pairs)
        for c, s in zip(candidates, scores):
            c["rerank_score"] = float(s)
        ranked = sorted(candidates, key=lambda c: c["rerank_score"], reverse=True)
    except Exception as exc:
        log.warning("reranker unavailable (%s), keeping original order", exc)
        ranked = candidates
    return ranked[:top_n]
