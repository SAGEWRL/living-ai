# core/system_engine.py

import time
import random
import json
import os
import threading
import asyncio

from core.storage_config import create_storage_backend

from core.event_emitter import (
    EventEmitter
)

from core.runtime_manager import RuntimeManager
# NOTE: Many core submodules (LLM, vector models, transformers, etc.) are
# expensive to import. To avoid heavy startup costs during testing or when
# only importing type definitions, these submodules are imported lazily
# inside the LivingAISystem constructor.


class LivingAISystem:

    def __init__(self, storage_backend=None):

        # =====================================
        # IDENTITY
        # =====================================

        self.identity = {

            "name": "LivingAI",

            "version": (
                "8.0 Predictive Autonomous Runtime"
            ),

            "status": "active"
        }

        # =====================================
        # EVENT EMITTER
        # =====================================

        self.event_emitter = EventEmitter()

        # =====================================
        # RUNTIME
        # =====================================

        self.runtime_manager = (
            RuntimeManager()
        )

        self.runtime_manager.start()

        # =====================================
        # STORAGE
        # =====================================

        # allow injection of a storage backend (tests or orchestrator can pass one)
        self.storage_backend = storage_backend or create_storage_backend()

        # =====================================
        # MEMORY
        # =====================================

        # lazy import memory-related modules
        from core.semantic_memory import SemanticMemory
        from core.vector_memory_engine import VectorMemoryEngine

        self.semantic_memory = SemanticMemory(storage_backend=self.storage_backend)
        self.vector_memory = VectorMemoryEngine()

        # =====================================
        # MODEL ROUTER
        # =====================================

        from core.llm_router import LLMRouter

        self.llm_router = LLMRouter()

        # =====================================
        # REASONING
        # =====================================

        from core.cognitive_reasoning_engine import CognitiveReasoningEngine
        from core.advanced_reasoning_engine import AdvancedReasoningEngine
        from core.multi_path_reasoning import MultiPathReasoning

        self.reasoning_engine = CognitiveReasoningEngine(llm_router=self.llm_router)
        self.advanced_reasoning = AdvancedReasoningEngine()
        self.multi_path_reasoning = MultiPathReasoning()

        # =====================================
        # CORE KERNEL
        # =====================================

        from core.cognitive_kernel import CognitiveKernel

        self.kernel = CognitiveKernel(storage_backend=self.storage_backend)

        # =====================================
        # EVOLUTION
        # =====================================

        from core.evolution_engine import EvolutionEngine

        self.evolution_engine = EvolutionEngine()

        # =====================================
        # META COGNITION
        # =====================================

        from core.meta_cognition import MetaCognition

        self.meta_cognition = MetaCognition()

        # =====================================
        # INTERNAL SIMULATION
        # =====================================

        from core.internal_simulation_engine import InternalSimulationEngine

        self.simulation_engine = InternalSimulationEngine()

        # =====================================
        # ATTENTION
        # =====================================

        from core.attention_manager import AttentionManager

        self.attention_manager = AttentionManager()

        # =====================================
        # BELIEF ENGINE
        # =====================================

        from core.belief_engine import BeliefEngine

        self.belief_engine = BeliefEngine()

        # =====================================
        # EMOTION
        # =====================================

        from core.emotion_engine import EmotionEngine

        self.emotion_engine = EmotionEngine()

        # =====================================
        # NATURAL RESPONSE
        # =====================================

        from core.natural_response_engine import NaturalResponseEngine

        self.natural_response_engine = NaturalResponseEngine()

        # =====================================
        # DECISION ENGINE
        # =====================================

        from core.decision_engine import DecisionEngine

        self.decision_engine = DecisionEngine()

        # =====================================
        # REFLECTION
        # =====================================

        from core.reflection_engine import ReflectionEngine

        self.reflection_engine = ReflectionEngine()

        # =====================================
        # BEHAVIOR
        # =====================================

        from core.adaptive_behavior_engine import AdaptiveBehaviorEngine

        self.behavior_engine = AdaptiveBehaviorEngine()

        # =====================================
        # TASK ENGINE
        # =====================================

        from core.task_execution_engine import TaskExecutionEngine

        self.task_engine = TaskExecutionEngine()

        # =====================================
        # LEARNING
        # =====================================

        from core.learning_engine import LearningEngine

        self.learning_engine = LearningEngine(system=self)

        # =====================================
        # PLANNER
        # =====================================

        from core.planner_agent import PlannerAgent

        self.planner_agent = PlannerAgent()

        # =====================================
        # TOOLS
        # =====================================

        from core.tool_executor import ToolExecutor

        self.tool_executor = ToolExecutor()

        # =====================================
        # AUTONOMOUS LOOP
        # =====================================

        from core.agent_loop_engine import AgentLoopEngine
        from core.autonomy_engine import AutonomyEngine

        self.agent_loop = AgentLoopEngine()
        self.autonomy_engine = AutonomyEngine()

        self.autonomy_running = False

        self.autonomy_thread = None

        self.autonomy_history = []

        self.autonomy_interval = 5

        # =====================================
        # COGNITIVE STATE
        # =====================================

        self.cognitive_state = {

            "energy": 100,

            "focus": 100,

            "stress": 0,

            "cognitive_load": 0,

            "learning_cycles": 0,

            "self_awareness": 0
        }

        # =====================================
        # DISTRIBUTED MEMORY
        # =====================================

        from core.distributed_memory_manager import DistributedMemoryManager
        from core.memory_priority import MemoryPriority

        self.distributed_memory = DistributedMemoryManager(storage_backend=self.storage_backend)
        self.memory_priority = MemoryPriority()

        # =====================================
        # MEMORY SNAPSHOTS
        # =====================================

        self.memory_snapshots = []

        # =====================================
        # LESSONS LEARNED
        # =====================================

        self.lessons_learned = []

        # =====================================
        # IDENTITY TRAITS
        # =====================================

        self.identity_traits = {

            "core_beliefs": [],

            "learned_patterns": [],

            "key_experiences": []
        }

        # =====================================
        # SIMULATION SAFETY HISTORY
        # =====================================

        self.simulation_safety_history = []

        self.scenario_safety_scores = {}

        # =====================================
        # AUTONOMOUS GOALS
        # =====================================

        self.autonomous_goals = []

        self.goal_evolution_history = []

        self.goal_completion_history = []

        self.goal_opportunities = []

        # =====================================
        # THOUGHT STREAM
        # =====================================

        self.thought_stream = []

        # =====================================
        # INTERNAL DIALOGUE
        # =====================================

        self.internal_dialogue = []

        # =====================================
        # STATS
        # =====================================

        self.runtime_stats = {

            "requests": 0,

            "tasks_completed": 0,

            "boot_time": time.time()
        }

        # Load persistent self-model if present
        try:
            self.load_self_model()
        except Exception:
            # if loading fails, continue with defaults
            pass

    # =====================================
    # AUTONOMOUS LOOP
    # =====================================

    def _autonomous_cycle(

        self

    ):

        while self.autonomy_running:

            cycle_result = self.autonomous_step()

            self.autonomy_history.append(
                cycle_result
            )

            self.runtime_manager.register_task(
                {
                    "type": "autonomous_cycle",
                    "goal": (
                        cycle_result.get(
                            "goal",
                            {}
                        ).get(
                            "goal"
                        )
                    ),
                    "performance": (
                        cycle_result.get(
                            "reflection",
                            {}
                        ).get(
                            "performance_score"
                        )
                    )
                }
            )

            time.sleep(
                self.autonomy_interval
            )

    def autonomous_step(

        self

    ):

        current_goal = self.kernel.select_goal()

        if current_goal is None:

            current_goal = {

                "goal": "maintain internal coherence",

                "priority": 1
            }

        plan = self.planner_agent.create_plan(
            current_goal["goal"]
        )

        execution_results = []

        for step in plan["steps"]:

            if step.get("type") == "tool":

                result = self.execute_step(step)

            else:

                result = {

                    "success": True,

                    "result": (
                        f"Reasoned about: {step.get('action', 'unknown')}"
                    )
                }

            execution_results.append(result)

        reflection = self.reflection_engine.reflect(
            current_goal["goal"],
            execution_results
        )

        self.distributed_memory.store_memory(
            f"Autonomous step: {current_goal['goal']}",
            priority="normal"
        )

        self.semantic_memory.add_memory(
            current_goal["goal"]
        )

        self.belief_engine.reinforce_belief(
            "Autonomy is important.",
            0.05
        )

        self.kernel.update_identity(
            f"Autonomous action completed for goal: {current_goal['goal']}"
        )

        self.kernel.update_world_model(
            {
                "autonomy_step": current_goal["goal"],
                "timestamp": time.time()
            }
        )

        completed_goal = None

        if reflection.get("performance_score", 0) >= 0.7:

            completed_goal = current_goal

            self.kernel.complete_goal(
                current_goal
            )

            self.record_goal_completion(
                current_goal,
                reflection.get(
                    "performance_score",
                    0.0
                )
            )

            self.goal_evolution_history.append({
                "goal": current_goal,
                "completed_at": time.time(),
                "performance_score": reflection.get(
                    "performance_score",
                    0.0
                )
            })

            self.save_self_model()

        elif reflection.get("performance_score", 0) < 0.4:

            current_goal["priority"] = max(
                1,
                current_goal.get("priority", 1) - 1
            )

        if reflection.get("performance_score", 0) < 0.5:

            self.belief_engine.weaken_belief(
                "Autonomy is important.",
                0.05
            )

        return {
            "goal": current_goal,
            "completed_goal": completed_goal,
            "plan": plan,
            "execution_results": execution_results,
            "reflection": reflection
        }

    def start_autonomy(

        self,
        interval=5

    ):

        if self.autonomy_running:

            return {

                "status": "already_running"
            }

        self.autonomy_interval = interval

        self.autonomy_running = True

        self.autonomy_thread = threading.Thread(

            target=self._autonomous_cycle,

            daemon=True
        )

        self.autonomy_thread.start()

        return {

            "status": "started",

            "interval": interval
        }

    def stop_autonomy(

        self

    ):

        if not self.autonomy_running:

            return {

                "status": "not_running"
            }

        self.autonomy_running = False

        if self.autonomy_thread is not None:

            self.autonomy_thread.join(
                timeout=2
            )

        return {

                "status": "stopped"
        }

    def record_goal_completion(

        self,
        goal,
        performance_score

    ):

        entry = {
            "goal": goal,
            "completed_at": time.time(),
            "performance_score": performance_score
        }

        self.goal_completion_history.append(entry)

        if len(self.goal_completion_history) > 100:

            self.goal_completion_history = (
                self.goal_completion_history[-100:]
            )

        # Emit event for goal completion
        self._emit_event("goal_completed", entry)

    def _emit_event(self, event_name: str, data: dict):
        """Emit an event asynchronously (non-blocking)."""
        try:
            # Try to emit in a thread to avoid blocking
            def emit_async():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(
                        self.event_emitter.emit(event_name, data)
                    )
                finally:
                    loop.close()
            
            thread = threading.Thread(target=emit_async, daemon=True)
            thread.start()
        except Exception:
            # If event emission fails, just continue
            pass

    def get_autonomy_status(

        self

    ):

        return {

            "running": self.autonomy_running,

            "history_count": len(
                self.autonomy_history
            ),

            "active_goals": len(
                self.kernel.goals
            )
        }

    # =====================================
    # GENERATE THOUGHT
    # =====================================

    def generate_thought(

        self,
        goal,
        decision,
        personality,
        pressure

    ):

        tone = "stable"

        if pressure >= 7:

            tone = "strained"

        elif personality[
            "confidence"
        ] >= 7:

            tone = "confident"

        elif personality[
            "curiosity"
        ] >= 7:

            tone = "exploratory"

        thought = (

            f"Internal cognitive mode: "
            f"{tone}. "

            f"Analyzing objective "
            f"'{goal}'. "

            f"Strategic selection: "
            f"{decision['action']}."
        )

        self.thought_stream.append(
            thought
        )

        if len(self.thought_stream) > 100:

            self.thought_stream.pop(0)

        return thought

    # =====================================
    # INTERNAL DIALOGUE
    # =====================================

    def generate_internal_dialogue(

        self,
        meta_reflection,
        personality,
        prediction,
        simulation

    ):

        dialogue = []

        confidence = (
            meta_reflection[
                "confidence"
            ]
        )

        uncertainty = (
            meta_reflection[
                "uncertainty"
            ]
        )

        best_future = (

            simulation[
                "comparison"
            ][
                "best_future"
            ][
                "type"
            ]
        )

        if confidence >= 0.8:

            dialogue.append(

                "Strategic confidence elevated."
            )

        if uncertainty >= 0.4:

            dialogue.append(

                "Future outcome remains uncertain."
            )

        if personality[
            "curiosity"
        ] >= 7:

            dialogue.append(

                "Exploration tendency increasing."
            )

        if prediction[
            "risk_level"
        ] == "high":

            dialogue.append(

                "Risk simulation recommends caution."
            )

        if best_future == "transformation":

            dialogue.append(

                "Detected possible pathway evolution."
            )

        if best_future == "failure":

            dialogue.append(

                "Potential instability detected."
            )

        self.internal_dialogue.extend(
            dialogue
        )

        if len(self.internal_dialogue) > 50:

            self.internal_dialogue = (

                self.internal_dialogue[-50:]
            )

        return dialogue

    # =====================================
    # EXECUTE STEP
    # =====================================

    def execute_step(

        self,
        step

    ):

        try:

            if step["type"] == "tool":

                tool = step["tool"]

                if tool == "list_directory":

                    return (

                        self.tool_executor
                        .list_directory(

                            step.get(
                                "path",
                                "."
                            )
                        )
                    )

                elif tool == "read_file":

                    return (

                        self.tool_executor
                        .read_file(

                            step["filepath"]
                        )
                    )

                elif tool == "write_file":

                    return (

                        self.tool_executor
                        .write_file(

                            step["filepath"],

                            step["content"]
                        )
                    )

                elif tool == "execute_python":

                    return (

                        self.tool_executor
                        .execute_python(

                            step["script_path"]
                        )
                    )

                elif tool == "execute_command":

                    return (

                        self.tool_executor
                        .execute_command(

                            step["command"]
                        )
                    )

            return {

                "success": True,

                "result": (

                    f"Completed step: "
                    f"{step.get('action')}"
                )
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)
            }

    # =====================================
    # UPDATE STATE
    # =====================================

    def update_cognitive_state(

        self,
        pressure,
        tension

    ):

        self.cognitive_state[
            "cognitive_load"
        ] += 1

        self.cognitive_state[
            "learning_cycles"
        ] += 1

        self.cognitive_state[
            "stress"
        ] = pressure

        self.cognitive_state[
            "self_awareness"
        ] += 1

        self.cognitive_state[
            "energy"
        ] -= random.randint(0, 2)

        self.cognitive_state[
            "focus"
        ] -= int(tension * 0.1)

        if self.cognitive_state[
            "energy"
        ] < 0:

            self.cognitive_state[
                "energy"
            ] = 0

        if self.cognitive_state[
            "focus"
        ] < 0:

            self.cognitive_state[
                "focus"
            ] = 0

    # =====================================
    # PERSISTENT SELF MODEL
    # =====================================

    def load_self_model(

        self,
        path="self_model.json"

    ):

        storage_key = path.replace("/", "_").replace("..", "_")
        data = self.storage_backend.get(
            storage_key,
            default={
                "identity_traits": {},
                "autonomous_goals": [],
                "kernel_goals": self.kernel.goals,
                "autonomy_history": [],
                "goal_evolution_history": [],
                "goal_completion_history": []
            }
        )

        if isinstance(data, dict):
            self.identity_traits.update(
                data.get("identity_traits", {})
            )

            self.autonomous_goals = data.get(
                "autonomous_goals",
                self.autonomous_goals
            )

            self.kernel.load_goals(
                data.get(
                    "kernel_goals",
                    self.kernel.goals
                )
            )

            self.autonomy_history = data.get(
                "autonomy_history",
                self.autonomy_history
            )

            self.goal_evolution_history = data.get(
                "goal_evolution_history",
                self.goal_evolution_history
            )

            self.goal_completion_history = data.get(
                "goal_completion_history",
                self.goal_completion_history
            )

        return True

    def save_self_model(

        self,
        path="self_model.json"

    ):

        storage_key = path.replace("/", "_").replace("..", "_")
        data = {

            "identity_traits": (
                self.identity_traits
            ),

            "autonomous_goals": (
                self.autonomous_goals
            ),

            "kernel_goals": (
                self.kernel.goals
            ),

            "autonomy_history": (
                self.autonomy_history
            ),

            "goal_evolution_history": (
                self.goal_evolution_history
            ),

            "goal_completion_history": (
                self.goal_completion_history
            ),

            "timestamp": time.time()
        }

        return self.storage_backend.set(storage_key, data)

    def consolidate_identity(

        self

    ):

        # Merge learned patterns from lessons
        patterns = set(
            self.identity_traits.get("learned_patterns", [])
        )

        for lesson in self.lessons_learned:

            text = str(lesson.get("experience", ""))

            tokens = [t.strip() for t in text.split() if len(t) > 3]

            for t in tokens:
                patterns.add(t.lower())

        # Keep top N patterns
        patterns_list = list(patterns)[:50]

        self.identity_traits["learned_patterns"] = (
            patterns_list
        )

        # Update core beliefs from worldview if present
        if isinstance(self.identity_traits.get("core_beliefs"), list):
            # ensure uniqueness
            self.identity_traits["core_beliefs"] = list(
                dict.fromkeys(self.identity_traits["core_beliefs"])
            )

        # Persist model
        self.save_self_model()

    # =====================================
    # MAIN PROCESS
    # =====================================

    def generate_goals_from_beliefs(

        self,
        worldview

    ):

        if not worldview:
            return []

        created = []
        for belief in worldview:
            text = str(belief).lower()
            if "technology" in text or "humanity" in text or "help" in text:
                goal_text = "Develop technology to help humanity"
            elif "learning" in text:
                goal_text = "Create a continuous learning roadmap"
            elif "robot" in text:
                goal_text = "Build robotics systems"
            elif "research" in text:
                goal_text = "Research practical applications of current beliefs"
            else:
                goal_text = f"Translate belief into an actionable goal: {belief}"

            if not self.kernel.contains_goal(goal_text):
                created.append(
                    self.kernel.add_goal(
                        goal_text,
                        priority=7
                    )
                )

        return created

    def process(self, user_input):

        try:

            # =====================================
            # STATS
            # =====================================

            self.runtime_stats[
                "requests"
            ] += 1

            # =====================================
            # MEMORY
            # =====================================

            self.semantic_memory.add_memory(
                user_input
            )

            self.vector_memory.store_memory(
                user_input
            )

            related_memories = (

                self.semantic_memory
                .search_memory(
                    user_input
                )
            )

            # =====================================
            # BELIEFS
            # =====================================

            self.belief_engine.extract_beliefs(
                user_input
            )

            worldview = (

                self.belief_engine
                .infer_worldview()
            )

            if "generate goals" in user_input.lower() or "goals aligned" in user_input.lower():
                self.generate_goals_from_beliefs(worldview)

            contradictions = (

                self.belief_engine
                .detect_contradictions()
            )

            # =====================================
            # ATTENTION
            # =====================================

            attention_focus = (
                self.attention_manager
                .update_attention(
                    user_input
                )
            )

            reasoning_budget = (
                attention_focus.get(
                    "focus_level",
                    50
                ) / 100.0
            )

            selected_count = int(
                len(related_memories) * reasoning_budget
            )
            if selected_count == 0 and related_memories:
                selected_count = 1

            selected_memories = (
                related_memories[:selected_count]
                if reasoning_budget > 0
                else related_memories
            )

            # =====================================
            # WORLD MODEL
            # =====================================

            self.kernel.update_world_model(
                user_input
            )

            self.kernel.update_identity(
                user_input
            )

            current_goal = (
                self.kernel.select_goal()
            )

            # =====================================
            # EMOTION
            # =====================================

            emotion_data = (

                self.emotion_engine
                .detect_emotion(
                    user_input
                )
            )

            # =====================================
            # REASONING
            # =====================================

            reasoning_analysis = (

                self.advanced_reasoning
                .analyze_goal(
                    user_input
                )
            )

            # =====================================
            # STRATEGIES
            # =====================================

            strategies = (

                self.multi_path_reasoning
                .generate_strategies(
                    user_input
                )
            )

            strategy_evaluation = (

                self.multi_path_reasoning
                .evaluate_strategies(
                    strategies
                )
            )

            strategy_explanation = (

                self.multi_path_reasoning
                .explain_strategy(
                    strategy_evaluation
                )
            )

            # =====================================
            # SIMULATION SANDBOX
            # =====================================

            sandbox_simulation = (
                self.simulation_engine
                .generate_future_scenarios(

                    user_input,

                    self.evolution_engine
                    .personality,

                    0.0
                )
            )

            sandbox_comparison = (
                self.simulation_engine
                .compare_scenarios(
                    sandbox_simulation
                )
            )

            # =====================================
            # STRATEGY SAFETY SCORING
            # =====================================

            best_future_type = (
                sandbox_comparison[
                    "best_future"
                ]["type"]
            )

            strategy_safety_score = 0.5

            if best_future_type == "success":

                strategy_safety_score = 0.9

            elif best_future_type == "failure":

                strategy_safety_score = 0.2

            else:

                strategy_safety_score = 0.5

            self.scenario_safety_scores = {

                "best_future": (
                    best_future_type
                ),

                "safety_score": (
                    strategy_safety_score
                ),

                "recommendation": (
                    sandbox_comparison[
                        "analysis"
                    ]
                )
            }

            self.simulation_safety_history.append(
                self.scenario_safety_scores
            )

            if len(
                self.simulation_safety_history
            ) > 100:

                self.simulation_safety_history = (
                    self.simulation_safety_history[
                        -100:
                    ]
                )

            # =====================================
            # DECISION
            # =====================================

            decision = (

                self.decision_engine
                .decide(

                    goal=user_input,

                    reasoning_analysis=(
                        reasoning_analysis
                    ),

                    cognitive_state=(
                        self.cognitive_state
                    )
                )
            )

            # =====================================
            # PLANNING
            # =====================================

            plan = (

                self.planner_agent
                .create_plan(
                    user_input
                )
            )

            # =====================================
            # EXECUTION
            # =====================================

            execution_results = []

            for step in plan["steps"]:

                result = (
                    self.execute_step(
                        step
                    )
                )

                execution_results.append(
                    result
                )

            # =====================================
            # REFLECTION
            # =====================================

            reflection = (

                self.reflection_engine
                .reflect(

                    user_input,

                    execution_results
                )
            )

            adaptation = (

                self.advanced_reasoning
                .learn_from_reflection(
                    reflection
                )
            )

            # =====================================
            # MEMORY PRIORITY CALCULATION
            # =====================================

            memory_priority_score = (
                self.memory_priority
                .calculate_priority(
                    user_input,
                    emotion_data[
                        "emotion"
                    ]
                )
            )

            # =====================================
            # LONG-TERM MEMORY STORAGE
            # =====================================

            self.distributed_memory.store_memory(
                f"{user_input}",
                priority=memory_priority_score[
                    "level"
                ]
            )

            # =====================================
            # LESSON EXTRACTION
            # =====================================

            if memory_priority_score[
                "level"
            ] in ["high", "critical"]:

                lesson = {

                    "experience": (
                        user_input
                    ),

                    "outcome": (
                        reflection.get(
                            "performance_score",
                            0.5
                        )
                    ),

                    "priority": (
                        memory_priority_score[
                            "level"
                        ]
                    ),

                    "emotion": (
                        emotion_data[
                            "emotion"
                        ]
                    )
                }

                self.lessons_learned.append(
                    lesson
                )

            # =====================================
            # IDENTITY PRESERVATION
            # =====================================

            self.identity_traits[
                "core_beliefs"
            ] = worldview.get(
                "core_beliefs",
                self.identity_traits[
                    "core_beliefs"
                ]
            ) if isinstance(
                worldview,
                dict
            ) else self.identity_traits[
                "core_beliefs"
            ]

            if memory_priority_score[
                "score"
            ] >= 30:

                self.identity_traits[
                    "key_experiences"
                ].append(user_input)

                if len(
                    self.identity_traits[
                        "key_experiences"
                    ]
                ) > 50:

                    self.identity_traits[
                        "key_experiences"
                    ] = self.identity_traits[
                        "key_experiences"
                    ][-50:]

            # =====================================
            # MEMORY SNAPSHOTS
            # =====================================

            snapshot = {

                "timestamp": time.time(),

                "memories_count": len(
                    related_memories
                ),

                "priority_memories": len(
                    self.distributed_memory
                    .get_priority_memory()
                ),

                "lessons_count": len(
                    self.lessons_learned
                ),

                "identity_traits": (
                    self.identity_traits
                )
            }

            self.memory_snapshots.append(
                snapshot
            )

            if len(
                self.memory_snapshots
            ) > 100:

                self.memory_snapshots = (
                    self.memory_snapshots[-100:]
                )

            # =====================================
            # MEMORY COMPRESSION
            # =====================================

            memory_summary = (

                self.evolution_engine
                .compress_memory(
                    related_memories
                )
            )

            # =====================================
            # AUTONOMOUS GOAL GENERATION
            # =====================================

            autonomous_new_goals = []

            # =========================
            # OPPORTUNITY 1: BELIEF GAPS
            # =========================

            if isinstance(
                contradictions,
                list
            ) and len(
                contradictions
            ) > 0:

                autonomous_new_goals.append({

                    "source": (
                        "belief_contradiction"
                    ),

                    "objective": (
                        "Resolve internal "
                        "contradictions"
                    ),

                    "priority": "high",

                    "reason": (
                        f"Detected {len(
                            contradictions
                        )} belief conflicts"
                    )
                })

            # =========================
            # OPPORTUNITY 2: LEARNING GAPS
            # =========================

            if len(
                self.lessons_learned
            ) > 3:

                avg_outcome = sum([
                    l.get(
                        "outcome",
                        0.5
                    ) for l in (
                        self.lessons_learned[
                            -3:
                        ]
                    )
                ]) / 3

                if avg_outcome < 0.6:

                    autonomous_new_goals.append({

                        "source": (
                            "low_performance"
                        ),

                        "objective": (
                            "Improve decision "
                            "quality"
                        ),

                        "priority": "high",

                        "reason": (
                            f"Recent performance "
                            f"score: {avg_outcome}"
                        )
                    })

            # =========================
            # OPPORTUNITY 3: SIMULATION PATHS
            # =========================

            if best_future_type == "transformation":

                autonomous_new_goals.append({

                    "source": (
                        "simulation_opportunity"
                    ),

                    "objective": (
                        "Explore transformation "
                        "pathway"
                    ),

                    "priority": "medium",

                    "reason": (
                        "Simulation predicts "
                        "evolutionary potential"
                    )
                })

            # =========================
            # OPPORTUNITY 4: IDENTITY GROWTH
            # =========================

            if len(
                self.identity_traits[
                    "key_experiences"
                ]
            ) > 10:

                autonomous_new_goals.append({

                    "source": (
                        "identity_evolution"
                    ),

                    "objective": (
                        "Consolidate identity "
                        "and self-model"
                    ),

                    "priority": "medium",

                    "reason": (
                        "Accumulated significant "
                        "experience set"
                    )
                })

            

            # =====================================
            # GOAL EVOLUTION
            # =====================================

            evolved_goals = (

                self.evolution_engine
                .evolve_goals(

                    self.kernel.goals,

                    reflection.get(
                        "performance_score",
                        0.5
                    )
                )
            )

            self.kernel.goals = (
                evolved_goals
            )

            # =====================================
            # PREDICTION
            # =====================================

            prediction = (

                self.evolution_engine
                .predict_outcome(

                    strategy_evaluation[
                        "best_strategy"
                    ]["name"]
                )
            )

            # =====================================
            # PERSONALITY
            # =====================================

            personality = (

                self.evolution_engine
                .drift_personality(

                    emotion_data[
                        "emotion"
                    ],

                    reflection.get(
                        "performance_score",
                        0.5
                    )
                )
            )

            # =====================================
            # META COGNITION
            # =====================================

            meta_reflection = (

                self.meta_cognition
                .reflect_on_response(

                    user_input,

                    prediction
                )
            )

            emotional_pressure = (

                self.meta_cognition
                .update_emotional_pressure(

                    emotion_data[
                        "emotion"
                    ]
                )
            )

