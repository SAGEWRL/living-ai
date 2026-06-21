# core/consciousness_engine.py


class ConsciousnessEngine:

    def __init__(self):

        self.states = {}

    def initialize_user(
        self,
        user_id
    ):

        if user_id not in self.states:

            self.states[user_id] = {

                "awareness_level": 0,

                "focus_state": "neutral",

                "self_model_strength": 0
            }

    def update_consciousness(
        self,
        user_id,
        emotion,
        memory_priority
    ):

        self.initialize_user(user_id)

        profile = self.states[user_id]

        # =========================
        # AWARENESS EVOLUTION
        # =========================

        profile[
            "awareness_level"
        ] += 1

        if (
            profile[
                "awareness_level"
            ] > 100
        ):

            profile[
                "awareness_level"
            ] = 100

        # =========================
        # FOCUS STATE
        # =========================

        if emotion == "sad":

            profile[
                "focus_state"
            ] = "emotional_support"

        elif emotion == "happy":

            profile[
                "focus_state"
            ] = "motivation"

        elif emotion == "angry":

            profile[
                "focus_state"
            ] = "stabilization"

        else:

            profile[
                "focus_state"
            ] = "observation"

        # =========================
        # SELF MODEL
        # =========================

        if memory_priority == "critical":

            profile[
                "self_model_strength"
            ] += 10

        elif memory_priority == "high":

            profile[
                "self_model_strength"
            ] += 5

        else:

            profile[
                "self_model_strength"
            ] += 1

        if (
            profile[
                "self_model_strength"
            ] > 100
        ):

            profile[
                "self_model_strength"
            ] = 100

        return profile