# core/emotion_engine.py


class EmotionEngine:

    def __init__(self):

        self.emotional_history = []

    # =========================
    # DETECT EMOTION
    # =========================

    def detect_emotion(

        self,
        text

    ):

        text_lower = text.lower()

        emotion = {

            "emotion": "neutral",

            "confidence": 0.5,

            "intensity": 1
        }

        # =========================
        # STRESS / FRUSTRATION
        # =========================

        stress_words = [

            "angry",
            "frustrated",
            "annoyed",
            "stressed",
            "hate",
            "broken",
            "tired",
            "upset"
        ]

        # =========================
        # SADNESS
        # =========================

        sad_words = [

            "sad",
            "depressed",
            "hurt",
            "cry",
            "lonely",
            "empty"
        ]

        # =========================
        # EXCITEMENT
        # =========================

        excited_words = [

            "awesome",
            "excited",
            "great",
            "amazing",
            "love",
            "perfect",
            "lets go"
        ]

        # =========================
        # DETECTION
        # =========================

        for word in stress_words:

            if word in text_lower:

                emotion["emotion"] = (
                    "frustrated"
                )

                emotion["confidence"] = 0.8

                emotion["intensity"] = 7

        for word in sad_words:

            if word in text_lower:

                emotion["emotion"] = (
                    "sad"
                )

                emotion["confidence"] = 0.8

                emotion["intensity"] = 6

        for word in excited_words:

            if word in text_lower:

                emotion["emotion"] = (
                    "excited"
                )

                emotion["confidence"] = 0.9

                emotion["intensity"] = 8

        self.emotional_history.append(
            emotion
        )

        return emotion

    # =========================
    # RESPONSE STYLE
    # =========================

    def process_emotion(

        self,
        text,
        intensity=None

    ):

        return self.detect_emotion(text)


    def response_style(

        self,
        emotion_data

    ):

        emotion = emotion_data.get(
            "emotion",
            "neutral"
        )

        style = {

            "tone": "balanced",

            "verbosity": "normal"
        }

        # =========================
        # FRUSTRATED
        # =========================

        if emotion == "frustrated":

            style["tone"] = (
                "calm_supportive"
            )

            style["verbosity"] = (
                "focused"
            )

        # =========================
        # SAD
        # =========================

        elif emotion == "sad":

            style["tone"] = (
                "empathetic"
            )

            style["verbosity"] = (
                "gentle"
            )

        # =========================
        # EXCITED
        # =========================

        elif emotion == "excited":

            style["tone"] = (
                "energetic"
            )

            style["verbosity"] = (
                "expressive"
            )

        return style

    # =========================
    # STATUS
    # =========================

    def get_status(self):

        return {

            "emotional_interactions": len(
                self.emotional_history
            )
        }