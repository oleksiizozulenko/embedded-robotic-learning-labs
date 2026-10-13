#!/usr/bin/env python3
"""
UDP Telemetry Receiver Module
Receives UDP telemetry frames, analyzes sequence gaps, out-of-order delivery,
measures latency & jitter metrics, and warns on network silence (>2s timeout).
"""

import socket
import time
import json
import argparse
import sys
from typing import Dict, Any, Optional

class TelemetryAnalyzer:
    def __init__(self, silence_threshold: float = 2.0):
        self.silence_threshold = silence_threshold
        self.last_rx_time: Optional[float] = None
        self.expected_seq: Optional[int] = None
        
        # Statistics
        self.total_received = 0
        self.total_dropped = 0
        self.total_out_of_order = 0
        self.latencies = []
        self.inter_arrival_times = []
        self.last_inter_arrival_ts: Optional[float] = None

    def process_packet(self, data_bytes: bytes, rx_timestamp: float) -> Dict[str, Any]:
        """Processes an incoming packet payload and updates telemetry statistics."""
        try:
            payload = json.loads(data_bytes.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            return {"status": "ERROR", "message": f"Malformed payload: {e}"}

        seq = payload.get("seq")
        tx_ts = payload.get("timestamp")

        if seq is None or tx_ts is None:
            return {"status": "ERROR", "message": "Missing seq or timestamp field"}

        # Calculate Latency
        latency_ms = (rx_timestamp - tx_ts) * 1000.0
        self.latencies.append(latency_ms)

        # Calculate Inter-arrival time and Jitter
        inter_arrival_ms = 0.0
        if self.last_inter_arrival_ts is not None:
            inter_arrival_ms = (rx_timestamp - self.last_inter_arrival_ts) * 1000.0
            self.inter_arrival_times.append(inter_arrival_ms)
        self.last_inter_arrival_ts = rx_timestamp

        status_flag = "OK"
        dropped_count = 0

        if self.expected_seq is None:
            # First packet received
            self.expected_seq = seq + 1
        elif seq == self.expected_seq:
            self.expected_seq += 1
        elif seq > self.expected_seq:
            dropped_count = seq - self.expected_seq
            self.total_dropped += dropped_count
            status_flag = f"GAP_DETECTED (lost {dropped_count} pkts)"
            self.expected_seq = seq + 1
        elif seq < self.expected_seq:
            self.total_out_of_order += 1
            status_flag = "OUT_OF_ORDER"

        self.total_received += 1
        self.last_rx_time = rx_timestamp

        return {
            "status": status_flag,
            "seq": seq,
            "dropped_gap": dropped_count,
            "latency_ms": round(latency_ms, 2),
            "inter_arrival_ms": round(inter_arrival_ms, 2),
            "payload": payload
        }

    def check_silence(self, current_time: float) -> Optional[float]:
        """Returns silence duration if last received packet exceeded silence threshold."""
        if self.last_rx_time is None:
            return None
        elapsed = current_time - self.last_rx_time
        if elapsed > self.silence_threshold:
            return elapsed
        return None

    def get_summary(self) -> Dict[str, Any]:
        """Generates comprehensive telemetry summary statistics."""
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        min_latency = min(self.latencies) if self.latencies else 0.0
        max_latency = max(self.latencies) if self.latencies else 0.0

        # Jitter calculation: standard deviation of inter-arrival times
        jitter_ms = 0.0
        if len(self.inter_arrival_times) > 1:
            mean_ia = sum(self.inter_arrival_times) / len(self.inter_arrival_times)
            variance = sum((x - mean_ia) ** 2 for x in self.inter_arrival_times) / (len(self.inter_arrival_times) - 1)
            jitter_ms = variance ** 0.5

        loss_percentage = 0.0
        total_expected = self.total_received + self.total_dropped
        if total_expected > 0:
            loss_percentage = (self.total_dropped / total_expected) * 100.0

        return {
            "total_received": self.total_received,
            "total_dropped": self.total_dropped,
            "total_out_of_order": self.total_out_of_order,
            "loss_percentage": round(loss_percentage, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "min_latency_ms": round(min_latency, 2),
            "max_latency_ms": round(max_latency, 2),
            "jitter_ms": round(jitter_ms, 2)
        }

def run_receiver(host: str = "127.0.0.1", port: int = 9000, silence_timeout: float = 2.0, max_packets: int = 0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.settimeout(0.5)  # Periodic timeout to allow checking silence and clean exit

    analyzer = TelemetryAnalyzer(silence_threshold=silence_timeout)
    print(f"[RECEIVER] Bound to {host}:{port}. Monitoring telemetry stream...")

    last_silence_warn = 0.0

    try:
        while True:
            now = time.time()

            # Check for network silence
            silence_dur = analyzer.check_silence(now)
            if silence_dur and (now - last_silence_warn > 1.0):
                print(f"[RECEIVER] ⚠️ [WARNING] SILENCE DETECTED! No data received for {silence_dur:.2f}s (Threshold: {silence_timeout}s)")
                last_silence_warn = now

            try:
                data, addr = sock.recvfrom(2048)
                rx_ts = time.time()
                res = analyzer.process_packet(data, rx_ts)

                if res.get("status") == "ERROR":
                    print(f"[RECEIVER] ❌ Error: {res.get('message')}")
                else:
                    seq = res["seq"]
                    status = res["status"]
                    lat = res["latency_ms"]
                    temp = res["payload"].get("temperature")
                    tag = f"[{status}]" if status != "OK" else "[OK]"
                    print(f"[RECEIVER] {tag} seq={seq:04d} | Temp={temp}°C | Latency={lat}ms | From {addr[0]}:{addr[1]}")

                if max_packets > 0 and analyzer.total_received >= max_packets:
                    break

            except socket.timeout:
                continue

    except KeyboardInterrupt:
        print("\n[RECEIVER] Stopping receiver.")
    finally:
        sock.close()
        summary = analyzer.get_summary()
        print("\n" + "="*50)
        print("          TELEMETRY ANALYSIS SUMMARY          ")
        print("="*50)
        for k, v in summary.items():
            print(f"  {k:<22}: {v}")
        print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Telemetry Receiver")
    parser.add_argument("--host", default="127.0.0.1", help="Bind IP")
    parser.add_argument("--port", type=int, default=9000, help="Bind Port")
    parser.add_argument("--silence-timeout", type=float, default=2.0, help="Silence warning threshold in seconds")
    parser.add_argument("--max-packets", type=int, default=0, help="Stop after N packets (0 = infinite)")
    args = parser.parse_args()

    run_receiver(host=args.host, port=args.port, silence_timeout=args.silence_timeout, max_packets=args.max_packets)
