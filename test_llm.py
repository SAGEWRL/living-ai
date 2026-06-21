from core.llm_router import LLMRouter


def _run_demo():
    llm = LLMRouter()

    # TEST CONNECTION
    connection = llm.test_connection()
    print(connection)

    # TEST GENERATION
    response = llm.generate("Hello, who are you?")
    print(response)


if __name__ == "__main__":
    _run_demo()