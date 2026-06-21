import abc
import json
import os


class StorageBackend(abc.ABC):

    @abc.abstractmethod
    def get(self, key, default=None):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass

    @abc.abstractmethod
    def delete(self, key):
        pass

    @abc.abstractmethod
    def exists(self, key):
        pass


class JsonStorageBackend(StorageBackend):

    def __init__(self, directory="data"):
        self.directory = os.path.abspath(directory)
        os.makedirs(self.directory, exist_ok=True)

    def _path(self, key):
        safe_key = key.replace("/", "_").replace("..", "")
        return os.path.join(self.directory, f"{safe_key}.json")

    def get(self, key, default=None):
        path = self._path(key)
        if not os.path.exists(path):
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def set(self, key, value):
        path = self._path(key)
        tmp_path = f"{path}.tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(value, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
            return True
        except Exception:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
            return False

    def delete(self, key):
        path = self._path(key)
        try:
            if os.path.exists(path):
                os.remove(path)
            return True
        except Exception:
            return False

    def exists(self, key):
        return os.path.exists(self._path(key))


class RedisStorageBackend(StorageBackend):

    def __init__(self, url="redis://localhost:6379/0"):
        try:
            import redis
        except ImportError as exc:
            raise ImportError(
                "Redis support requires the 'redis' package. "
                "Install it with 'pip install redis'."
            ) from exc
        self.client = redis.Redis.from_url(url, decode_responses=True)

    def get(self, key, default=None):
        value = self.client.get(key)
        if value is None:
            return default
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def set(self, key, value):
        payload = json.dumps(value)
        return self.client.set(key, payload)

    def delete(self, key):
        return self.client.delete(key) == 1

    def exists(self, key):
        return self.client.exists(key) == 1


class PostgresStorageBackend(StorageBackend):

    def __init__(self, dsn=None):
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError as exc:
            raise ImportError(
                "Postgres support requires the 'psycopg2-binary' package. "
                "Install it with 'pip install psycopg2-binary'."
            ) from exc

        self.dsn = dsn or "postgresql://postgres:postgres@localhost:5432/living_ai"
        # create a connection for simple sync operations
        self.conn = psycopg2.connect(self.dsn)
        self.conn.autocommit = True
        self._ensure_table()

    def _ensure_table(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS kv_store (
                    key TEXT PRIMARY KEY,
                    value JSONB
                )
                """
            )

    def get(self, key, default=None):
        with self.conn.cursor() as cur:
            cur.execute("SELECT value FROM kv_store WHERE key = %s", (key,))
            row = cur.fetchone()
            if not row:
                return default
            return row[0]

    def set(self, key, value):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO kv_store (key, value) VALUES (%s, %s) "
                "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                (key, json.dumps(value)),
            )
        return True

    def delete(self, key):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM kv_store WHERE key = %s", (key,))
            return cur.rowcount > 0

    def exists(self, key):
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM kv_store WHERE key = %s", (key,))
            return cur.fetchone() is not None


class CombinedStorageBackend(StorageBackend):
    """Route short-term keys to Redis and long-term to Postgres.

    Keys starting with 'long:' or 'ltm:' will go to Postgres. Keys starting
    with 'short:' or 'stm:' will go to Redis. If no prefix is present, the
    default_backend param decides (defaults to redis).
    """

    def __init__(self, redis_backend: RedisStorageBackend, postgres_backend: PostgresStorageBackend, default="redis"):
        self.redis = redis_backend
        self.postgres = postgres_backend
        self.default = default

    def _route(self, key):
        if isinstance(key, str):
            lk = key.lower()
            if lk.startswith("long:") or lk.startswith("ltm:"):
                return self.postgres
            if lk.startswith("short:") or lk.startswith("stm:"):
                return self.redis
        return self.redis if self.default == "redis" else self.postgres

    def get(self, key, default=None):
        return self._route(key).get(key, default=default)

    def set(self, key, value):
        return self._route(key).set(key, value)

    def delete(self, key):
        return self._route(key).delete(key)

    def exists(self, key):
        return self._route(key).exists(key)

    # Convenience helpers
    def set_short(self, key, value):
        return self.redis.set(f"short:{key}", value)

    def get_short(self, key, default=None):
        return self.redis.get(f"short:{key}", default=default)

    def set_long(self, key, value):
        return self.postgres.set(f"long:{key}", value)

    def get_long(self, key, default=None):
        return self.postgres.get(f"long:{key}", default=default)
