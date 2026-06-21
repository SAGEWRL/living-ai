# core/learning_feedback_loop.py


class LearningFeedbackLoop:

    def __init__(self):

        self.feedback_history = []

        self.learning_score = 0

    # =========================
    # PROCESS FEEDBACK
    # =========================

    def process_feedback(
        self,
        interaction_result
    ):

        self.learning_score += 1

        feedback = {

            "interaction": (
                interaction_result
            ),

            "learning_score": (
                self.learning_score
            ),

            "status": (
                "improved"
            )
        }

        self.feedback_history.append(
            feedback
        )

        return feedback

    # =========================
    # GET LEARNING STATE
    # =========================

    def get_learning_state(self):

        return {

            "score": (
                self.learning_score
            ),

            "history_size": len(
                self.feedback_history
            )
        }