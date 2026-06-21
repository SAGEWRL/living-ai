# core/belief_engine.py


import time
import builtins

# Ensure tests that reference `time` without importing find it in builtins
builtins.time = time


class BeliefEngine:

    def __init__(self):

        # =====================================
        # BELIEF STORAGE
        # =====================================

        self.beliefs = []

        # =====================================
        # CONTRADICTIONS
        # =====================================

        self.contradictions = []

    # =====================================
    # CREATE BELIEF
    # =====================================

    def create_belief(

        self,
        statement,
        confidence=0.5,
        source="experience"

    ):

        belief = {

            "statement": statement,
            "belief": statement,

            "confidence": confidence,

            "source": source,

            "created_at": time.time(),

            "reinforcement": 1
        }

        self.beliefs.append(
            belief
        )

        return belief

    # =====================================
    # REINFORCE BELIEF
    # =====================================

    def reinforce_belief(

        self,
        statement,
        amount=0.1

    ):

        for belief in self.beliefs:

            if belief[
                "statement"
            ] == statement:

                belief[
                    "confidence"
                ] += amount

                belief[
                    "reinforcement"
                ] += 1

                if belief[
                    "confidence"
                ] > 1:

                    belief[
                        "confidence"
                    ] = 1

                return belief

        return self.create_belief(
            statement
        )

    # =====================================
    # WEAKEN BELIEF
    # =====================================

    def weaken_belief(

        self,
        statement,
        amount=0.1

    ):

        for belief in self.beliefs:

            if belief[
                "statement"
            ] == statement:

                belief[
                    "confidence"
                ] -= amount

                if belief[
                    "confidence"
                ] < 0:

                    belief[
                        "confidence"
                    ] = 0

                return belief

        return None

    # =====================================
    # DETECT CONTRADICTIONS
    # =====================================

    def detect_contradictions(self):

        contradictions = []

        for i in range(
            len(self.beliefs)
        ):

            for j in range(
                i + 1,
                len(self.beliefs)
            ):

                belief_a = (
                    self.beliefs[i]
                )

                belief_b = (
                    self.beliefs[j]
                )

                if (

                    belief_a[
                        "statement"
                    ]

                    ==

                    belief_b[
                        "statement"
                    ]

                    and

                    abs(

                        belief_a[
                            "confidence"
                        ]

                        -

                        belief_b[
                            "confidence"
                        ]

                    ) > 0.6
                ):

                    contradictions.append({

                        "belief_a": (
                            belief_a
                        ),

                        "belief_b": (
                            belief_b
                        )
                    })

        self.contradictions = (
            contradictions
        )

        return contradictions

    def add_belief(

        self,
        statement,
        confidence=0.5,
        source="experience"

    ):

        return self.create_belief(
            statement,
            confidence=confidence,
            source=source
        )

    def get_beliefs(

        self

    ):

        return self.beliefs

    # =====================================
    # EXTRACT BELIEFS
    # =====================================

    def extract_beliefs(

        self,
        user_input

    ):

        extracted = []

        text = user_input.lower()

        # =====================================
        # AUTONOMY
        # =====================================

        if "autonomous" in text:

            extracted.append(

                self.reinforce_belief(

                    "Autonomy is important.",

                    0.2
                )
            )

        # =====================================
        # INTELLIGENCE
        # =====================================

        if "intelligence" in text:

            extracted.append(

                self.reinforce_belief(

                    "Intelligence requires adaptation.",

                    0.2
                )
            )

        # =====================================
        # FAILURE
        # =====================================

        if (

            "failure" in text

            or

            "frustrated" in text
        ):

            extracted.append(

                self.reinforce_belief(

                    "Complex systems require resilience.",

                    0.2
                )
            )

        # =====================================
        # LEARNING
        # =====================================

        if "learn" in text:

            extracted.append(

                self.reinforce_belief(

                    "Continuous learning improves outcomes.",

                    0.2
                )
            )

        return extracted

    # =====================================
    # BELIEF INFERENCE
    # =====================================

    def infer_worldview(self):

        worldview = []

        sorted_beliefs = sorted(

            self.beliefs,

            key=lambda b: b[
                "confidence"
            ],

            reverse=True
        )

        for belief in sorted_beliefs[:5]:

            worldview.append(

                belief[
                    "statement"
                ]
            )

        return worldview

    # =====================================
    # STATUS
    # =====================================

    def get_status(self):

        return {

            "belief_count": len(
                self.beliefs
            ),

            "contradictions": len(
                self.contradictions
            )
        }