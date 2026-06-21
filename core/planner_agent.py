# core/planner_agent.py


class PlannerAgent:

    def __init__(self):

        self.plans = []

    # =========================
    # CREATE PLAN
    # =========================

    def create_plan(

        self,
        goal

    ):

        if isinstance(goal, dict):
            goal = goal.get("goal", "")

        goal_lower = str(goal).lower()

        # =========================
        # ROBOTICS
        # =========================

        if "robot" in goal_lower:

            steps = [

                {
                    "type": "reasoning",

                    "action": (
                        "Learn Python"
                    )
                },

                {
                    "type": "reasoning",

                    "action": (
                        "Study electronics"
                    )
                },

                {
                    "type": "reasoning",

                    "action": (
                        "Build Arduino projects"
                    )
                }
            ]

        # =========================
        # LIST FILES
        # =========================

        elif "list files" in goal_lower:

            steps = [

                {
                    "type": "tool",

                    "tool": "list_directory",

                    "path": "."
                }
            ]

        # =========================
        # READ FILE
        # =========================

        elif "read file" in goal_lower:

            parts = goal.split()

            filepath = parts[-1]

            steps = [

                {
                    "type": "tool",

                    "tool": "read_file",

                    "filepath": filepath
                }
            ]

        # =========================
        # CREATE FILE
        # =========================

        elif "create file" in goal_lower:

            parts = goal.split()

            filename = parts[-1]

            steps = [

                {
                    "type": "tool",

                    "tool": "write_file",

                    "filepath": filename,

                    "content": (
                        "# File created "
                        "by Living AI"
                    )
                }
            ]

        # =========================
        # EXECUTE PYTHON
        # =========================

        elif "run python" in goal_lower:

            parts = goal.split()

            script = parts[-1]

            steps = [

                {
                    "type": "tool",

                    "tool": "execute_python",

                    "script_path": script
                }
            ]

        # =========================
        # DEFAULT
        # =========================

        else:

            steps = [

                {
                    "type": "reasoning",

                    "action": (
                        "Analyze goal"
                    )
                },

                {
                    "type": "reasoning",

                    "action": (
                        "Break into tasks"
                    )
                },

                {
                    "type": "reasoning",

                    "action": (
                        "Execute tasks"
                    )
                }
            ]

        # =========================
        # FINAL PLAN
        # =========================

        plan = {

            "goal": goal,

            "steps": steps,

            "completed": []
        }

        self.plans.append(plan)

        return plan