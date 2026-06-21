# core/events/event_bus.py


class EventBus:

    def __init__(self):

        self.listeners = {}

        self.event_history = []

    # =========================
    # REGISTER LISTENER
    # =========================

    def subscribe(
        self,
        event_name,
        callback
    ):

        if event_name not in self.listeners:

            self.listeners[event_name] = []

        self.listeners[
            event_name
        ].append(callback)

    # =========================
    # REMOVE LISTENER
    # =========================

    def unsubscribe(
        self,
        event_name,
        callback
    ):

        if event_name in self.listeners:

            if callback in self.listeners[
                event_name
            ]:

                self.listeners[
                    event_name
                ].remove(callback)

    # =========================
    # EMIT EVENT
    # =========================

    def emit(
        self,
        event_name,
        data
    ):

        event_payload = {

            "event": event_name,

            "data": data
        }

        self.event_history.append(
            event_payload
        )

        if event_name in self.listeners:

            for callback in self.listeners[
                event_name
            ]:

                callback(
                    event_payload
                )

    # =========================
    # GET HISTORY
    # =========================

    def get_history(self):

        return self.event_history