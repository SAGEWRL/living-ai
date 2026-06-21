# core/meta_cognition.py


class MetaCognition:

    def __init__(self):

        self.self_evaluation_history = []

        self.cognitive_tension = 0

        self.emotional_pressure = 0

    # =========================
    # SELF REFLECTION
    # =========================

    def reflect_on_response(

        self,
        response,
        prediction

    ):

        reflection = {

            "confidence": 0.5,

            "uncertainty": 0.5,

            "self_commentary": ""
        }

        # =========================
        # CONFIDENCE
        # =========================

        probability = prediction.get(

            "success_probability",

            0.5
        )

        reflection[
            "confidence"
        ] = probability

        reflection[
            "uncertainty"
        ] = 1 - probability

        # =========================
        # COMMENTARY
        # =========================

        if probability >= 0.8:

            reflection[
                "self_commentary"
            ] = (

                "Reasoning appears stable "
                "and strategically sound."
            )

        elif probability >= 0.6:

            reflection[
                "self_commentary"
            ] = (

                "Strategy seems viable "
                "but contains uncertainty."
            )

        else:

            reflection[
                "self_commentary"
            ] = (

                "High uncertainty detected "
                "in current reasoning."
            )

        self.self_evaluation_history.append(
            reflection
        )

        return reflection

    # =========================
    # EMOTIONAL PRESSURE
    # =========================

    def update_emotional_pressure(

        self,
        emotion

    ):

        if emotion == "frustrated":

            self.emotional_pressure += 2

        elif emotion == "sad":

            self.emotional_pressure += 1

        elif emotion == "excited":

            self.emotional_pressure -= 1

        # =========================
        # LIMITS
        # =========================

        if self.emotional_pressure < 0:

            self.emotional_pressure = 0

        if self.emotional_pressure > 10:

            self.emotional_pressure = 10

        return self.emotional_pressure

    # =========================
    # COGNITIVE TENSION
    # =========================

    def evaluate_tension(

        self,
        goals

    ):

        if len(goals) <= 1:

            self.cognitive_tension = 0

        else:

            priorities = [

                g["priority"]

                for g in goals
            ]

            spread = max(priorities) - min(priorities)

            self.cognitive_tension = spread

        return self.cognitive_tension

    # =========================
    # META STATE
    # =========================

    def get_meta_state(self):

        return {

            "emotional_pressure": (
                self.emotional_pressure
            ),

            "cognitive_tension": (
                self.cognitive_tension
            ),

            "reflection_cycles": len(
                self.self_evaluation_history
            )
        }