# core/attention_manager.py


class AttentionManager:

    def __init__(self):

        self.current_focus = None

        self.focus_level = 0

    # =========================
    # UPDATE ATTENTION
    # =========================

    def update_attention(
        self,
        input_text
    ):

        self.current_focus = (
            input_text
        )

        self.focus_level = min(

            len(input_text) / 10,

            100
        )

        return {

            "focus": (
                self.current_focus
            ),

            "focus_level": (
                self.focus_level
            )
        }

    # =========================
    # GET CURRENT FOCUS
    # =========================

    def get_focus(self):

        return {

            "focus": (
                self.current_focus
            ),

            "focus_level": (
                self.focus_level
            )
        }