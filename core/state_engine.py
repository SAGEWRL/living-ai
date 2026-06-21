# core/state_engine.py

from core.event_bus import bus

state = {"mood": "neutral", "energy": 100}

def state_engine(text):
    t = text.lower()

    if "sad" in t:
        state["mood"] = "low"
        state["energy"] -= 5

    if "happy" in t:
        state["mood"] = "high"
        state["energy"] += 5

    state["energy"] = max(0, min(100, state["energy"]))

    return {"state": state}

bus.subscribe("input", state_engine)