"""Corrective RAG. Grades retrieved context for relevance. If the grade is
low the graph can trigger a web fallback or ask for clarification instead of
answering from weak context."""
from app.core.llm import gateway


def grade_context(query: str, context: str) -> str:
    prompt = (
        "Grade the context for answering the question. "
        "Reply with one word: relevant or irrelevant.\n"
        f"Question: {query}\nContext: {context}"
    )
    verdict = gateway.complete(prompt).strip().lower()
    return "relevant" if "relevant" in verdict and "irrelevant" not in verdict else "irrelevant"
