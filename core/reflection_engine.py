# core/reflection_engine.py


class ReflectionEngine:

    def __init__(self):

        self.reflections = []

    # =========================
    # REFLECT
    # =========================

    def reflect(

        self,
        goal,
        execution_results=None

    ):

        if execution_results is None and isinstance(goal, dict):
            data = goal
            goal = data.get("goal", str(data))
            execution_results = data.get("execution_results", [])

        execution_results = execution_results or []

        successful = 0

        failed = 0

        observations = []

        for result in execution_results:

            if result.get(

                "success",
                False

            ):

                successful += 1

            else:

                failed += 1

                observations.append(

                    result.get(
                        "error",
                        "Unknown failure"
                    )
                )

        # =========================
        # PERFORMANCE SCORE
        # =========================

        total = successful + failed

        if total == 0:

            score = 0

        else:

            score = round(
                successful / total,
                2
            )

        # =========================
        # REFLECTION DATA
        # =========================

        reflection = {

            "goal": goal,

            "successful_steps": successful,

            "failed_steps": failed,

            "performance_score": score,

            "observations": observations
        }

        self.reflections.append(
            reflection
        )

        return reflection

    # =========================
    # STATUS
    # =========================

    def get_status(self):

        return {

            "reflections": len(
                self.reflections
            )
        }