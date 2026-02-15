from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingModel:
    _model = None

    @classmethod
    def load(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model

    @classmethod
    def embed(cls, texts: List[str]) -> np.ndarray:
        model = cls.load()
        return model.encode(texts, normalize_embeddings=True)
