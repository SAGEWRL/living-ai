# core/reasoning_engine.py

from core.event_bus import bus


def reasoning_engine(text):

    text = text.lower()

    # Emotional reasoning
    if "sad" in text or "lonely" in text:
        return {
            "decision": "Provide emotional support",
            "priority": "high"
        }

    if "happy" in text or "excited" in text:
        return {
            "decision": "Encourage positivity",
            "priority": "medium"
        }

    if "angry" in text:
        return {
            "decision": "De-escalate conversation",
            "priority": "high"
        }

    return {
        "decision": "Observe and continue listening",
        "priority": "low"
    }


# Subscribe to event bus
bus.subscribe("text_input", reasoning_engine)