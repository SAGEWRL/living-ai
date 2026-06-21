# core/natural_response_engine.py


class NaturalResponseEngine:

    def __init__(self):

        self.response_history = []

    # =========================
    # GENERATE RESPONSE
    # =========================

    def generate(

        self,
        system_data

    ):

        user_input = system_data.get(
            "input",
            ""
        )

        reasoning = system_data.get(
            "reasoning_analysis",
            {}
        )

        llm_reasoning = system_data.get(
            "llm_reasoning",
            {}
        )

        emotion_data = system_data.get(
            "emotion_data",
            {}
        )

        decision = system_data.get(
            "decision",
            {}
        )

        reflection = system_data.get(
            "reflection",
            {}
        )

        behavior = system_data.get(
            "behavior",
            {}
        )

        # =========================
        # EXTRACT
        # =========================

        emotion = emotion_data.get(
            "emotion",
            "neutral"
        )

        goal_type = reasoning.get(
            "goal_type",
            "general"
        )

        strategy = reasoning.get(
            "strategy",
            []
        )

        tone = behavior.get(
            "mode",
            "balanced"
        )

        performance = reflection.get(
            "performance_score",
            1
        )

        llm_text = llm_reasoning.get(
            "response"
        ) if isinstance(
            llm_reasoning,
            dict
        ) else None

        # =========================
        # RESPONSE START
        # =========================

        response = ""

        # =========================
        # EMOTIONAL ADAPTATION
        # =========================

        if emotion == "frustrated":

            response += (

                "I can detect some "
                "frustration in your "
                "request. "

                "I'll try to keep this "
                "focused and efficient.\n\n"
            )

        elif emotion == "sad":

            response += (

                "I understand this may "
                "feel emotionally heavy. "

                "I'll approach it carefully.\n\n"
            )

        elif emotion == "excited":

            response += (

                "This looks exciting. "

                "Let's build it properly.\n\n"
            )

        # =========================
        # GOAL REASONING
        # =========================

        response += (

            f"I analyzed your goal "
            f"as a {goal_type} task.\n\n"
        )

        # =========================
        # STRATEGY
        # =========================

        if strategy:

            response += (
                "Best strategy:\n"
            )

            for i, step in enumerate(
                strategy,
                start=1
            ):

                response += (

                    f"{i}. {step}\n"
                )

            response += "\n"

        # =========================
        # DECISION ANALYSIS
        # =========================

        response += (

            f"Decision mode: "
            f"{decision.get('action')}\n"
        )

        # =========================
        # PERFORMANCE
        # =========================

        if performance < 0.5:

            response += (

                "\nPerformance was low, "
                "so future execution "
                "will become more cautious."
            )

        elif performance >= 0.8:

            response += (

                "\nExecution quality was "
                "high. Current strategy "
                "appears effective."
            )

        # =========================
        # TONE ADAPTATION
        # =========================

        if tone == "focused":

            response += (

                "\n\nMaintaining focused "
                "execution mode."
            )

        elif tone == "relaxed":

            response += (

                "\n\nSystem state is stable."
            )

        # =========================
        # LLM REASONING
        # =========================

        if llm_text:

            response += (

                "\n\nAdditional reasoning:\n"
                f"{llm_text}\n"
            )

        # =========================
        # STORE
        # =========================

        self.response_history.append(
            response
        )

        return response

    # =========================
    # STATUS
    # =========================

    def get_status(self):

        return {

            "responses_generated": len(
                self.response_history
            )
        }