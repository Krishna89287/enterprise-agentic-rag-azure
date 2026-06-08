"""Document ingestion: load, chunk, embed and index into the vector store.
Run as: python -m ingest.pipeline path/to/docs"""
import sys
from pathlib import Path
from app.core.embeddings import embedder
from app.core.logging import get_logger

log = get_logger(__name__)


def chunk(text: str, size: int = 800, overlap: int = 160):
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step) if text[i:i + size].strip()]


def ingest(folder: str):
    files = list(Path(folder).glob("**/*.txt")) + list(Path(folder).glob("**/*.md"))
    total = 0
    for f in files:
        chunks = chunk(f.read_text(encoding="utf-8", errors="ignore"))
        for c in chunks:
            embedder.embed(c)  # replace with upsert into Qdrant
            total += 1
        log.info("ingested %s into %d chunks", f.name, len(chunks))
    log.info("done, %d chunks total", total)


if __name__ == "__main__":
    ingest(sys.argv[1] if len(sys.argv) > 1 else "data")
