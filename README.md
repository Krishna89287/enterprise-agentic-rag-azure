# Enterprise Agentic RAG Platform on Azure

A production minded Retrieval Augmented Generation system built as a LangGraph
state machine. It combines hybrid retrieval, cross encoder reranking, HyDE query
expansion, corrective RAG grading and Self RAG reflection, wrapped with a layered
guardrails pipeline, offline evaluation hooks and Prometheus observability. It is
designed for regulated environments such as financial services, with the EU AI Act,
BaFin, MaRisk and DORA in mind.

## Why this exists

Most RAG demos stop at "embed, retrieve, answer." Real deployments need answer
grounding, failure handling when retrieval is weak, protection against prompt
injection and PII leakage, and metrics you can put on a dashboard. This project
shows the full path from a question to a graded, guarded, observable answer.

## Architecture

```
query
  -> input guardrails (injection, length)
  -> HyDE query expansion
  -> hybrid search (dense vectors + BM25)
  -> cross encoder rerank
  -> CRAG relevance grade
  -> answer generation (Azure OpenAI via LLM gateway)
  -> Self RAG reflection (is the answer supported)
  -> output guardrails (PII redaction)
  -> response + metrics
```

See `docs/architecture.md` for the detailed flow.

## Stack

- LangGraph for the agentic control flow
- Azure OpenAI (chat + embeddings) behind a single LLM gateway, with a local
  fallback so the app runs without cloud keys
- Qdrant for vector storage, BM25 for sparse retrieval
- FastAPI service with `/chat`, `/health` and `/metrics`
- Prometheus metrics, Docker and Kubernetes manifests, Terraform for Azure
- GitHub Actions CI running the test suite

## Quickstart

```bash
make install
make run          # serves on http://localhost:8000
```

Then:

```bash
curl -s localhost:8000/health
curl -s -X POST localhost:8000/chat -H "content-type: application/json" \
  -d '{"query":"What does DORA require of financial entities?"}'
```

It runs with no credentials in mock mode. Add Azure OpenAI keys in `.env`
(see `.env.example`) for real answers.

## Run with Docker

```bash
cp .env.example .env   # fill in Azure keys
make docker            # starts the API and Qdrant
```

## Tests

```bash
make test
```

## Project layout

```
app/
  api/            FastAPI routes
  core/           LLM gateway, embeddings, logging
  rag/            graph, retrieval, rerank, hyde, crag, self_rag
  guardrails/     input and output checks
  evals/          offline evaluation hooks
  observability/  Prometheus metrics
ingest/           document ingestion pipeline
infra/            kubernetes and terraform
docs/             architecture notes
```

## Roadmap

- Swap the in memory corpus for live Qdrant upsert in the ingestion pipeline
- Add Text2SQL branch with human approval before execution
- Wire RAGAS to a labelled set and publish eval runs in CI
- Add LangSmith tracing and Grafana dashboards
- Add a web search fallback when CRAG grades context as irrelevant

## License

MIT
