# core/distributed_memory_manager.py

import json
import os

from core.storage_config import create_storage_backend


class DistributedMemoryManager:

    def __init__(self, storage_path="distributed_memory.json", storage_backend=None):

        self.short_term_memory = []

        self.long_term_memory = []

        self.priority_memory = []

        self.storage_path = storage_path

        self.storage_backend = storage_backend or create_storage_backend()

        self.storage_key = self._storage_key(storage_path)

        self.load_memory_store()

    def _storage_key(self, path):
        return path.replace("/", "_").replace("..", "_")

    # =========================
    # STORE MEMORY
    # =========================

    def store_memory(
        self,
        memory,
        priority="normal"
    ):

        self.short_term_memory.append(
            memory
        )

        if isinstance(memory, (str, list, dict, tuple)) and len(memory) > 20:

            self.long_term_memory.append(
                memory
            )

        if priority in [

            "high",

            "critical"
        ]:

            self.priority_memory.append(
                memory
            )

        self.save_memory_store()

    def store(self, key, value=None, priority="normal"):
        """Legacy compatible store method for simple key/value memory."""
        entry = {key: value} if value is not None else key
        self.store_memory(entry, priority=priority)

    def search(self, query):
        """Search all memory stores for query text."""
        results = []
        query_lower = str(query).lower()

        for memory_list in [
            self.short_term_memory,
            self.long_term_memory,
            self.priority_memory
        ]:
            for item in memory_list:
                try:
                    searchable = json.dumps(item)
                except Exception:
                    searchable = str(item)
                if query_lower in searchable.lower():
                    results.append(item)

        return results

    # =========================
    # GET SHORT TERM
    # =========================

    def get_short_term(self):

        return self.short_term_memory

    # =========================
    # GET LONG TERM
    # =========================

    def get_long_term(self):

        return self.long_term_memory

    # =========================
    # GET PRIORITY
    # =========================

    def get_priority_memory(self):

        return self.priority_memory

    # =========================
    # MEMORY STATS
    # =========================

    def get_memory_stats(self):

        return {

            "short_term": len(
                self.short_term_memory
            ),

            "long_term": len(
                self.long_term_memory
            ),

            "priority": len(
                self.priority_memory
            )
        }

    def load_memory_store(self):
        # Try legacy single-key store first for backward compatibility
        stored = self.storage_backend.get(self.storage_key, default=None)

        if isinstance(stored, dict):
            self.short_term_memory = stored.get("short_term_memory", [])
            self.long_term_memory = stored.get("long_term_memory", [])
            self.priority_memory = stored.get("priority_memory", [])
            return

        # If combined backend is in use, attempt to load segregated stores
        try:
            short_key = f"short:{self.storage_key}"
            long_key = f"long:{self.storage_key}"
            priority_key = f"priority:{self.storage_key}"

            short = self.storage_backend.get(short_key, default=None)
            long = self.storage_backend.get(long_key, default=None)
            priority = self.storage_backend.get(priority_key, default=None)

            if isinstance(short, list):
                self.short_term_memory = short
            if isinstance(long, list):
                self.long_term_memory = long
            if isinstance(priority, list):
                self.priority_memory = priority
        except Exception:
            # fallback to empty defaults
            self.short_term_memory = []
            self.long_term_memory = []
            self.priority_memory = []

    def save_memory_store(self):
        # Save legacy single-key for backward compatibility
        try:
            self.storage_backend.set(
                self.storage_key,
                {
                    "short_term_memory": self.short_term_memory,
                    "long_term_memory": self.long_term_memory,
                    "priority_memory": self.priority_memory,
                },
            )
        except Exception:
            pass

        # Also save segregated stores when possible
        try:
            short_key = f"short:{self.storage_key}"
            long_key = f"long:{self.storage_key}"
            priority_key = f"priority:{self.storage_key}"

            # write short-term to short/redis
            try:
                # prefer specialized helper if available
                if hasattr(self.storage_backend, "set_short"):
                    self.storage_backend.set_short(self.storage_key, self.short_term_memory)
                else:
                    self.storage_backend.set(short_key, self.short_term_memory)
            except Exception:
                pass

            # write long-term to long/postgres
            try:
                if hasattr(self.storage_backend, "set_long"):
                    self.storage_backend.set_long(self.storage_key, self.long_term_memory)
                else:
                    self.storage_backend.set(long_key, self.long_term_memory)
            except Exception:
                pass

            # priority memory
            try:
                self.storage_backend.set(priority_key, self.priority_memory)
            except Exception:
                pass
        except Exception:
            pass
