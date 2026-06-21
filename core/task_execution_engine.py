# core/task_execution_engine.py

import time


class TaskExecutionEngine:

    def __init__(self):

        self.active_tasks = []

        self.completed_tasks = []

        self.failed_tasks = []

    # =========================
    # CREATE TASK
    # =========================

    def create_task(

        self,
        name,
        action=None

    ):

        task = {

            "id": len(
                self.active_tasks
            ) + 1,

            "name": name,

            "action": action,

            "status": "pending",

            "created_at": time.time()
        }

        self.active_tasks.append(
            task
        )

        return task

    # =========================
    # EXECUTE TASK
    # =========================

    def execute_task(

        self,
        task

    ):

        try:

            task["status"] = (
                "running"
            )

            # =========================
            # SIMULATED EXECUTION
            # =========================

            result = (

                f"Executed task: "
                f"{task['name']}"
            )

            task["status"] = (
                "completed"
            )

            task["result"] = result

            self.completed_tasks.append(
                task
            )

            # REMOVE ACTIVE

            self.active_tasks.remove(
                task
            )

            return {

                "success": True,

                "result": result
            }

        except Exception as e:

            task["status"] = (
                "failed"
            )

            task["error"] = str(e)

            self.failed_tasks.append(
                task
            )

            return {

                "success": False,

                "error": str(e)
            }

    # =========================
    # EXECUTE ALL TASKS
    # =========================

    def execute_all(self):

        results = []

        for task in self.active_tasks[:]:

            result = self.execute_task(
                task
            )

            results.append(result)

        return results

    # =========================
    # STATUS
    # =========================

    def get_status(self):

        return {

            "active_tasks": len(
                self.active_tasks
            ),

            "completed_tasks": len(
                self.completed_tasks
            ),

            "failed_tasks": len(
                self.failed_tasks
            )
        }