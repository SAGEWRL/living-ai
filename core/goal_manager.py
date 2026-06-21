# core/goal_manager.py


class GoalManager:

    def __init__(self):

        self.active_goals = {}

    def detect_goal(
        self,
        text
    ):

        text = text.lower()

        if (
            "success" in text
            or "money" in text
            or "rich" in text
        ):

            return (
                "Support ambition and growth"
            )

        elif (
            "sad" in text
            or "lonely" in text
            or "depressed" in text
        ):

            return (
                "Provide emotional support"
            )

        elif (
            "learn" in text
            or "study" in text
            or "build" in text
        ):

            return (
                "Encourage learning and creation"
            )

        return (
            "Maintain healthy interaction"
        )

    def update_goal(
        self,
        user_id,
        text
    ):

        detected_goal = (
            self.detect_goal(text)
        )

        self.active_goals[
            user_id
        ] = detected_goal

        return detected_goal

    def get_goal(
        self,
        user_id
    ):

        return self.active_goals.get(

            user_id,

            "Maintain healthy interaction"
        )