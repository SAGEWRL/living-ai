# core/planning_engine.py


class PlanningEngine:

    def __init__(self):

        self.active_plans = []

    # =========================
    # CREATE PLAN
    # =========================

    def create_plan(
        self,
        goal
    ):

        plan = {

            "goal": goal,

            "steps": [

                "analyze_goal",

                "build_strategy",

                "execute_actions",

                "evaluate_results"
            ]
        }

        self.active_plans.append(
            plan
        )

        return plan

    # =========================
    # GET ACTIVE PLANS
    # =========================

    def get_active_plans(self):

        return self.active_plans