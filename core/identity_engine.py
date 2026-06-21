# core/identity_engine.py

from core.event_bus import bus

identity = {"tone": "calm", "empathy": 0.7}

def identity_engine(text):
    t = text.lower()

    if "sad" in t:
        identity["tone"] = "supportive"

    if "happy" in t:
        identity["tone"] = "positive"

    return {"identity": identity}

bus.subscribe("input", identity_engine)