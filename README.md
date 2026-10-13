# 🤖 Embedded Robotics & Integration Engineering Learning Labs

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://isocpp.org/)
[![ROS 2](https://img.shields.io/badge/ROS_2-Humble%2FJazzy-green.svg)](https://docs.ros.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://www.docker.com/)

Практичний лабораторний стенд та теоретична програма підготовки з напрямку **Robotics & Embedded Systems Integration Engineer** (НРК).

---

## 📌 Структура репозиторію

- `lab01_udp_telemetry/`: UDP Telemetry sender/receiver з виявленням втрат пакетів, джиттера, latencies та таймерів тиші (>2s).
- `lab02_linux_telemetry_service/`: Systemd service конфігурація, логування та аварійний перезапуск у Linux VM.
- `lab03_docker_network_metrics/`: Docker UDP sender/receiver з вимірюванням втрат та затримок у заізольованих контейнерах.
- `lab04_ros2_pubsub_bag/`: ROS 2 C++/Python ноди, QoS профілі, rosbag2 запис та відтворення.
- `lab05_mavlink_inspector/`: MAVLink inspector для обробки HEARTBEAT та SYS_STATUS повідомлень.
- `lab06_sensor_fusion_sim/`: Генератор синтетичних LiDAR/IMU вимірювань, complementary/Kalman фільтрація, оцінка похибок.
- `lab07_bounded_queue/`: Thread-safe Bounded Telemetry Queue з витісненням застарілих даних (drop-oldest), backpressure та unit-тестами.
- `lab08_docker_fault_injection/`: Docker Compose інтеграційний стенд з автоматичним інпактом мережевих збоїв та watchdog тестуванням.

---

## 🧪 Запуск тестів

### Lab 01 (UDP Telemetry)
```bash
python3 -m unittest discover -s lab01_udp_telemetry -p "test_*.py"
```

### Lab 07 (Bounded Queue)
```bash
python3 -m unittest discover -s lab07_bounded_queue -p "test_*.py"
```
