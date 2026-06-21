# core/semantic_memory.py

import json
import os

from core.storage_config import create_storage_backend

from core.vector_memory_engine import VectorMemoryEngine


class SemanticMemory:

    def __init__(self, storage_path="semantic_memory.json", storage_backend=None):

        self.memories = []

        self.vector_engine = VectorMemoryEngine()

        self.storage_path = storage_path

        self.storage_backend = storage_backend or create_storage_backend()

        self.storage_key = self._storage_key(storage_path)

        self.load_memories()

    def _storage_key(self, path):
        return path.replace("/", "_").replace("..", "_")

    # =========================
    # ADD MEMORY
    # =========================

    def add_memory(

        self,
        text

    ):

        self.memories.append(text)

        self.vector_engine.store_memory(text)

        self.save_memories()

    # =========================
    # STORE MEMORY
    # =========================

    def store_memory(

        self,
        text

    ):

        self.add_memory(text)

    # =========================
    # SEARCH MEMORY
    # =========================

    def search_memory(

        self,
        query

    ):

        results = []

        for memory in self.memories:

            if query.lower() in memory.lower():

                results.append(memory)

        vector_matches = [
            item["text"]
            for item in self.vector_engine.search_memory(query)
        ]

        for memory in vector_matches:

            if memory not in results:

                results.append(memory)

        return results[:5]

    # =========================
    # PERSISTENCE
    # =========================

    def load_memories(self):
        # Try legacy single-key first
        stored = self.storage_backend.get(self.storage_key, default=None)
        if isinstance(stored, list):
            self.memories = stored
            for text in self.memories:
                self.vector_engine.store_memory(text)
            return

        # Try long-term prefixed store when available
        try:
            long_key = f"long:{self.storage_key}"
            stored_long = self.storage_backend.get(long_key, default=None)
            if isinstance(stored_long, list):
                self.memories = stored_long
                for text in self.memories:
                    self.vector_engine.store_memory(text)
        except Exception:
            # fallback to empty
            self.memories = []

    def save_memories(self):
        # Write legacy key for compatibility
        try:
            self.storage_backend.set(self.storage_key, self.memories)
        except Exception:
            pass

        # Write to long-term store if available
        try:
            long_key = f"long:{self.storage_key}"
            # prefer helper if available
            if hasattr(self.storage_backend, "set_long"):
                self.storage_backend.set_long(self.storage_key, self.memories)
            else:
                self.storage_backend.set(long_key, self.memories)
        except Exception:
            pass

    # =========================
    # ALIAS SEARCH
    # =========================

    def search(

        self,
        query

    ):

        return self.search_memory(query)

    # =========================
    # GET MEMORIES
    # =========================

    def get_memories(self):

        return self.memories