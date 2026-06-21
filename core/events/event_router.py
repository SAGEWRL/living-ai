# core/events/event_router.py


class EventRouter:

    def __init__(
        self,
        event_bus,
        event_queue
    ):

        self.event_bus = event_bus

        self.event_queue = event_queue

    # =========================
    # ROUTE EVENT
    # =========================

    def route(
        self,
        event_name,
        data
    ):

        event = {

            "event": event_name,

            "data": data
        }

        self.event_queue.push(
            event
        )

        self.event_bus.emit(
            event_name,
            data
        )

    # =========================
    # PROCESS QUEUE
    # =========================

    def process_queue(self):

        while (
            self.event_queue.size() > 0
        ):

            event = (
                self.event_queue.pop()
            )

            print(
                "\n[QUEUE PROCESSING]"
            )

            print(event)