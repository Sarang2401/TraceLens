import numpy as np
from typing import List, Tuple


class LocalVectorStore:
    def __init__(self):
        self.vectors = []
        self.metadata = []

    def add(self, embedding: np.ndarray, meta: dict):
        self.vectors.append(embedding)
        self.metadata.append(meta)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
        min_score: float = 0.6
    ) -> List[Tuple[dict, float]]:

        results = []
        for vec, meta in zip(self.vectors, self.metadata):
            score = float(np.dot(query_embedding, vec))
            if score >= min_score:
                results.append((meta, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
