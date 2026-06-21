# core/cognitive_kernel.py


import time
import uuid


class CognitiveKernel:

    def __init__(self, storage_backend=None):

        # =========================
        # LONG TERM IDENTITY
        # =========================

        self.identity = {

            "name": "LivingAI",

            "self_model": "emerging",

            "beliefs": [],

            "values": ["learn", "adapt", "stabilize"],

            "history_summary": []
        }

        # =========================
        # WORLD MODEL
        # =========================

        self.world_model = {

            "known_entities": {},

            "state_estimates": {},

            "cause_effect_links": []
        }

        # =========================
        # AUTONOMOUS GOALS
        # =========================

        self.goals = [

            {
                "goal": "maintain stability",

                "priority": 10
            }
        ]

        # =========================
        # CONTINUOUS THOUGHT BUFFER
        # =========================

        self.thought_buffer = []

        # optional shared storage backend for persisting kernel state
        self.storage_backend = storage_backend
        self.storage_key = "kernel_goals"

    # =========================
    # UPDATE IDENTITY
    # =========================

    def update_identity(

        self,
        experience

    ):

        self.identity["history_summary"].append(
            experience
        )

        if len(self.identity["history_summary"]) > 50:

            self.identity["history_summary"].pop(0)

    # =========================
    # UPDATE WORLD MODEL
    # =========================

    def update_world_model(

        self,
        input_data

    ):

        self.world_model["state_estimates"][
            str(time.time())
        ] = input_data

    # =========================
    # ADD GOAL
    # =========================

    def contains_goal(

        self,
        goal

    ):

        return any(
            existing.get("goal") == goal
            for existing in self.goals
        )

    def add_goal(

        self,
        goal,
        priority=5

    ):

        if self.contains_goal(goal):
            for existing in self.goals:
                if existing.get("goal") == goal:
                    existing["priority"] = max(
                        existing.get("priority", 5),
                        priority
                    )
                    return existing
        new_goal = {
            "id": uuid.uuid4().hex,
            "goal": goal,
            "priority": priority,
            "status": "active"
        }
        self.goals.append(new_goal)
        # persist updated goals if backend available
        try:
            if self.storage_backend:
                self.storage_backend.set(self.storage_key, self.goals)
        except Exception:
            pass
        return new_goal

    # =========================
    # SELECT TOP GOAL
    # =========================

    def select_goal(self):

        if not self.goals:

            return None

        return sorted(

            self.goals,

            key=lambda x: x["priority"],

            reverse=True

        )[0]

    # =========================
    # COMPLETE GOAL
    # =========================

    def complete_goal(

        self,
        goal

    ):

        if isinstance(goal, dict):
            target = goal.get("goal")
        else:
            target = goal

        self.goals = [
            existing
            for existing in self.goals
            if existing.get("goal") != target
        ]

        try:
            if self.storage_backend:
                self.storage_backend.set(self.storage_key, self.goals)
        except Exception:
            pass

        return target

    def save_goals(self, storage_key=None):
        key = storage_key or self.storage_key
        if self.storage_backend:
            try:
                return self.storage_backend.set(key, self.goals)
            except Exception:
                return False
        return False

    # =========================
    # LOAD GOALS
    # =========================

    def load_goals(

        self,
        goals

    ):

        if isinstance(goals, list):
            unique = []
            seen = set()
            for goal in goals:
                if isinstance(goal, dict):
                    goal_text = goal.get("goal")
                    if goal_text and goal_text not in seen:
                        seen.add(goal_text)
                        normalized_goal = {
                            "id": goal.get("id") or uuid.uuid4().hex,
                            "goal": goal_text,
                            "priority": goal.get("priority", 5),
                            "status": goal.get("status", "active")
                        }
                        unique.append(normalized_goal)
                else:
                    if goal not in seen:
                        seen.add(goal)
                        unique.append({
                            "id": uuid.uuid4().hex,
                            "goal": goal,
                            "priority": 5,
                            "status": "active"
                        })
            self.goals = unique

        return self.goals

    # =========================
    # CONTINUOUS THINK STEP
    # =========================

    def think(self):

        goal = self.select_goal()

        thought = {

            "goal": goal,

            "timestamp": time.time(),

            "reflection": "system is maintaining internal coherence"
        }

        self.thought_buffer.append(thought)

        if len(self.thought_buffer) > 100:

            self.thought_buffer.pop(0)

        return thought