# core/memory_engine.py

from core.event_bus import bus

memory = []

def memory_engine(text):
    memory.append(text)

    return {
        "memory_size": len(memory),
        "last_input": memory[-1]
    }

bus.subscribe("input", memory_engine)