#!/usr/bin/env python3
"""
Thread-safe Bounded Telemetry Queue with Backpressure Handling (Lab 07)
Supports drop-oldest, drop-newest, and blocking strategies when queue is full.
Includes metrics tracking (pushed, dropped, consumed, current_size, high_watermark).
"""

import threading
import queue
import time
from typing import Any, Optional, Dict
from enum import Enum

class OverflowPolicy(Enum):
    DROP_OLDEST = 1  # Evict oldest item (typical for telemetry where freshness matters)
    DROP_NEWEST = 2  # Reject incoming new item
    BLOCK = 3        # Block producer until space opens up

class BoundedTelemetryQueue:
    def __init__(self, maxsize: int = 100, policy: OverflowPolicy = OverflowPolicy.DROP_OLDEST):
        self.maxsize = maxsize
        self.policy = policy
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
        
        self._storage = []
        
        # Metrics
        self.total_pushed = 0
        self.total_dropped = 0
        self.total_consumed = 0
        self.high_watermark = 0

    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """Pushes an item into the queue. Applies configured OverflowPolicy if full."""
        with self._lock:
            if len(self._storage) >= self.maxsize:
                if self.policy == OverflowPolicy.DROP_OLDEST:
                    dropped_item = self._storage.pop(0)
                    self.total_dropped += 1
                    # Space opened up
                elif self.policy == OverflowPolicy.DROP_NEWEST:
                    self.total_dropped += 1
                    return False
                elif self.policy == OverflowPolicy.BLOCK:
                    end_time = time.time() + timeout if timeout else None
                    while len(self._storage) >= self.maxsize:
                        if timeout is not None:
                            remaining = end_time - time.time()
                            if remaining <= 0:
                                self.total_dropped += 1
                                return False
                            self._not_full.wait(remaining)
                        else:
                            self._not_full.wait()

            self._storage.append(item)
            self.total_pushed += 1
            cur_len = len(self._storage)
            if cur_len > self.high_watermark:
                self.high_watermark = cur_len

            self._not_empty.notify()
            return True

    def get(self, timeout: Optional[float] = None) -> Any:
        """Retrieves and removes an item from the queue."""
        with self._lock:
            end_time = time.time() + timeout if timeout else None
            while len(self._storage) == 0:
                if timeout is not None:
                    remaining = end_time - time.time()
                    if remaining <= 0:
                        raise queue.Empty
                    self._not_empty.wait(remaining)
                else:
                    self._not_empty.wait()

            item = self._storage.pop(0)
            self.total_consumed += 1
            self._not_full.notify()
            return item

    def qsize(self) -> int:
        with self._lock:
            return len(self._storage)

    def get_metrics(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "current_size": len(self._storage),
                "maxsize": self.maxsize,
                "high_watermark": self.high_watermark,
                "total_pushed": self.total_pushed,
                "total_dropped": self.total_dropped,
                "total_consumed": self.total_consumed,
                "policy": self.policy.name
            }
