# Architecture

## Request flow

1. **Input guardrails.** Block obvious prompt injection and oversized input
   before any model call, so cost and risk stay bounded.
2. **HyDE expansion.** Generate a short hypothetical answer and append it to the
   query to improve recall on sparse phrasing.
3. **Hybrid retrieval.** Run dense vector search and BM25 in parallel, then fuse
   the rankings. Dense catches meaning, sparse catches exact terms and codes.
4. **Reranking.** A cross encoder scores each candidate against the query and
   keeps the top passages, which raises precision before generation.
5. **CRAG grade.** The model grades whether the retrieved context is relevant.
   A low grade can route to a web fallback or a clarification instead of a guess.
6. **Generation.** The LLM gateway calls Azure OpenAI with a grounded prompt and
   asks for citations to the supporting lines.
7. **Self RAG reflection.** The model checks whether its own answer is supported
   by the context and flags unsupported claims.
8. **Output guardrails.** Redact PII before the answer leaves the service.
9. **Observability.** Request counts, blocked counts and latency are exported to
   Prometheus at `/metrics`.

## Design choices

- A single LLM gateway means routing, retries, cost tracking and model fallback
  are added in one place rather than scattered across the codebase.
- Every external dependency has a local fallback so the pipeline runs end to end
  on a laptop with no cloud credentials, which keeps development fast.
- The graph is explicit. Each stage is a node, so adding a branch such as
  Text2SQL or a web fallback is a small, testable change.

## Compliance notes

For regulated finance the relevant controls map cleanly onto the pipeline:
input and output guardrails for data protection, CRAG and Self RAG for answer
accuracy and auditability, full tracing for the DORA expectation of operational
resilience, and documented evaluation runs for EU AI Act high risk obligations.
