# core/vector_memory_engine.py

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class VectorMemoryEngine:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):

        self.vector_memories = []

        self.embedder = None

        self.model_name = model_name

    # =========================
    # EMBED TEXT
    # =========================

    def _embed_text(
        self,
        text
    ):

        if self.embedder is not None:

            try:
                return self.embedder.encode(
                    text,
                    convert_to_numpy=True
                )
            except Exception:
                pass

        return np.array(
            [float(hash(text) % 1000)],
            dtype=float
        )

    # =========================
    # COSINE SIMILARITY
    # =========================

    def _cosine_similarity(
        self,
        a,
        b
    ):

        a_vec = np.array(a, dtype=float)
        b_vec = np.array(b, dtype=float)

        denom = np.linalg.norm(a_vec) * np.linalg.norm(b_vec)

        if denom == 0:

            return 0.0

        return float(np.dot(a_vec, b_vec) / denom)

    # =========================
    # STORE MEMORY
    # =========================

    def store_memory(
        self,
        text
    ):

        memory = {

            "text": text,

            "embedding": (
                self._embed_text(text)
            )
        }

        self.vector_memories.append(
            memory
        )

        return memory

    # =========================
    # SEARCH MEMORY
    # =========================

    def search_memory(
        self,
        query,
        k=5
    ):

        if not self.vector_memories:

            return []

        query_embedding = self._embed_text(
            query
        )

        scored = []

        for memory in self.vector_memories:

            similarity = self._cosine_similarity(
                memory["embedding"],
                query_embedding
            )

            scored.append(
                {
                    "memory": memory,
                    "score": similarity
                }
            )

        scored.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return [
            item["memory"]
            for item in scored[:k]
        ]
