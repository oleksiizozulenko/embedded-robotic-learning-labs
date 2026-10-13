#!/usr/bin/env python3
import unittest
import time
import threading
import queue
from bounded_queue import BoundedTelemetryQueue, OverflowPolicy

class TestBoundedTelemetryQueue(unittest.TestCase):
    def test_capacity_and_fifo(self):
        q = BoundedTelemetryQueue(maxsize=3, policy=OverflowPolicy.DROP_NEWEST)
        self.assertTrue(q.put("pkt1"))
        self.assertTrue(q.put("pkt2"))
        self.assertTrue(q.put("pkt3"))
        # 4th item should be rejected under DROP_NEWEST
        self.assertFalse(q.put("pkt4"))

        self.assertEqual(q.get(), "pkt1")
        self.assertEqual(q.get(), "pkt2")
        self.assertEqual(q.get(), "pkt3")

    def test_drop_oldest_policy(self):
        q = BoundedTelemetryQueue(maxsize=2, policy=OverflowPolicy.DROP_OLDEST)
        q.put("pkt1")
        q.put("pkt2")
        # Overwriting pkt1 with pkt3
        q.put("pkt3")

        self.assertEqual(q.qsize(), 2)
        self.assertEqual(q.get(), "pkt2")
        self.assertEqual(q.get(), "pkt3")

        metrics = q.get_metrics()
        self.assertEqual(metrics["total_dropped"], 1)

    def test_concurrent_producer_consumer(self):
        q = BoundedTelemetryQueue(maxsize=10, policy=OverflowPolicy.DROP_OLDEST)
        pushed_count = 100
        received = []

        def producer():
            for i in range(pushed_count):
                q.put(f"item_{i}")
                time.sleep(0.001)

        def consumer():
            for _ in range(pushed_count):
                try:
                    item = q.get(timeout=0.5)
                    received.append(item)
                except queue.Empty:
                    break

        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        metrics = q.get_metrics()
        self.assertEqual(metrics["total_pushed"], pushed_count)
        self.assertGreater(len(received), 0)

if __name__ == "__main__":
    unittest.main()
