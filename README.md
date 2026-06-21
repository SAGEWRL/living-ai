# Living AI Framework

## Overview

Living AI is a cognitive AI architecture that models a persistent, adaptive agent rather than a simple request/response bot. It combines memory, beliefs, goals, planning, decision-making, simulation, emotion, reflection, and learning into a single runtime.

## Features

- Semantic and vector memory storage
- Distributed memory persistence
- Belief extraction and worldview inference
- Goal selection and planner integration
- Emotion detection and behavior adaptation
- Simulation of future scenarios
- Reflection and learning from execution results
- Structured response generation

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the interactive agent

```bash
python run_ai.py
```

Then type a prompt like:

```text
YOU: Analyze our latest incident and suggest next steps
```

### Run the API server

```bash
uvicorn main:app --reload
```

## Developer Usage

### Direct Python access

```python
from core.system_engine import LivingAISystem

ai = LivingAISystem()
result = ai.process("What should I do next?")
print(result["response"])
print(result["active_goal"])
print(result["emotion"])
```

### FastAPI integration

```python
from fastapi import FastAPI
from core.system_engine import LivingAISystem

app = FastAPI()
ai = LivingAISystem()

@app.post("/ask")
def ask(payload: dict):
    return ai.process(payload["text"])
```

## API Endpoints

- `GET /` — health check
- `POST /process` — submit user input and receive a system response
- `POST /autonomy/start` — start the autonomous background cycle
- `POST /autonomy/stop` — stop the autonomous background cycle
- `GET /autonomy/status` — view autonomy runtime state
- `GET /autonomy/history` — view autonomous cycle history
- `GET /system/status` — view runtime, memory, goals, and belief status
- `GET /goals` — view active goals and autonomous goals
- `POST /goals/add` — add a goal to the cognitive kernel
- `GET /memory/search?query=...` — search semantic memory

## Persistence

The system persists key runtime data to disk:

- `semantic_memory.json` — semantic memory items and vector embeddings
- `distributed_memory.json` — short-term, long-term, and priority memories
- `self_model.json` — identity state, goals, and learned traits

## Run with Docker Compose (recommended for scaled local runs)

This project includes a `Dockerfile` and `docker-compose.yml` to run Redis, an RQ worker, and the API.

1. Build and start the stack:

```bash
./run-compose.sh
```

Or on Windows:

```powershell
run-compose.bat
```

2. The API will be available on `http://localhost:8000`.

3. Use the `/jobs/{job_id}` endpoint to check queued RQ job status.

Environment variables (can be set in `docker-compose.yml` or your environment):

- `LIVING_AI_STORAGE_BACKEND` — `redis` to use Redis, or `json` for filesystem fallback
- `LIVING_AI_REDIS_URL` — Redis connection URL
- `LIVING_AI_USE_QUEUE` — `1` to enable RQ enqueueing for heavy tasks
 - `LIVING_AI_POSTGRES_DSN` — Postgres DSN when using Postgres or combined mode
 - `LIVING_AI_STORAGE_BACKEND` — `redis`, `postgres`, `json`, or `both` to use combined Redis (short-term) + Postgres (long-term)


## Notes

This repository is a prototype cognitive agent runtime for experimentation and architecture development. It is designed to demonstrate how multiple AI subsystems can be composed into a single adaptive system, rather than serving as a finished production product.

