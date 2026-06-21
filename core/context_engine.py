# core/context_engine.py

import core.memory_db as memory_db


def context_engine(user_id):

    recent = memory_db.get_recent(
        user_id,
        5
    )

    sadness = 0
    happiness = 0
    anger = 0

    for item in recent:

        text, emotion = item

        if emotion == "sad":
            sadness += 1

        elif emotion == "happy":
            happiness += 1

        elif emotion == "angry":
            anger += 1

    context = {

        "dominant_emotion": "neutral",

        "emotional_trend": "stable",

        "memory_depth": len(recent)
    }

    if sadness > happiness and sadness > anger:

        context["dominant_emotion"] = "sad"

        context["emotional_trend"] = "declining"

    elif happiness > sadness:

        context["dominant_emotion"] = "happy"

        context["emotional_trend"] = "improving"

    elif anger > 0:

        context["dominant_emotion"] = "angry"

        context["emotional_trend"] = "unstable"

    return context