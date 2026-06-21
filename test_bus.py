# test_bus.py

from core.event_bus import bus


def _run_demo():
    # Load full system (imports kept here to avoid side-effects at import-time)
    import core.emotion_engine
    import core.reasoning_engine
    import core.action_engine
    import core.memory_engine
    import core.state_engine
    import core.goal_engine
    import core.attention_engine
    import core.learning_engine
    import core.identity_engine
    import adapters.memos_adapter

    print("===== LIVING AI FULL SYSTEM =====")

    # Interaction 1
    result1 = bus.emit("text_input", "I feel very lonely today")
    print("\n===== INTERACTION 1 =====")
    for r in result1:
        print(r)

    # Interaction 2
    result2 = bus.emit("text_input", "I am angry and frustrated")
    print("\n===== INTERACTION 2 =====")
    for r in result2:
        print(r)

    # Interaction 3
    result3 = bus.emit("text_input", "I feel happy and motivated")
    print("\n===== INTERACTION 3 =====")
    for r in result3:
        print(r)


if __name__ == "__main__":
    _run_demo()