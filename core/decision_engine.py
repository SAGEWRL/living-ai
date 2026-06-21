# core/decision_engine.py


class DecisionEngine:

    def __init__(self):

        self.decision_history = []

    # =========================
    # DECIDE
    # =========================

    def decide(

        self,
        goal,
        reasoning_analysis=None,
        execution_results=None,
        cognitive_state=None

    ):

        decision = {

            "action": "normal_execution",

            "reason": "Default execution",

            "priority": 1,

            "risk_score": 0
        }

        # =========================
        # REASONING ANALYSIS
        # =========================

        if reasoning_analysis:

            complexity = reasoning_analysis.get(
                "complexity",
                1
            )

            risks = reasoning_analysis.get(
                "risks",
                []
            )

            if len(risks) > 0:

                decision["action"] = (
                    "careful_execution"
                )

                decision["reason"] = (
                    "Risk-aware execution"
                )

                decision["priority"] = (
                    complexity + 3
                )

                decision["risk_score"] = (
                    len(risks) * 2
                )

            elif complexity >= 3:

                decision["action"] = (
                    "strategic_execution"
                )

                decision["reason"] = (
                    "Complex task detected"
                )

                decision["priority"] = (
                    complexity
                )

            else:

                decision["action"] = (
                    "normal_execution"
                )

                decision["reason"] = (
                    "Low complexity task"
                )

                decision["priority"] = 2

        # =========================
        # FAILURE CHECK
        # =========================

        if execution_results:

            failures = [

                result

                for result in execution_results

                if not result.get(
                    "success",
                    False
                )
            ]

            if failures:

                decision["action"] = (
                    "recovery"
                )

                decision["reason"] = (
                    "Failures detected"
                )

                decision["priority"] = 10

        # =========================
        # LOW ENERGY
        # =========================

        if cognitive_state:

            energy = cognitive_state.get(
                "energy",
                100
            )

            if energy < 20:

                decision["action"] = (
                    "recovery"
                )

                decision["reason"] = (
                    "Low energy"
                )

                decision["priority"] = 9

        self.decision_history.append(
            decision
        )

        return decision

    # Backwards-compatible alias expected by tests
    def make_decision(self, goal, cognitive_state=None, sim_result=None, reasoning_analysis=None, execution_results=None):
        return self.decide(
            goal,
            reasoning_analysis=reasoning_analysis,
            execution_results=execution_results,
            cognitive_state=cognitive_state
        )

    # =========================
    # LEARNING ADAPTATION
    # =========================

    def adapt_from_learning(

        self,
        adaptation

    ):

        adjustments = adaptation.get(
            "adjustments",
            []
        )

        risk_awareness = adaptation.get(
            "risk_awareness",
            0
        )

        strategy_update = {

            "decision_style": "normal",

            "validation_level": 1,

            "risk_modifier": 0
        }

        if risk_awareness >= 5:

            strategy_update[
                "decision_style"
            ] = "cautious"

            strategy_update[
                "validation_level"
            ] = 3

            strategy_update[
                "risk_modifier"
            ] = risk_awareness

        elif risk_awareness >= 2:

            strategy_update[
                "decision_style"
            ] = "balanced"

            strategy_update[
                "validation_level"
            ] = 2

        else:

            strategy_update[
                "decision_style"
            ] = "efficient"

        if (
            "Increase validation checks"
            in adjustments
        ):

            strategy_update[
                "validation_level"
            ] += 1

        return strategy_update