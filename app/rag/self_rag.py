"""Self RAG reflection. After drafting an answer the model checks whether the
answer is supported by the context and flags unsupported claims."""
from app.core.llm import gateway


def reflect(answer: str, context: str) -> dict:
    prompt = (
        "Is the answer fully supported by the context? "
        "Reply yes or no and a one line reason.\n"
        f"Answer: {answer}\nContext: {context}"
    )
    verdict = gateway.complete(prompt)
    return {"supported": verdict.lower().startswith("yes"), "note": verdict}
