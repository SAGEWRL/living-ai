Release v0.2.0 - Dual storage and queueing

Changes:
- Added `PostgresStorageBackend` for long-term persistent storage (JSONB).
- Added `CombinedStorageBackend` routing: short-term (Redis) and long-term (Postgres).
- Updated `storage_config.create_storage_backend()` to support `both` mode.
- Modified `DistributedMemoryManager` and `SemanticMemory` to support segregated short/long stores while preserving legacy single-key behavior.
- Added Docker Compose service for Postgres and configured `web` and `worker` to use combined backend.
- Added job-status API and observatory improvements.

Notes:
- To run locally, start Docker Compose (Redis + Postgres + app + worker):

```bash
./run-compose.sh
```

- After starting, verify:
  - API at http://localhost:8000
  - Observatory at http://localhost:8000/dashboard?api_key=demo-key

Changelog and migration notes are included in the full README.
