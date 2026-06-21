# core/tool_registry.py


class ToolRegistry:

    def __init__(self):

        self.registry = {}

        self.tool_metadata = {}

    # =========================
    # REGISTER TOOL
    # =========================

    def register_tool(
        self,
        tool_name,
        tool_function,
        description=None
    ):

        self.registry[
            tool_name
        ] = tool_function

        self.tool_metadata[
            tool_name
        ] = {

            "description": description,

            "status": "active"
        }

    # =========================
    # GET TOOL
    # =========================

    def get_tool(
        self,
        tool_name
    ):

        return self.registry.get(
            tool_name
        )

    # =========================
    # EXECUTE TOOL
    # =========================

    def execute_tool(
        self,
        tool_name,
        input_data=None
    ):

        tool = self.get_tool(
            tool_name
        )

        if tool is None:

            return {

                "error": (
                    "Tool not found"
                )
            }

        try:

            result = tool(
                input_data
            )

            return {

                "tool": tool_name,

                "status": (
                    "success"
                ),

                "result": result
            }

        except Exception as error:

            return {

                "tool": tool_name,

                "status": (
                    "failed"
                ),

                "error": str(
                    error
                )
            }

    # =========================
    # LIST TOOLS
    # =========================

    def list_tools(self):

        return list(
            self.registry.keys()
        )

    # =========================
    # GET METADATA
    # =========================

    def get_metadata(self):

        return self.tool_metadata