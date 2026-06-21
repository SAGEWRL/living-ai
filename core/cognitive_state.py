# core/cognitive_state.py


class CognitiveState:

    def __init__(self):

        self.states = {}

    def initialize_user(
        self,
        user_id
    ):

        if user_id not in self.states:

            self.states[user_id] = {

                "energy": 100,

                "focus": 100,

                "stress": 0,

                "emotional_pressure": 0,

                "cognitive_load": 0
            }

    def update_state(
        self,
        user_id,
        emotion
    ):

        self.initialize_user(user_id)

        state = self.states[user_id]

        if emotion == "sad":

            state["stress"] += 10

            state[
                "emotional_pressure"
            ] += 15

            state["energy"] -= 5

        elif emotion == "angry":

            state["stress"] += 15

            state["focus"] -= 10

            state["energy"] -= 5

        elif emotion == "happy":

            state["energy"] += 5

            state["stress"] -= 5

        state["cognitive_load"] += 2

        for key in state:

            if state[key] < 0:

                state[key] = 0

            if state[key] > 100:

                state[key] = 100

        return state

    def get_state(
        self,
        user_id
    ):

        self.initialize_user(user_id)

        return self.states[user_id]