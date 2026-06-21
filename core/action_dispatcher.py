# core/action_dispatcher.py


class ActionDispatcher:

    def __init__(
        self,
        tool_registry
    ):

        self.tool_registry = (
            tool_registry
        )

        self.action_history = []

    # =========================
    # DISPATCH ACTION
    # =========================

    def dispatch(
        self,
        action_name,
        payload=None
    ):

        result = (

            self.tool_registry.execute_tool(

                action_name,

                payload
            )
        )

        action_record = {

            "action": action_name,

            "payload": payload,

            "result": result
        }

        self.action_history.append(
            action_record
        )

        return action_record

    # =========================
    # GET HISTORY
    # =========================

    def get_history(self):

        return self.action_history