from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.api.routes import router
from app.core.logging import get_logger

log = get_logger(__name__)
app = FastAPI(title="Enterprise Agentic RAG Platform", version="0.1.0")
app.include_router(router)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
def startup():
    log.info("Enterprise Agentic RAG Platform started")
