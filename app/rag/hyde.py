"""HyDE: generate a hypothetical answer to the query and use it to widen
retrieval recall, then retrieve against the expanded text."""
from app.core.llm import gateway


def hyde_expand(query: str) -> str:
    prompt = f"Write a short factual passage that would answer this question:\n{query}"
    return query + " " + gateway.complete(prompt)
