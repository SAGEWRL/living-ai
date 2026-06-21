# core/events/event_queue.py


class EventQueue:

    def __init__(self):

        self.queue = []

    # =========================
    # PUSH EVENT
    # =========================

    def push(
        self,
        event
    ):

        self.queue.append(
            event
        )

    # =========================
    # POP EVENT
    # =========================

    def pop(self):

        if len(self.queue) == 0:

            return None

        return self.queue.pop(0)

    # =========================
    # QUEUE SIZE
    # =========================

    def size(self):

        return len(
            self.queue
        )

    # =========================
    # CLEAR QUEUE
    # =========================

    def clear(self):

        self.queue = []