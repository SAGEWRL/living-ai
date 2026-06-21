# core/command_executor.py

import subprocess


def command_executor(
    input_data=None
):

    if input_data is None:

        return {

            "error": (
                "No command provided"
            )
        }

    command = input_data.get(
        "command"
    )

    try:

        result = subprocess.run(

            command,

            shell=True,

            capture_output=True,

            text=True
        )

        return {

            "status": "success",

            "stdout": result.stdout,

            "stderr": result.stderr,

            "returncode": (
                result.returncode
            )
        }

    except Exception as error:

        return {

            "status": "failed",

            "error": str(
                error
            )
        }