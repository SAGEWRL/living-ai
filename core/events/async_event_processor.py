# core/events/async_event_processor.py

import threading
import time


class AsyncEventProcessor:

    def __init__(
        self,
        event_queue,
        event_bus
    ):

        self.event_queue = (
            event_queue
        )

        self.event_bus = (
            event_bus
        )

        self.running = False

        self.thread = None

    # =========================
    # START PROCESSOR
    # =========================

    def start(self):

        if not self.running:

            self.running = True

            self.thread = threading.Thread(

                target=self.process_loop,

                daemon=True
            )

            self.thread.start()

            print(
                "\n[ASYNC PROCESSOR STARTED]"
            )

    # =========================
    # STOP PROCESSOR
    # =========================

    def stop(self):

        self.running = False

        print(
            "\n[ASYNC PROCESSOR STOPPED]"
        )

    # =========================
    # PROCESS LOOP
    # =========================

    def process_loop(self):

        while self.running:

            event = self.event_queue.pop()

            if event:

                print(
                    "\n[ASYNC EVENT]"
                )

                print(event)

            time.sleep(0.1)