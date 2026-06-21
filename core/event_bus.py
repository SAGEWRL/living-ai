# core/event_bus.py

class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, fn):
        self.listeners.setdefault(event, []).append(fn)

    def emit(self, event, data):
        results = []

        for fn in self.listeners.get(event, []):
            try:
                results.append(fn(data))
            except Exception as e:
                results.append({"error": str(e)})

        return results


bus = EventBus()