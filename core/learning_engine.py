# core/learning_engine.py

from core.event_bus import bus

weights = {"sad": 1, "happy": 1, "angry": 1}

def learning_engine(text):
    t = text.lower()

    if "sad" in t:
        weights["sad"] += 1

    if "happy" in t:
        weights["happy"] += 1

    if "angry" in t:
        weights["angry"] += 1

    return {"learning": weights}


class LearningEngine:

    def __init__(self, system=None):
        self.system = system
        self.weights = {"sad": 1, "happy": 1, "angry": 1}
        self.lessons = []

    def record_lesson(self, lesson):
        self.lessons.append(lesson)
        if self.system is not None and hasattr(self.system, "lessons_learned"):
            self.system.lessons_learned.append(lesson)
        return {
            "status": "recorded",
            "lesson": lesson
        }

    def process(self, text):
        t = text.lower()

        if "sad" in t:
            self.weights["sad"] += 1

        if "happy" in t:
            self.weights["happy"] += 1

        if "angry" in t:
            self.weights["angry"] += 1

        return {"learning": self.weights}


bus.subscribe("input", learning_engine)