# core/memory_priority.py


class MemoryPriority:

    def __init__(self):

        self.high_priority_keywords = [

            "dream",
            "goal",
            "future",
            "love",
            "fear",
            "pain",
            "success",
            "company",
            "life",
            "death"
        ]

    def calculate_priority(
        self,
        text,
        emotion
    ):

        score = 0

        text_lower = text.lower()

        # =========================
        # KEYWORD IMPORTANCE
        # =========================

        for keyword in (

            self.high_priority_keywords
        ):

            if keyword in text_lower:

                score += 20

        # =========================
        # EMOTIONAL IMPORTANCE
        # =========================

        if emotion == "sad":

            score += 15

        elif emotion == "angry":

            score += 10

        elif emotion == "happy":

            score += 5

        # =========================
        # LENGTH IMPORTANCE
        # =========================

        score += min(
            len(text) // 10,
            20
        )

        # =========================
        # PRIORITY LEVEL
        # =========================

        if score >= 50:

            level = "critical"

        elif score >= 30:

            level = "high"

        elif score >= 15:

            level = "medium"

        else:

            level = "low"

        return {

            "score": score,

            "level": level
        }