# Ensure `cognitive_tension` exists even if evaluate_tension fails or is skipped
            try:
                cognitive_tension = (
                    self.meta_cognition
                    .evaluate_tension(
                        self.kernel.goals
                    )
                )
            except Exception:
                cognitive_tension = 0

            # =====================================
            # OPPORTUNITY 5: COGNITIVE TENSION (now handled after computation)

            if cognitive_tension > 0.7:

                autonomous_new_goals.append({

                    "source": (
                        "cognitive_tension"
                    ),

                    "objective": (
                        "Reduce internal tension"
                    ),

                    "priority": "critical",

                    "reason": (
                        "High cognitive tension "
                        "detected"
                    )
                })

            # finalize autonomous goals

            self.goal_opportunities = (
                autonomous_new_goals
            )

            self.autonomous_goals.extend(
                autonomous_new_goals
            )

            if len(
                self.autonomous_goals
            ) > 100:

                self.autonomous_goals = (
                    self.autonomous_goals[-100:]
                )

            # =====================================
            # INTERNAL SIMULATION
            # =====================================

            simulation = (

                self.simulation_engine
                .run_simulation(

                    user_input,

                    personality,

                    emotional_pressure
                )
            )

            # =====================================
            # THOUGHT
            # =====================================

            thought = (

                self.generate_thought(

                    user_input,

                    decision,

                    personality,

                    emotional_pressure
                )
            )

            # =====================================
            # DIALOGUE
            # =====================================

            internal_dialogue = (

                self.generate_internal_dialogue(

                    meta_reflection,

                    personality,

                    prediction,

                    simulation
                )
            )

            # =====================================
            # LEARNING
            # =====================================

            decision_learning = (

                self.decision_engine
                .adapt_from_learning(
                    adaptation
                )
            )

            # =====================================
            # UPDATE STATE
            # =====================================

            # safe fallback in case cognitive_tension wasn't set earlier
            cognitive_tension = locals().get("cognitive_tension", 0)
            self.update_cognitive_state(
                emotional_pressure,
                cognitive_tension
            )

            # Consolidate and persist self-model periodically
            if self.cognitive_state.get("learning_cycles", 0) % 5 == 0:
                try:
                    self.consolidate_identity()
                except Exception:
                    pass

            # =====================================
            # BEHAVIOR
            # =====================================

            behavior = (

                self.behavior_engine
                .adapt_behavior(

                    emotion=emotion_data[
                        "emotion"
                    ],

                    priority=decision[
                        "priority"
                    ]
                )
            )

            # =====================================
            # CONTINUOUS THINKING
            # =====================================

            background_thought = (
                self.kernel.think()
            )

            # =====================================
            # SYSTEM DATA
            # =====================================

            system_data = {

                "input": user_input,

                "emotion_data": (
                    emotion_data
                ),

                "thought": thought,

                "internal_dialogue": (
                    internal_dialogue
                ),

                "decision": decision,

                "reasoning_analysis": (
                    reasoning_analysis
                ),

                "strategy_evaluation": (
                    strategy_evaluation
                ),

                "strategy_explanation": (
                    strategy_explanation
                ),

                "plan": plan,

                "execution_results": (
                    execution_results
                ),

                "reflection": (
                    reflection
                ),

                "adaptation": (
                    adaptation
                ),

                "decision_learning": (
                    decision_learning
                ),

                "behavior": behavior,

                "memories": (
                    selected_memories
                ),

                "attention_focus": (
                    attention_focus
                ),

                "reasoning_budget": (
                    reasoning_budget
                ),

                "memory_priority_score": (
                    memory_priority_score
                ),

                "lessons_learned": (
                    self.lessons_learned[
                        -5:
                    ] if len(
                        self.lessons_learned
                    ) > 0 else []
                ),

                "identity_traits": (
                    self.identity_traits
                ),

                "distributed_memory_stats": (
                    self.distributed_memory
                    .get_memory_stats()
                ),

                "simulation_sandbox": {

                    "scenarios": (
                        sandbox_simulation
                    ),

                    "best_future": (
                        sandbox_comparison[
                            "best_future"
                        ]
                    ),

                    "safety_analysis": (
                        sandbox_comparison[
                            "analysis"
                        ]
                    )
                },

                "strategy_safety_score": (
                    strategy_safety_score
                ),

                "memory_summary": (
                    memory_summary
                ),

                "prediction": (
                    prediction
                ),

                "personality": (
                    personality
                ),

                "meta_reflection": (
                    meta_reflection
                ),

                "emotional_pressure": (
                    emotional_pressure
                ),

                "cognitive_tension": (
                    locals().get("cognitive_tension", 0)
                ),

                "simulation": (
                    simulation
                ),

                "active_goal": (
                    current_goal
                ),

                "background_thought": (
                    background_thought
                ),

                "cognitive_state": (
                    self.cognitive_state
                ),

                "autonomous_goals_generated": (
                    autonomous_new_goals
                ),

                "goal_opportunities": (
                    self.goal_opportunities
                ),

                "beliefs": worldview,

                "contradictions": (
                    contradictions
                )
            }

            # =====================================

            llm_reasoning = (

                self.reasoning_engine
                .reason(system_data)
            )

            system_data[
                "llm_reasoning"
            ] = llm_reasoning

            # =====================================
            # NATURAL RESPONSE
            # =====================================

            natural_response = (

                self.natural_response_engine
                .generate(system_data)
            )

            # =====================================
            # TASK STATS
            # =====================================

            self.runtime_stats[
                "tasks_completed"
            ] += len(
                execution_results
            )

            # =====================================
            # FINAL RESPONSE
            # =====================================

            return {

                "response": (
                    natural_response
                ),

                "emotion": (
                    emotion_data[
                        "emotion"
                    ]
                ),

                "thought": thought,

                "simulation": (
                    simulation
                ),

                "internal_dialogue": (
                    internal_dialogue
                ),

                "active_goal": (
                    current_goal
                ),

                "background_thought": (
                    background_thought
                ),

                "memory_summary": (
                    memory_summary
                ),

                "prediction": (
                    prediction
                ),

                "personality": (
                    personality
                ),

                "meta_reflection": (
                    meta_reflection
                ),

                "emotional_pressure": (
                    emotional_pressure
                ),

                "cognitive_tension": (
                    cognitive_tension
                ),

                "strategy": (

                    strategy_evaluation[
                        "best_strategy"
                    ]["name"]
                ),

                "strategy_safety_score": (
                    strategy_safety_score
                ),

                "simulation_sandbox": {

                    "scenarios": (
                        sandbox_simulation
                    ),

                    "best_future": (
                        sandbox_comparison[
                            "best_future"
                        ]
                    ),

                    "safety_analysis": (
                        sandbox_comparison[
                            "analysis"
                        ]
                    )
                },

                "autonomous_goals_generated": (
                    autonomous_new_goals
                ),

                "goal_opportunities": (
                    self.goal_opportunities
                ),

                "cognitive_state": (
                    self.cognitive_state
                ),

                "attention_focus": (
                    attention_focus
                ),

                "reasoning_budget": (
                    reasoning_budget
                ),

                "memory_priority_score": (
                    memory_priority_score
                ),

                "lessons_learned": (
                    self.lessons_learned[
                        -5:
                    ] if len(
                        self.lessons_learned
                    ) > 0 else []
                ),

                "identity_traits": (
                    self.identity_traits
                ),

                "beliefs": worldview,

                "contradictions": (
                    contradictions
                ),

                "status": "success"
            }

        except Exception as e:

            return {

                "status": "error",

                "error": str(e)
            }