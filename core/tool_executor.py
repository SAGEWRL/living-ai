# core/tool_executor.py

import os
import subprocess


class ToolExecutor:

    def __init__(self):

        self.execution_history = []

    # =========================
    # LIST DIRECTORY
    # =========================

    def list_directory(

        self,
        path="."

    ):

        try:

            files = os.listdir(path)

            result = {

                "success": True,

                "files": files
            }

            self.execution_history.append(
                result
            )

            return result

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =========================
    # READ FILE
    # =========================

    def read_file(

        self,
        filepath

    ):

        try:

            with open(

                filepath,
                "r",
                encoding="utf-8"

            ) as file:

                content = file.read()

            result = {

                "success": True,

                "content": content
            }

            self.execution_history.append(
                result
            )

            return result

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =========================
    # WRITE FILE
    # =========================

    def write_file(

        self,
        filepath,
        content

    ):

        try:

            with open(

                filepath,
                "w",
                encoding="utf-8"

            ) as file:

                file.write(content)

            result = {

                "success": True,

                "filepath": filepath
            }

            self.execution_history.append(
                result
            )

            return result

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =========================
    # EXECUTE PYTHON
    # =========================

    def execute_python(

        self,
        script_path

    ):

        # Optionally enqueue heavy script executions to a worker queue
        if os.environ.get("LIVING_AI_USE_QUEUE", "0") == "1":
            try:
                from core.task_queue import enqueue_python
                job = enqueue_python(script_path)
                return {"success": True, "queued": True, "job_id": job.id}
            except Exception:
                # fall back to local execution on failure
                pass

        try:

            result = subprocess.run(

                ["python", script_path],

                capture_output=True,

                text=True
            )

            output = {

                "success": True,

                "stdout": result.stdout,

                "stderr": result.stderr
            }

            self.execution_history.append(
                output
            )

            return output

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =========================
    # EXECUTE TERMINAL COMMAND
    # =========================

    def execute_command(

        self,
        command

    ):

        # Optionally enqueue shell command executions to a worker queue
        if os.environ.get("LIVING_AI_USE_QUEUE", "0") == "1":
            try:
                from core.task_queue import enqueue_command
                job = enqueue_command(command)
                return {"success": True, "queued": True, "job_id": job.id}
            except Exception:
                # fall back to local execution on failure
                pass

        try:

            result = subprocess.run(

                command,

                shell=True,

                capture_output=True,

                text=True
            )

            output = {

                "success": True,

                "stdout": result.stdout,

                "stderr": result.stderr
            }

            self.execution_history.append(
                output
            )

            return output

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =========================
    # TOOL STATUS
    # =========================

    def get_status(self):

        return {

            "executions": len(
                self.execution_history
            )
        }