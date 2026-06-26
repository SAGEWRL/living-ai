# main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import os
import time
from fastapi import Depends

# Defer importing heavy core modules until after we check LIVING_AI_SKIP_INIT
# so tests can set the env var and avoid pulling in large ML libraries at import-time.
LivingAISystem = None
# lightweight alert ingestor can be imported eagerly (no heavy ML deps)
from core.alert_ingestor import ingest_alert, ingest_structured_alert


class GoalInput(BaseModel):

    goal: str

    priority: int = 5

# =========================
# APP INIT
# =========================

app = FastAPI()

# =========================
# API KEY CONFIG
# =========================

DEFAULT_API_KEY = os.environ.get("LIVING_AI_DEFAULT_API_KEY", "demo-key")
API_KEYS = set(
    k.strip() for k in os.environ.get("LIVING_AI_API_KEYS", DEFAULT_API_KEY).split(",") if k.strip()
)


def get_request_api_key(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return request.headers.get("x-api-key") or request.query_params.get("api_key")


def validate_api_key(api_key: str):
    return bool(api_key and api_key in API_KEYS)


def require_api_key(request: Request):
    api_key = get_request_api_key(request)
    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: invalid API key"
        )
    return api_key


def require_websocket_api_key(websocket: WebSocket):
    api_key = websocket.query_params.get("api_key")
    auth_header = websocket.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        api_key = api_key or auth_header[7:].strip()
    api_key = api_key or websocket.headers.get("x-api-key")
    if not validate_api_key(api_key):
        return False
    return True


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str, request: Request):
    """Return RQ job status and result if available."""
    require_api_key(request)
    try:
        from core.queue_utils import fetch_job
        info = fetch_job(job_id)
        if info is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return info
    except ImportError:
        raise HTTPException(status_code=501, detail="RQ support not installed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# AI SYSTEM INIT
# =========================

system = None
# Allow tests or other environments to skip heavy system init at import-time by
# setting LIVING_AI_SKIP_INIT=1. Tests can then instantiate `main.system`
# explicitly when needed.
try:
    if os.environ.get("LIVING_AI_SKIP_INIT", "0") != "1":
        # import heavy modules lazily
        from core.system_engine import LivingAISystem as _LivingAISystem
        from core.alert_ingestor import ingest_alert as _ingest_alert, ingest_structured_alert as _ingest_structured_alert

        LivingAISystem = _LivingAISystem
        ingest_alert = _ingest_alert
        ingest_structured_alert = _ingest_structured_alert

        system = LivingAISystem()
except Exception:
    system = None

# If heavy init was skipped, provide a lightweight stub system for smoke tests
if system is None and os.environ.get("LIVING_AI_SKIP_INIT", "0") == "1":
    class _StubKernel:
        def __init__(self):
            self.goals = []

        def add_goal(self, goal, priority=5):
            self.goals.append({"goal": goal, "priority": priority})

        def complete_goal(self, goal):
            for g in list(self.goals):
                if g.get("goal") == goal or g == goal:
                    try:
                        self.goals.remove(g)
                    except Exception:
                        pass
                    return True
            return False

        def select_goal(self):
            return self.goals[0] if self.goals else None

    class _StubRuntimeManager:
        def get_state(self):
            return {"status": "stub", "uptime": 0}

        def start(self):
            return True

    class _StubDistributedMemory:
        def get_memory_stats(self):
            return {"short_term": 0, "long_term": 0, "priority": 0}

        def store_memory(self, *args, **kwargs):
            return True

    class _StubSystem:
        def __init__(self):
            self.identity = {"name": "StubLivingAI", "version": "stub"}
            self.identity_traits = []
            self.lessons_learned = []
            self.kernel = _StubKernel()
            self.runtime_manager = _StubRuntimeManager()
            self.distributed_memory = _StubDistributedMemory()
            self.belief_engine = type("B", (), {"beliefs": []})()
            self.autonomous_goals = []
            self.goal_evolution_history = []
            self.goal_completion_history = []

        def process(self, text):
            return {"response": f"stub response to: {text}", "active_goal": self.kernel.select_goal()}

        def start_autonomy(self, interval=5):
            return {"status": "started", "interval": interval}

        def stop_autonomy(self):
            return {"status": "stopped"}

        def get_autonomy_status(self):
            return {"running": False}

        def save_self_model(self):
            return True

        def record_goal_completion(self, goal, performance_score=0.0):
            self.goal_completion_history.append({"goal": goal, "score": performance_score})

        def _emit_event(self, t, payload):
            return True

    system = _StubSystem()

# =========================
# INPUT MODEL
# =========================

class UserInput(BaseModel):

    text: str


class AlertInput(BaseModel):

    source: str = "generic"

    payload: dict

    priority: int = 7

# =========================
# ROOT ROUTE
# =========================

@app.get("/")

def home():

    return {

        "message": "Living AI Core Running",

        "version": "6.0"
    }

# =========================
# MAIN PROCESS ROUTE
# =========================

@app.post("/process")

def process_input(
    user_input: UserInput,
    request: Request
):

    require_api_key(request)
    result = system.process(
        user_input.text
    )

    return result


# =========================
# AUTONOMY CONTROL ROUTES
# =========================

@app.post("/autonomy/start")

def start_autonomy(request: Request):

    require_api_key(request)
    result = system.start_autonomy(
        interval=5
    )

    return result


@app.post("/autonomy/stop")

def stop_autonomy(request: Request):

    require_api_key(request)
    result = system.stop_autonomy()

    return result


@app.get("/autonomy/status")

def autonomy_status(request: Request):

    require_api_key(request)
    return system.get_autonomy_status()


@app.get("/autonomy/history")

def autonomy_history(request: Request):

    require_api_key(request)
    return {

        "history": system.autonomy_history
    }


@app.get("/system/status")

def system_status(request: Request):

    require_api_key(request)
    return {

        "runtime": system.runtime_manager.get_state(),

        "autonomy": system.get_autonomy_status(),

        "goals": system.kernel.goals,

        "memory": system.distributed_memory.get_memory_stats(),

        "belief_count": len(system.belief_engine.beliefs)
    }


@app.get("/goals")

def get_goals(request: Request):

    require_api_key(request)
    return {

        "active_goals": system.kernel.goals,

        "autonomous_goals": system.autonomous_goals,

        "goal_history": system.goal_evolution_history,

        "completed_goals": system.goal_completion_history
    }


class CompleteGoalInput(BaseModel):

    goal: str


@app.post("/goals/complete")

def complete_goal(goal_input: CompleteGoalInput, request: Request):

    require_api_key(request)
    completed = system.kernel.complete_goal(
        goal_input.goal
    )

    if completed:
        system.record_goal_completion(
            goal_input.goal,
            performance_score=0.0
        )
        system.save_self_model()
        
        # Emit goal completion event
        system._emit_event("goal_completed", {
            "goal": goal_input.goal,
            "completed_at": time.time(),
            "performance_score": 0.0
        })
        
        return {
            "status": "completed",
            "goal": goal_input.goal
        }

    return {
        "status": "not_found",
        "goal": goal_input.goal
    }


@app.post("/goals/add")

def add_goal(goal_input: GoalInput, request: Request):

    require_api_key(request)
    system.kernel.add_goal(
        goal_input.goal,
        priority=goal_input.priority
    )

    system.save_self_model()

    # Emit goal added event
    system._emit_event("goal_added", {
        "goal": goal_input.goal,
        "priority": goal_input.priority,
        "added_at": time.time()
    })

    return {
        "status": "goal_added",
        "goal": goal_input.goal,
        "priority": goal_input.priority
    }


@app.get("/memory/search")

def search_memory(query: str, request: Request):

    require_api_key(request)
    return {

        "query": query,

        "results": system.semantic_memory.search(query)
    }


@app.get("/whoami")

def who_am_i(request: Request):

    require_api_key(request)
    return {

        "identity": system.identity,

        "identity_traits": system.identity_traits,

        "lessons_learned": system.lessons_learned[-10:],

        "active_goals": system.kernel.goals
    }


@app.post("/ingest_alert")
def ingest_alert_route(payload: dict, request: Request):
    """Accepts a JSON payload with `alert` and optional `priority`."""
    alert_text = payload.get("alert") if isinstance(payload, dict) else None
    priority = payload.get("priority", 7) if isinstance(payload, dict) else 7
    if not alert_text:
        return {"status": "error", "error": "missing alert field"}

    require_api_key(request)
    # import here to avoid any module-level import ordering issues
    from core.alert_ingestor import ingest_alert as _ingest_alert
    result = _ingest_alert(system, alert_text, priority=priority)
    return result


@app.post("/alerts/ingest")
def ingest_structured_alert_route(alert: AlertInput, request: Request):
    require_api_key(request)
    # import here to avoid any module-level import ordering issues
    from core.alert_ingestor import ingest_structured_alert as _ingest_structured_alert
    result = _ingest_structured_alert(
        system,
        source=alert.source,
        payload=alert.payload,
        priority=alert.priority
    )
    return result


# =========================
# DASHBOARD ROUTES
# =========================

@app.get("/dashboard")
def user_dashboard(request: Request):
    """Serve user dashboard"""
    require_api_key(request)
    dashboard_path = os.path.join(
        os.path.dirname(__file__),
        "templates",
        "cognitive_observatory.html"
    )
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"error": "Dashboard not found"}



# =========================
# WEBSOCKET CONNECTION POOL (simplified)
# =========================

websocket_connections = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that streams real-time updates.
    Simple fallback to periodic polling for stability.
    """
    if not require_websocket_api_key(websocket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    websocket_connections.add(websocket)
    
    try:
        # Send periodic updates to client
        while True:
            payload = {
                "type": "status_update",
                "active_goals": system.kernel.goals,
                "autonomy": system.get_autonomy_status(),
                "identity": system.identity,
                "timestamp": time.time()
            }
            try:
                await websocket.send_json(payload)
            except Exception:
                break
            
            # Send updates every 2 seconds
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        websocket_connections.discard(websocket)
    finally:
        websocket_connections.discard(websocket)


@app.get("/")
def root():
    """Redirect to user dashboard"""
    return {"message": "LivingAI Core Runtime", "endpoints": {
        "dashboard": "/dashboard",
        "admin_dashboard": "/admin/dashboard",
        "api_docs": "/docs",
        "goals": "/goals",
        "whoami": "/whoami",
        "process": "/process"
    }}