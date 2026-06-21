import os
from core.storage import JsonStorageBackend, RedisStorageBackend, PostgresStorageBackend, CombinedStorageBackend


def create_storage_backend():
    # Support: 'json', 'redis', 'postgres', 'both'
    backend = os.environ.get("LIVING_AI_STORAGE_BACKEND", "json").lower()
    if backend == "redis":
        redis_url = os.environ.get("LIVING_AI_REDIS_URL", "redis://localhost:6379/0")
        return RedisStorageBackend(redis_url)

    if backend == "postgres":
        dsn = os.environ.get("LIVING_AI_POSTGRES_DSN", "postgresql://postgres:postgres@localhost:5432/living_ai")
        return PostgresStorageBackend(dsn)

    if backend in ("both", "combined", "redis+postgres") or os.environ.get("LIVING_AI_USE_BOTH") == "1":
        # create redis + postgres combined backend
        redis_url = os.environ.get("LIVING_AI_REDIS_URL", "redis://localhost:6379/0")
        dsn = os.environ.get("LIVING_AI_POSTGRES_DSN", "postgresql://postgres:postgres@localhost:5432/living_ai")
        redis = RedisStorageBackend(redis_url)
        pg = PostgresStorageBackend(dsn)
        default = os.environ.get("LIVING_AI_COMBINED_DEFAULT", "redis")
        return CombinedStorageBackend(redis, pg, default=default)

    # default: json filesystem storage
    return JsonStorageBackend(os.environ.get("LIVING_AI_JSON_STORAGE_DIR", "data"))
