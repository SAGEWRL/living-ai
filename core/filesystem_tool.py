# core/filesystem_tool.py

import os


def filesystem_tool(
    input_data=None
):

    if input_data is None:

        return {

            "error": (
                "No input provided"
            )
        }

    action = input_data.get(
        "action"
    )

    path = input_data.get(
        "path"
    )

    # =========================
    # READ FILE
    # =========================

    if action == "read":

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            return {

                "status": "success",

                "content": content
            }

        except Exception as error:

            return {

                "status": "failed",

                "error": str(
                    error
                )
            }

    # =========================
    # WRITE FILE
    # =========================

    if action == "write":

        content = input_data.get(
            "content",
            ""
        )

        try:

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    content
                )

            return {

                "status": "success",

                "message": (
                    "File written"
                )
            }

        except Exception as error:

            return {

                "status": "failed",

                "error": str(
                    error
                )
            }

    return {

        "error": (
            "Unknown filesystem action"
        )
    }