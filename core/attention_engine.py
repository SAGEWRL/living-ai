# core/attention_engine.py

from core.event_bus import bus

attention = {"focus": "normal", "priority": 1}

def attention_engine(text):
    t = text.lower()

    if "sad" in t:
        attention.update({"focus": "emotional", "priority": 5})

    elif "angry" in t:
        attention.update({"focus": "conflict", "priority": 4})

    return {"attention": attention}

bus.subscribe("input", attention_engine)