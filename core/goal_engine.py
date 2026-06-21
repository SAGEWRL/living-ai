# core/goal_engine.py

from core.event_bus import bus

goal = {"current": "observe"}

def goal_engine(text):
    t = text.lower()

    if "sad" in t:
        goal["current"] = "support_user"

    elif "happy" in t:
        goal["current"] = "reinforce_positive"

    return {"goal": goal}

bus.subscribe("input", goal_engine)