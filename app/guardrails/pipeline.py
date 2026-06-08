"""Layered guardrails. Input checks run before retrieval, output checks run
before the answer is returned. Each layer is independent so you can enable or
disable them per environment."""
import re
from app.core.logging import get_logger

log = get_logger(__name__)

_PII = re.compile(r"\b(\d{3}-\d{2}-\d{4}|\d{16}|[\w.+-]+@[\w-]+\.[\w.]+)\b")
_INJECTION = re.compile(r"(ignore (previous|all) instructions|system prompt|jailbreak)", re.I)


def check_input(text: str) -> dict:
    issues = []
    if _INJECTION.search(text):
        issues.append("possible prompt injection")
    if len(text) > 8000:
        issues.append("input too long")
    return {"blocked": bool(issues), "issues": issues}


def redact_pii(text: str) -> str:
    return _PII.sub("[REDACTED]", text)


def check_output(text: str) -> dict:
    redacted = redact_pii(text)
    return {"text": redacted, "pii_redacted": redacted != text}
