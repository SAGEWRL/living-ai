import json
import os
import time

from core.system_engine import LivingAISystem


def show_whoami(system):
    data = {
        "identity": system.identity,
        "identity_traits": system.identity_traits,
        "active_goals": system.kernel.goals,
        "autonomy_history": system.autonomy_history[-5:],
        "memory_stats": system.distributed_memory.get_memory_stats(),
    }
    print(json.dumps(data, indent=2, default=str))
    return data


def synthetic_workflow(system):
    steps = [
        "Alert: production latency exceeds threshold",
        "Analyze recent deploys and service dependencies",
        "Add goal: reduce incident response time",
        "Recommend a mitigation plan",
    ]

    for step in steps:
        print(f"\n[INPUT] {step}")
        response = system.process(step)
        print("[RESPONSE]", response.get("response"))
        print("[GOALS]", [g["goal"] for g in system.kernel.goals])


def main():
    print("=== Starting validation harness ===")

    system = LivingAISystem()
    print("\n=== Initial state ===")
    show_whoami(system)

    print("\n=== Running synthetic workflow ===")
    synthetic_workflow(system)

    print("\n=== Adding persistence test goal ===")
    system.kernel.add_goal("Maintain incident orchestration continuity", priority=9)
    system.save_self_model()

    print("\n=== Final state before restart ===")
    show_whoami(system)

    print("\nSaving state files...")
    system.save_self_model()
    time.sleep(1)

    print("\n=== Restarting system ===")
    system2 = LivingAISystem()
    show_whoami(system2)

    persisted_goals = [g["goal"] for g in system2.kernel.goals]
    print("\nPersisted goal found:", "Maintain incident orchestration continuity" in persisted_goals)
    print("Persistence file status:", {
        "semantic_memory": os.path.exists("semantic_memory.json"),
        "distributed_memory": os.path.exists("distributed_memory.json"),
        "self_model": os.path.exists("self_model.json"),
    })


if __name__ == "__main__":
    main()
