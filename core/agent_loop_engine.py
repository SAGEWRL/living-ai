# core/agent_loop_engine.py

import time


class AgentLoopEngine:

    def __init__(self):

        self.active = False

        self.loop_history = []

    # =========================
    # START LOOP
    # =========================

    def start_loop(
        self,
        task,
        cycles=3
    ):

        self.active = True

        results = []

        for cycle in range(
            cycles
        ):

            result = {

                "cycle": cycle + 1,

                "task": task,

                "status": (
                    "executed"
                )
            }

            results.append(
                result
            )

            self.loop_history.append(
                result
            )

            time.sleep(1)

        self.active = False

        return results

    # =========================
    # GET HISTORY
    # =========================

    def get_history(self):

        return self.loop_history