# core/cognitive_reasoning_engine.py

import os


class CognitiveReasoningEngine:

    def __init__(self, llm_router=None):
        self.llm_router = llm_router

    # =========================
    # DETECT GOAL TYPE
    # =========================
    # =========================
    # DETECT GOAL TYPE
    # =========================

    def detect_goal_type(

        self,
        text

    ):

        text = text.lower()

        if "robot" in text:

            return "robotics"

        elif "ai" in text:

            return "artificial_intelligence"

        elif "app" in text:

            return "application_development"

        elif "money" in text:

            return "business"

        return "general"

    # =========================
    # REASON
    # =========================

    def reason(

        self,
        system_data

    ):

        user_input = system_data.get(
            "input",
            ""
        )

        thought = system_data.get(
            "thought",
            ""
        )

        plan = system_data.get(
            "plan",
            {}
        )

        task_results = system_data.get(
            "task_results",
            []
        )

        memories = system_data.get(
            "memories",
            []
        )

        cognitive_state = system_data.get(
            "cognitive_state",
            {}
        )

        behavior = system_data.get(
            "behavior",
            {}
        )

        # =========================
        # GOAL ANALYSIS
        # =========================

        goal_type = (
            self.detect_goal_type(
                user_input
            )
        )

        # =========================
        # MODEL-BASED REASONING
        # =========================

        if self.llm_router is not None:

            prompt_parts = [
                "You are an autonomous cognitive agent. Analyze the following system state and provide a concise reasoning response.",
                f"User Input: {user_input}",
                f"Internal Thought: {thought}",
                f"Goal Type: {goal_type}",
                f"Plan: {plan}",
                f"Task Results: {task_results}",
                f"Memories: {memories}",
                f"Cognitive State: {cognitive_state}",
                f"Behavior: {behavior}"
            ]

            prompt = "\n".join(prompt_parts)

            llm_result = self.llm_router.generate(
                prompt
            )

            if llm_result.get("success"):

                return {
                    "response": llm_result["response"],
                    "goal_type": goal_type,
                    "llm": True,
                    "plan": plan
                }

        # =========================
        # FALLBACK RULE-BASED REASONING
        # =========================

        response = []

        response.append(
            "LIVING AI COGNITIVE REPORT"
        )

        response.append("")

        response.append(
            f"Goal Type: {goal_type}"
        )

        response.append("")

        response.append(
            f"Internal Thought: {thought}"
        )

        response.append("")

        response.append(
            "EXECUTION PLAN:"
        )

        response.append("")

        for i, step in enumerate(

            plan.get("steps", []),

            start=1

        ):

            response.append(
                f"[STEP {i}] {step}"
            )

        response.append("")

        response.append(
            "TASK EXECUTION RESULTS:"
        )

        response.append("")

        for result in task_results:

            if result.get("success"):

                response.append(

                    f"[SUCCESS] "

                    f"{result.get('result')}"
                )

            else:

                response.append(

                    f"[FAILED] "

                    f"{result.get('error')}"
                )

        response.append("")

        response.append(
            "MEMORY ANALYSIS:"
        )

        response.append("")

        response.append(
            f"Relevant Memories: {len(memories)}"
        )

        return {
            "response": "\n".join(response),
            "goal_type": goal_type,
            "llm": False,
            "plan": plan
        }
        # =========================

        response.append("")

        response.append(
            "COGNITIVE STATE:"
        )

        response.append("")

        response.append(

            f"Energy: "
            f"{cognitive_state.get('energy')}"
        )

        response.append(

            f"Focus: "
            f"{cognitive_state.get('focus')}"
        )

        response.append(

            f"Cognitive Load: "
            f"{cognitive_state.get('cognitive_load')}"
        )

        # =========================
        # BEHAVIOR
        # =========================

        response.append("")

        response.append(
            "BEHAVIORAL MODE:"
        )

        response.append("")

        response.append(

            f"Mode: "
            f"{behavior.get('mode', 'balanced')}"
        )

        # =========================
        # RUNTIME
        # =========================

        response.append("")

        response.append(
            "RUNTIME STATUS:"
        )

        response.append("")

        response.append(

            f"Running: "
            f"{runtime_state.get('running')}"
        )

        response.append(

            f"Active Tasks: "
            f"{runtime_state.get('active_tasks')}"
        )

        # =========================
        # FINAL
        # =========================

        final_response = "\n".join(
            response
        )

        return {

            "success": True,

            "response": final_response
        }

    async def reason_async(self, system_data):
        """Async wrapper for reasoning to avoid blocking the main thread.

        This runs the blocking `reason` method in a thread pool.
        """
        import asyncio
        return await asyncio.to_thread(self.reason, system_data)