# core/tool_manager.py


class ToolManager:

    def __init__(self):

        self.tools = {}

        self.execution_history = []

    # =========================
    # REGISTER TOOL
    # =========================

    def register_tool(
        self,
        tool_name,
        tool_function
    ):

        self.tools[
            tool_name
        ] = tool_function

    # =========================
    # EXECUTE TOOL
    # =========================

    def execute_tool(
        self,
        tool_name,
        input_data=None
    ):

        if tool_name not in self.tools:

            return {

                "error": (
                    "Tool not found"
                )
            }

        try:

            tool = self.tools[
                tool_name
            ]

            result = tool(
                input_data
            )

            execution = {

                "tool": tool_name,

                "input": input_data,

                "result": result,

                "status": "success"
            }

            self.execution_history.append(
                execution
            )

            return execution

        except Exception as error:

            failed_execution = {

                "tool": tool_name,

                "error": str(
                    error
                ),

                "status": "failed"
            }

            self.execution_history.append(
                failed_execution
            )

            return failed_execution

    # =========================
    # GET TOOLS
    # =========================

    def get_tools(self):

        return list(
            self.tools.keys()
        )

    # =========================
    # GET HISTORY
    # =========================

    def get_history(self):

        return self.execution_history