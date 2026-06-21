# core/multi_agent_runtime.py


class MultiAgentRuntime:

    def __init__(self):

        self.active_agents = {}

        self.agent_states = {}

    # =========================
    # REGISTER AGENT
    # =========================

    def register_agent(
        self,
        agent_name,
        agent_instance
    ):

        self.active_agents[
            agent_name
        ] = agent_instance

        self.agent_states[
            agent_name
        ] = {

            "status": "active",

            "executions": 0
        }

    # =========================
    # EXECUTE SINGLE AGENT
    # =========================

    def execute_agent(
        self,
        agent_name,
        input_data
    ):

        if agent_name not in self.active_agents:

            return {

                "error": (
                    "Agent not found"
                )
            }

        agent = self.active_agents[
            agent_name
        ]

        result = agent(
            input_data
        )

        self.agent_states[
            agent_name
        ][
            "executions"
        ] += 1

        return result

    # =========================
    # EXECUTE ALL AGENTS
    # =========================

    def execute_all(
        self,
        input_data
    ):

        results = {}

        for name, agent in self.active_agents.items():

            try:

                results[name] = agent(
                    input_data
                )

                self.agent_states[
                    name
                ][
                    "executions"
                ] += 1

            except Exception as error:

                results[name] = {

                    "error": str(
                        error
                    )
                }

        return results

    # =========================
    # GET STATES
    # =========================

    def get_states(self):

        return self.agent_states