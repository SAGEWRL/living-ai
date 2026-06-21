# core/events/event_logger.py


class EventLogger:

    def __init__(self):

        self.logs = []

    def log_event(
        self,
        payload
    ):

        self.logs.append(
            payload
        )

        print(
            "\n[EVENT]"
        )

        print(payload)

    def get_logs(self):

        return self.logs