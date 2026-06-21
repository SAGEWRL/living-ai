from core.system_engine import LivingAISystem


def main():

    ai = LivingAISystem()

    print("\n" + "=" * 60)
    print("LIVING AI COGNITIVE SYSTEM")
    print("=" * 60)

    print("\nType 'exit' to quit.\n")

    while True:

        user_input = input("YOU: ")

        # =========================
        # EXIT
        # =========================

        if user_input.lower() in [

            "exit",
            "quit"
        ]:

            print("\nShutting down LivingAI...\n")
            break

        # =========================
        # PROCESS INPUT
        # =========================

        result = ai.process(user_input)

        print("\n" + "=" * 60)
        print("LIVING AI RESPONSE")
        print("=" * 60)

        # =========================
        # SUCCESS
        # =========================

        if result["status"] == "success":

            print("\nAI:")
            print(result["response"])

            print("\n--------------------------------")

            print(
                f"Emotion: "
                f"{result['emotion']}"
            )

            print(
                f"Strategy: "
                f"{result['strategy']}"
            )

            print(
                f"Active Goal: "
                f"{result['active_goal']}"
            )

            print(
                f"Background Thought: "
                f"{result['background_thought']}"
            )

            print(
                f"Prediction: "
                f"{result['prediction']}"
            )

            print(
                f"Personality: "
                f"{result['personality']}"
            )

            print(
                f"Cognitive State: "
                f"{result['cognitive_state']}"
            )

        # =========================
        # ERROR
        # =========================

        else:

            print("\nSYSTEM ERROR:")
            print(result["error"])

        print("\n")


if __name__ == "__main__":

    main()