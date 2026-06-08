"""LangGraph pipeline wiring the RAG stages into a state machine:
hyde -> retrieve -> rerank -> crag -> generate -> reflect.
Degrades gracefully so it runs end to end."""
from typing import TypedDict
from app.rag.retrieval import hybrid_search
from app.rag.rerank import rerank
from app.rag.hyde import hyde_expand
from app.rag.crag import grade_context
from app.rag.self_rag import reflect
from app.core.llm import gateway
from app.core.logging import get_logger

log = get_logger(__name__)


class RAGState(TypedDict, total=False):
    query: str
    expanded: str
    candidates: list
    context: str
    grade: str
    answer: str
    reflection: dict


def node_hyde(state: RAGState) -> RAGState:
    state["expanded"] = hyde_expand(state["query"])
    return state


def node_retrieve(state: RAGState) -> RAGState:
    state["candidates"] = hybrid_search(state.get("expanded", state["query"]))
    return state


def node_rerank(state: RAGState) -> RAGState:
    top = rerank(state["query"], state["candidates"])
    state["context"] = "\n".join(c["text"] for c in top)
    return state


def node_crag(state: RAGState) -> RAGState:
    state["grade"] = grade_context(state["query"], state["context"])
    return state


def node_generate(state: RAGState) -> RAGState:
    prompt = (
        "Answer the question using only the context. Cite the relevant lines.\n"
        f"Context:\n{state['context']}\n\nQuestion: {state['query']}"
    )
    state["answer"] = gateway.complete(prompt)
    return state


def node_reflect(state: RAGState) -> RAGState:
    state["reflection"] = reflect(state["answer"], state["context"])
    return state


def build_graph():
    from langgraph.graph import StateGraph, END
    g = StateGraph(RAGState)
    g.add_node("hyde", node_hyde)
    g.add_node("retrieve", node_retrieve)
    g.add_node("rerank", node_rerank)
    g.add_node("crag", node_crag)
    g.add_node("generate", node_generate)
    g.add_node("reflect", node_reflect)
    g.set_entry_point("hyde")
    g.add_edge("hyde", "retrieve")
    g.add_edge("retrieve", "rerank")
    g.add_edge("rerank", "crag")
    g.add_edge("crag", "generate")
    g.add_edge("generate", "reflect")
    g.add_edge("reflect", END)
    return g.compile()


_graph = None


def run_pipeline(query: str) -> RAGState:
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph.invoke({"query": query})
