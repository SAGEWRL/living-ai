# core/adaptive_behavior_engine.py


class AdaptiveBehaviorEngine:

    def __init__(self):

        self.behavior_mode = "balanced"

    # =========================
    # ADAPT BEHAVIOR
    # =========================

    def adapt_behavior(

        self,
        emotion="neutral",
        priority=1

    ):

        behavior = {

            "mode": "balanced",

            "response_speed": "normal"
        }

        if priority >= 8:

            behavior["mode"] = "focused"

            behavior["response_speed"] = "fast"

        elif priority <= 2:

            behavior["mode"] = "relaxed"

            behavior["response_speed"] = "slow"

        self.behavior_mode = behavior[
            "mode"
        ]

        return behavior

    # =========================
    # LEARNING ADAPTATION
    # =========================

    def adapt_from_learning(

        self,
        reflection

    ):

        failed_steps = reflection.get(
            "failed_steps",
            0
        )

        score = reflection.get(
            "performance_score",
            1
        )

        adaptation = {

            "behavior_mode": "balanced",

            "risk_level": 0
        }

        if failed_steps >= 3:

            adaptation[
                "behavior_mode"
            ] = "cautious"

            adaptation[
                "risk_level"
            ] = 8

        elif score < 0.5:

            adaptation[
                "behavior_mode"
            ] = "careful"

            adaptation[
                "risk_level"
            ] = 5

        else:

            adaptation[
                "behavior_mode"
            ] = "efficient"

            adaptation[
                "risk_level"
            ] = 2

        self.behavior_mode = adaptation[
            "behavior_mode"
        ]

        return adaptation