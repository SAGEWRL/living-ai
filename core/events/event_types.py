# core/events/event_types.py


class CognitiveEvents:

    # =========================
    # USER EVENTS
    # =========================

    USER_INPUT = (
        "user_input"
    )

    USER_RESPONSE = (
        "user_response"
    )

    # =========================
    # EMOTION EVENTS
    # =========================

    EMOTION_DETECTED = (
        "emotion_detected"
    )

    EMOTION_CHANGED = (
        "emotion_changed"
    )

    # =========================
    # MEMORY EVENTS
    # =========================

    MEMORY_STORED = (
        "memory_stored"
    )

    MEMORY_RETRIEVED = (
        "memory_retrieved"
    )

    MEMORY_PRIORITY_UPDATED = (
        "memory_priority_updated"
    )

    # =========================
    # GOAL EVENTS
    # =========================

    GOAL_CREATED = (
        "goal_created"
    )

    GOAL_UPDATED = (
        "goal_updated"
    )

    # =========================
    # COGNITIVE EVENTS
    # =========================

    COGNITIVE_STATE_UPDATED = (
        "cognitive_state_updated"
    )

    CONSCIOUSNESS_UPDATED = (
        "consciousness_updated"
    )

    # =========================
    # SYSTEM EVENTS
    # =========================

    RESPONSE_GENERATED = (
        "response_generated"
    )

    SYSTEM_ERROR = (
        "system_error"
    )