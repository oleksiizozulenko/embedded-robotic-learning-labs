#!/usr/bin/env python3
"""
UDP Telemetry Sender Module
Simulates an embedded sensor/node sending periodic telemetry data over UDP.
Includes fault injection options: packet loss, latency/jitter, out-of-order delivery.
"""

import socket
import time
import json
import random
import argparse
import sys

def run_sender(host: str = "127.0.0.1", port: int = 9000, interval: float = 0.1,
               drop_rate: float = 0.10, jitter_max: float = 0.0, reorder_rate: float = 0.0,
               count: int = 0):
    """
    Sends UDP telemetry frames to target host:port.
    
    :param host: Receiver IP address
    :param port: Receiver port
    :param interval: Send interval in seconds (default 100ms)
    :param drop_rate: Probability [0.0 - 1.0] of intentionally dropping a packet
    :param jitter_max: Max artificial delay (seconds) before sending
    :param reorder_rate: Probability [0.0 - 1.0] of swapping packet order
    :param count: Total packets to send (0 = infinite)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seq = 0
    pending_reorder_pkt = None

    print(f"[SENDER] Starting UDP Telemetry Sender -> {host}:{port}")
    print(f"[SENDER] Interval: {interval*1000:.0f}ms | Drop rate: {drop_rate*100:.1f}% | Jitter max: {jitter_max*1000:.0f}ms")

    try:
        while True:
            seq += 1
            now = time.time()
            # Synthetic sensors
            temp = round(20.0 + random.uniform(-1.5, 2.5), 2)
            battery_v = round(12.4 - (seq * 0.0001), 2)

            payload = {
                "seq": seq,
                "timestamp": now,
                "temperature": temp,
                "battery_voltage": battery_v,
                "node_id": "sensor_esp32_01"
            }

            data = json.dumps(payload).encode('utf-8')

            # Packet loss simulation
            if random.random() < drop_rate:
                print(f"[SENDER] [DROPPED] Simulated packet loss for seq={seq}")
            else:
                # Jitter simulation
                if jitter_max > 0:
                    time.sleep(random.uniform(0, jitter_max))

                # Reordering simulation
                if random.random() < reorder_rate and pending_reorder_pkt is None:
                    pending_reorder_pkt = data
                    print(f"[SENDER] [REORDER] Holding back seq={seq} to deliver out-of-order")
                else:
                    sock.sendto(data, (host, port))
                    print(f"[SENDER] Sent seq={seq} | Temp={temp}°C | Bytes={len(data)}")

                    if pending_reorder_pkt:
                        sock.sendto(pending_reorder_pkt, (host, port))
                        print(f"[SENDER] [REORDER] Sent delayed packet out-of-order")
                        pending_reorder_pkt = None

            if count > 0 and seq >= count:
                break

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[SENDER] Stopped by user.")
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Telemetry Sender")
    parser.add_argument("--host", default="127.0.0.1", help="Target IP")
    parser.add_argument("--port", type=int, default=9000, help="Target Port")
    parser.add_argument("--interval", type=float, default=0.1, help="Interval in seconds")
    parser.add_argument("--drop-rate", type=float, default=0.10, help="Packet drop rate (0.0 - 1.0)")
    parser.add_argument("--jitter", type=float, default=0.0, help="Max random jitter in seconds")
    parser.add_argument("--reorder", type=float, default=0.0, help="Out-of-order rate (0.0 - 1.0)")
    parser.add_argument("--count", type=int, default=0, help="Number of packets to send (0 = infinite)")
    args = parser.parse_args()

    run_sender(
        host=args.host,
        port=args.port,
        interval=args.interval,
        drop_rate=args.drop_rate,
        jitter_max=args.jitter,
        reorder_rate=args.reorder,
        count=args.count
    )
