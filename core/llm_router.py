# core/llm_router.py

import requests


class LLMRouter:

    def __init__(self):

        self.base_url = (
            "http://localhost:11434/api/generate"
        )

        # VERY LIGHT MODEL
        self.model = "phi3"

    # =========================
    # GENERATE
    # =========================

    def generate(

        self,
        prompt,
        system_prompt=None

    ):

        try:

            # =========================
            # SHORT PROMPT
            # =========================

            final_prompt = (
                str(prompt)
            )[:300]

            # =========================
            # REQUEST
            # =========================

            response = requests.post(

                self.base_url,

                json={

                    "model": self.model,

                    "prompt": final_prompt,

                    "stream": False,

                    "options": {

                        "num_predict": 80,

                        "temperature": 0.7
                    }
                },

                timeout=60
            )

            # =========================
            # RESPONSE
            # =========================

            data = response.json()

            return {

                "success": True,

                "response": data.get(
                    "response",
                    ""
                )
            }

        except Exception as e:

            return {

                "success": False,

                "response": (
                    "Local reasoning timeout."
                ),

                "error": str(e)
            }

    # =========================
    # TEST CONNECTION
    # =========================

    def test_connection(self):

        try:

            response = requests.get(

                "http://localhost:11434/api/tags",

                timeout=10
            )

            return {

                "connected": (
                    response.status_code == 200
                )
            }

        except Exception as e:

            return {

                "connected": False,

                "error": str(e)
            }