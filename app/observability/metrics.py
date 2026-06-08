"""Prometheus metrics. Exposes request counts and latency for the chat path."""
from prometheus_client import Counter, Histogram

REQUESTS = Counter("rag_requests_total", "Total RAG requests")
BLOCKED = Counter("rag_blocked_total", "Requests blocked by guardrails")
LATENCY = Histogram("rag_request_seconds", "RAG request latency in seconds")
