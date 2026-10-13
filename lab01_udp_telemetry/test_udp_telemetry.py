#!/usr/bin/env python3
"""
Unit tests for TelemetryAnalyzer (Lab 01 - UDP Telemetry)
"""

import unittest
import time
import json
from receiver import TelemetryAnalyzer

class TestTelemetryAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TelemetryAnalyzer(silence_threshold=2.0)

    def _make_packet(self, seq: int, ts_offset: float = 0.0) -> bytes:
        payload = {
            "seq": seq,
            "timestamp": time.time() - ts_offset,
            "temperature": 22.5,
            "battery_voltage": 12.1,
            "node_id": "test_node"
        }
        return json.dumps(payload).encode('utf-8')

    def test_in_sequence_packets(self):
        t0 = time.time()
        res1 = self.analyzer.process_packet(self._make_packet(1), t0)
        res2 = self.analyzer.process_packet(self._make_packet(2), t0 + 0.1)
        res3 = self.analyzer.process_packet(self._make_packet(3), t0 + 0.2)

        self.assertEqual(res1["status"], "OK")
        self.assertEqual(res2["status"], "OK")
        self.assertEqual(res3["status"], "OK")
        self.assertEqual(self.analyzer.total_received, 3)
        self.assertEqual(self.analyzer.total_dropped, 0)

    def test_sequence_gap_detection(self):
        t0 = time.time()
        self.analyzer.process_packet(self._make_packet(1), t0)
        # Skip seq 2 & 3, receive seq 4 directly
        res = self.analyzer.process_packet(self._make_packet(4), t0 + 0.3)

        self.assertIn("GAP_DETECTED", res["status"])
        self.assertEqual(res["dropped_gap"], 2)
        self.assertEqual(self.analyzer.total_dropped, 2)
        self.assertEqual(self.analyzer.total_received, 2)

    def test_out_of_order_detection(self):
        t0 = time.time()
        self.analyzer.process_packet(self._make_packet(1), t0)
        self.analyzer.process_packet(self._make_packet(3), t0 + 0.2)
        # Late arrival of seq 2
        res = self.analyzer.process_packet(self._make_packet(2), t0 + 0.25)

        self.assertEqual(res["status"], "OUT_OF_ORDER")
        self.assertEqual(self.analyzer.total_out_of_order, 1)

    def test_latency_calculation(self):
        t_rx = time.time()
        # Packet generated 0.05 seconds (50ms) ago
        pkt = self._make_packet(seq=1, ts_offset=0.05)
        res = self.analyzer.process_packet(pkt, t_rx)

        self.assertAlmostEqual(res["latency_ms"], 50.0, delta=5.0)

    def test_silence_detection(self):
        t0 = time.time()
        self.analyzer.process_packet(self._make_packet(1), t0)

        # 1.5 seconds later -> no silence alert
        self.assertIsNone(self.analyzer.check_silence(t0 + 1.5))

        # 2.5 seconds later -> silence alert
        silence_dur = self.analyzer.check_silence(t0 + 2.5)
        self.assertIsNotNone(silence_dur)
        self.assertAlmostEqual(silence_dur, 2.5, delta=0.01)

if __name__ == '__main__':
    unittest.main()
