"""Offline evaluation hooks. Wire these to a labelled set to track retrieval
recall and answer faithfulness across changes. Stubbed so CI can import it."""


def evaluate(samples: list[dict]) -> dict:
    # samples: [{"query":..., "answer":..., "context":..., "ground_truth":...}]
    if not samples:
        return {"count": 0}
    faithful = sum(1 for s in samples if s.get("ground_truth", "").lower() in s.get("answer", "").lower())
    return {"count": len(samples), "faithfulness": round(faithful / len(samples), 3)}
