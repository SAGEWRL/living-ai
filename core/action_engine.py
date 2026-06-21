# core/action_engine.py

from core.event_bus import bus

def action_engine(text):
    t = text.lower()

    if "sad" in t or "lonely" in t:
        return {"response": "I'm here with you."}

    if "happy" in t:
        return {"response": "That’s great to hear."}

    if "angry" in t:
        return {"response": "Take a breath. I'm listening."}

    return {"response": "Noted."}


bus.subscribe("input", action_engine)