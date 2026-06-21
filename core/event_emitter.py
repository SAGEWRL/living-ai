# core/event_emitter.py
"""Simple event emitter for real-time updates."""

import asyncio
from typing import Callable, List, Dict, Any, Optional
from queue import Queue, Empty
import threading


class EventEmitter:
    """Thread-safe event emitter for system events."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        # Use a thread-safe queue
        self.event_queue = Queue(maxsize=100)
        self._lock = threading.Lock()
        
    def on(self, event_name: str, callback: Callable):
        """Subscribe to an event."""
        with self._lock:
            if event_name not in self.subscribers:
                self.subscribers[event_name] = []
            self.subscribers[event_name].append(callback)
    
    def off(self, event_name: str, callback: Callable):
        """Unsubscribe from an event."""
        with self._lock:
            if event_name in self.subscribers and callback in self.subscribers[event_name]:
                self.subscribers[event_name].remove(callback)
    
    async def emit(self, event_name: str, data: Any = None):
        """Emit an event (async)."""
        event = {
            "type": event_name,
            "data": data
        }
        
        # Put event in queue for async subscribers
        try:
            self.event_queue.put_nowait(event)
        except Exception:
            # Queue full, skip
            pass
        
        # Call sync subscribers
        with self._lock:
            callbacks = self.subscribers.get(event_name, [])
        
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception:
                # Ignore callback errors
                pass
    
    def get_event(self) -> Optional[Dict]:
        """Get next event from queue (non-blocking)."""
        try:
            return self.event_queue.get_nowait()
        except Empty:
            return None


