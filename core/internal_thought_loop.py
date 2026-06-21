# core/internal_thought_loop.py


class InternalThoughtLoop:

    def __init__(self):

        self.thoughts = []

    # =========================
    # THINK
    # =========================

    def think(
        self,
        input_data
    ):

        thought = {

            "reflection": (
                "Analyzing current situation"
            ),

            "input": input_data,

            "status": (
                "processed"
            )
        }

        self.thoughts.append(
            thought
        )

        return thought

    # =========================
    # GET THOUGHTS
    # =========================

    def get_thoughts(self):

        return self.thoughts