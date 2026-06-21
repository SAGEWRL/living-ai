# core/runtime_manager.py


class RuntimeManager:

    def __init__(self):

        self.running = False

        self.active_tasks = []

        self.system_state = {

            "status": "idle",

            "uptime": 0,

            "tasks_processed": 0
        }

    # =========================
    # START RUNTIME
    # =========================

    def start(self):

        self.running = True

        self.system_state["status"] = (
            "running"
        )

        return {

            "success": True,

            "message": (
                "Runtime started"
            )
        }

    # =========================
    # STOP RUNTIME
    # =========================

    def stop(self):

        self.running = False

        self.system_state["status"] = (
            "stopped"
        )

        return {

            "success": True,

            "message": (
                "Runtime stopped"
            )
        }

    # =========================
    # REGISTER TASK
    # =========================

    def register_task(

        self,
        task

    ):

        self.active_tasks.append(task)

        self.system_state[
            "tasks_processed"
        ] += 1

    # =========================
    # GET STATE
    # =========================

    def get_state(self):

        return {

            "running": self.running,

            "active_tasks": len(
                self.active_tasks
            ),

            "system_state": (
                self.system_state
            )
        }