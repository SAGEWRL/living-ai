# core/response_engine.py


def response_engine(system_data):

    # =========================
    # GET REASONING
    # =========================

    reasoning = system_data.get(
        "llm_reasoning",
        {}
    )

    # =========================
    # EXTRACT RESPONSE
    # =========================

    response_text = reasoning.get(
        "response",
        "No response generated."
    )

    # =========================
    # EMOTION
    # =========================

    emotion_data = system_data.get(
        "emotion",
        {}
    )

    emotion = emotion_data.get(
        "emotion",
        "neutral"
    )

    # =========================
    # COGNITIVE STATE
    # =========================

    cognitive_state = system_data.get(
        "cognitive_state",
        {}
    )

    # =========================
    # FINAL RESPONSE OBJECT
    # =========================

    final_response = {

        "response": response_text,

        "emotion": emotion,

        "cognitive_state": (
            cognitive_state
        ),

        "status": "success"
    }

    return final_response