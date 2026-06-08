import time
from fastapi import APIRouter
from pydantic import BaseModel
from app.config import settings
from app.rag.graph import run_pipeline
from app.guardrails import pipeline as guards
from app.observability.metrics import REQUESTS, BLOCKED, LATENCY

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    grade: str | None = None
    supported: bool | None = None
    pii_redacted: bool = False
    blocked: bool = False
    issues: list[str] = []


@router.get("/health")
def health():
    return {"status": "ok", "azure_configured": settings.azure_configured}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    REQUESTS.inc()
    start = time.time()

    if settings.enable_guardrails:
        gate = guards.check_input(req.query)
        if gate["blocked"]:
            BLOCKED.inc()
            return ChatResponse(answer="Request blocked by input guardrails.",
                                blocked=True, issues=gate["issues"])

    state = run_pipeline(req.query)
    answer = state.get("answer", "")
    out = guards.check_output(answer) if settings.enable_guardrails else {"text": answer, "pii_redacted": False}

    LATENCY.observe(time.time() - start)
    reflection = state.get("reflection") or {}
    return ChatResponse(
        answer=out["text"],
        grade=state.get("grade"),
        supported=reflection.get("supported"),
        pii_redacted=out["pii_redacted"],
    )
