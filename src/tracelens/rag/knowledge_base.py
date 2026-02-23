import json
from pathlib import Path
from typing import List
from tracelens.rag.schema import FailurePattern
from tracelens.rag.embeddings import EmbeddingModel
from tracelens.rag.vector_store import LocalVectorStore


class FailureKnowledgeBase:
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.store = LocalVectorStore()
        self._load()

    def _load(self):
        data = json.loads(self.kb_path.read_text())

        patterns: List[FailurePattern] = [
            FailurePattern(**item) for item in data
        ]

        texts = [
            f"{p.name}. {p.description}. Signals: {', '.join(p.signals)}"
            for p in patterns
        ]

        embeddings = EmbeddingModel.embed(texts)

        for emb, pattern in zip(embeddings, patterns):
            self.store.add(
                embedding=emb,
                meta=pattern.model_dump()
            )

    def retrieve(self, timeline_events: List[str]):
        query_text = " ".join(timeline_events)
        query_embedding = EmbeddingModel.embed([query_text])[0]
        return self.store.search(query_embedding)
