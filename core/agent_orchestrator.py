# core/agent_orchestrator.py


class AgentOrchestrator:

    def __init__(self):

        self.agents = {}

    def register_agent(
        self,
        name,
        function
    ):

        self.agents[name] = function

    def execute_agents(
        self,
        text
    ):

        results = {}

        for name, function in self.agents.items():

            try:

                results[name] = function(text)

            except Exception as e:

                results[name] = {

                    "error": str(e)
                }

        return results