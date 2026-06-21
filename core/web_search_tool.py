# core/web_search_tool.py


def web_search_tool(
    input_data=None
):

    query = "unknown"

    if input_data:

        query = input_data.get(
            "query",
            "unknown"
        )

    return {

        "query": query,

        "results": [

            "web_result_1",

            "web_result_2",

            "web_result_3"
        ],

        "status": (
            "simulated"
        )
    }