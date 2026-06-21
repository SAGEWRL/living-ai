import os
import subprocess
import os


def _get_redis_conn():
    try:
        import redis
    except ImportError:
        raise ImportError("Install redis package to use task queue")
    url = os.environ.get("LIVING_AI_REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(url, decode_responses=True)


def _get_queue():
    try:
        from rq import Queue
    except ImportError:
        raise ImportError("Install rq package to use task queue")
    conn = _get_redis_conn()
    return Queue("livingai", connection=conn)


def run_shell_command(command):
    """Worker-callable function to run a shell command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_python_script(script_path):
    """Worker-callable function to run a Python script."""
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def enqueue_command(command):
    q = _get_queue()
    job = q.enqueue(run_shell_command, command)
    return job


def enqueue_python(script_path):
    q = _get_queue()
    job = q.enqueue(run_python_script, script_path)
    return job


def run_reasoning(system_data):
    """Worker-callable function to run the reasoning pipeline."""
    try:
        from core.cognitive_reasoning_engine import CognitiveReasoningEngine
        from core.llm_router import LLMRouter
        llm = LLMRouter()
        engine = CognitiveReasoningEngine(llm_router=llm)
        return engine.reason(system_data)
    except Exception as e:
        return {"success": False, "error": str(e)}


def enqueue_reasoning(system_data):
    q = _get_queue()
    job = q.enqueue(run_reasoning, system_data)
    return job
