# 🛰️ Robotics & Embedded Systems Integration Engineer — Technical Interview Hub (40 Q&A + 8 Labs)

> 🔗 **GitHub Repository:** [embedded-robotic-learning-labs](https://github.com/RollingTL/embedded-robotic-learning-labs)  
> 📁 **Local Path:** `/Users/oleksiizozulenko/sandbox/github/embedded-robotic-learning-labs`  
> 🎯 **Target Notion Page:** [Robotics-40 (ozozulenko)](https://app.notion.com/p/ozozulenko/Robotics-40-3f34fc4e47ce81359b90c6cc32e1a361?source=copy_link)  
> 💻 **Environment:** MacBook M3 Max | Docker | Python 3.12 | C++17 | ROS 2 | ESP32 Emulators | Linux VM

---

## 📋 Таблиця прогресу курсу

| Модуль | Тема | 5 Q&A | Практичний стенд | Статус |
| :--- | :--- | :---: | :--- | :---: |
| **Модуль 1** | Архітектура НРК & Hardware Split | ✅ 5/5 | Емулятори IMU/LiDAR & Telemetry Logger | 🟢 Готово |
| **Модуль 2** | Embedded Linux & System Diagnostics | ✅ 5/5 | Systemd service, логування, crash tests | 🟢 Готово |
| **Модуль 3** | Networking & Latency / Jitter | ✅ 5/5 | **Lab 01: UDP Telemetry Analyzer** | 🟢 Готово |
| **Модуль 4** | ROS 2 Architecture, DDS & QoS | ✅ 5/5 | Pub/Sub, QoS профілі, rosbag2 | 🟢 Готово |
| **Модуль 5** | MAVLink Protocol & Autopilot Stacks | ✅ 5/5 | MAVLink Heartbeat Inspector | 🟢 Готово |
| **Модуль 6** | LiDAR, IMU & Sensor Fusion | ✅ 5/5 | Синтетичні вимірювання, EKF, похибки | 🟢 Готово |
| **Модуль 7** | C++ / Python Concurrency & Backpressure | ✅ 5/5 | **Lab 07: Bounded Telemetry Queue** | 🟢 Готово |
| **Модуль 8** | Integration Testing & Fault Injection | ✅ 5/5 | Docker Compose, fault injection, Watchdog | 🟢 Готово |

---

## 📚 БЛОК 1: 8 МОДУЛІВ ПРОГРАМИ (ЛЕКЦІЇ, ПОСИЛАННЯ ТА 40 ПИТАНЬ)

---

### 🔹 Модуль 1. Архітектура НРК

#### 📖 Мінілекція
Наземні робототехнічні комплекси (НРК) та автономні мобільні роботи (AMR) проєктуються за принципом чіткого дворівневого розподілу обов'язків:
1. **Low-level (Hard Real-Time):** Мікроконтролер або автопілот (STM32, ESP32, Pixhawk/NuttX). Виконує задачі стабілізації (400–1000 Гц), читання високошвидкісних IMU, опитування енкодерів, генерацію сигналів на приводи (PWM/CAN/DShot) та роботу апаратного Watchdog. Будь-яка затримка у декілька мілісекунд призводить до аварії платформи.
2. **High-level (Soft Real-Time / Non-Real-Time):** Companion Computer (NVIDIA Jetson, Intel NUC, Raspberry Pi). Виконує ресурсомісткі задачі: SLAM (одночасна локалізація та картографування), фільтрацію 3D Point Cloud від LiDAR, розпізнавання об'єктів (AI/Computer Vision), планування траєкторій (Global/Local Planners у Nav2) та передачу телеметрії оператору.

#### 🔗 Корисні посилання
- [PX4 Companion Computer Architecture](https://docs.px4.io/main/en/companion_computer/pixhawk_companion.html)
- [ArduPilot Companion Computers Overview](https://ardupilot.org/dev/docs/companion-computers.html)
- [CAN in Automation (CiA) Specifications](https://www.can-cia.org/can-knowledge/)

#### 💬 Відповіді на 5 питань модуля
1. **Що таке companion computer і чим відрізняється від controller?**  
   *Companion Computer* — високорівневий комп'ютер на базі Linux/ROS 2 для важких алгоритмів (Vision, SLAM, AI). *Controller (MCU)* — мікроконтролер для жорсткого реального часу (стабілізація, PID-регулятори, керування двигунами).
2. **Як виглядає архітектура мобільного робота?**  
   Високопотокові сенсори (LiDAR, камери) підключаються до Companion Computer (Ethernet/USB 3.0). Сенсори стабілізації (IMU, енкодери коліс) підключаються до MCU (SPI/CAN). Зв'язок між CC та MCU здійснюється через UART/CAN (протоколи MAVLink, Micro-XRCE-DDS).
3. **Чим відрізняються UART, CAN, SPI, I²C, Ethernet?**  
   - *UART:* асинхронний Point-to-Point, 2 дроти (до 3–6 Мбіт/с, до 2–5 м).  
   - *CAN:* надійна диференційна шина з пріоритезацією арбітражу за ID повідомлення (до 1–8 Мбіт/с, до 40 м).  
   - *SPI:* синхронний швидкісний інтерфейс Master-Slave на одній платі (10–100+ Мбіт/с).  
   - *I²C:* 2-провідна шина з адресацією для низькошвидкісних сенсорів (до 400 кбіт/с – 3.4 Мбіт/с).  
   - *Ethernet:* мережевий інтерфейс високої пропускної здатності (100 Мбіт/с – 10 Гбіт/с) для LiDAR та відеопотоків.
4. **Як запускається embedded Linux?**  
   `ROM Code (BootROM)` $\rightarrow$ `First Stage Bootloader` $\rightarrow$ `U-Boot` (ініціалізація DRAM, завантаження DTB та ядра) $\rightarrow$ `Linux Kernel` (ініціалізація драйверів і VFS) $\rightarrow$ `User Space init (systemd, PID=1)`.
5. **Як забезпечити модульність при заміні hardware?**  
   Використанням Hardware Abstraction Layer (HAL), стандартизованих повідомлень ROS 2 (`sensor_msgs`, `geometry_msgs`), динамічного завантаження плагінів (`pluginlib`) та конфігураційних YAML-файлів.

---

### 🔹 Модуль 2. Embedded Linux

#### 📖 Мінілекція
Linux на Companion Computer вимагає глибокого розуміння підсистеми ядра та діагностики. Опис периферії винесено у **Device Tree (.dts/.dtb)**, що дозволяє одному ядру працювати на різних платах. Демони робота керуються **systemd** юнітами з політиками відновлення (`Restart=always`). Для діагностики зависань використовуються `htop`, системний трасувальник `strace`, налагоджувач `gdb` та інспекція відкритих дескрипторів `lsof`.

#### 🔗 Корисні посилання
- [Linux Device Tree Architecture (kernel.org)](https://www.kernel.org/doc/Documentation/devicetree/usage-model.txt)
- [systemd.service Documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
- [Linux Performance & Tracing Tools by Brendan Gregg](https://www.brendangregg.com/linuxperf.html)

#### 💬 Відповіді на 5 питань модуля
1. **Що таке Device Tree?**  
   Деревоподібна структура даних, що описує залізо (адреси регістрів, GPIO, переривання IRQ, шини I2C/SPI), відокремлюючи конфігурацію плати від скомпільованого ядра Linux.
2. **Як знайти USB-UART адаптер?**  
   Командами `lsusb`, `dmesg | grep -i tty`, перевіркою вузлів `/dev/ttyUSB*` або `/dev/ttyACM*`. Для постійного фіксованого імені створюють **udev rules** (`/etc/udev/rules.d/`).
3. **Як працюють systemd service і restart policy?**  
   Юніт-файл задає команду запуску `ExecStart`, права та правила перезапуску: `Restart=always` або `Restart=on-failure`, та затримку `RestartSec=3s`.
4. **Чим відрізняються process і thread?**  
   *Process* має власний ізольований віртуальний простір пам'яті. *Thread* ділить спільну пам'ять (Heap, глобальні змінні) всередині процесу, маючи власний стек (Stack).
5. **Як діагностувати зависання застосунку?**  
   - `top`/`htop` — оцінка навантаження CPU та витоків пам'яті RAM.  
   - `gdb -p <PID>` з командою `thread apply all bt` — перевірка місця блокування потоків (deadlock/mutex).  
   - `strace -p <PID>` — аналіз системних викликів ядра (очікування read/select/futex).

---

### 🔹 Модуль 3. Networking

#### 📖 Мінілекція
Бездротовий зв'язок мобільного робота характеризується 4 ключовими метриками: **Latency** (затримка), **Jitter** (дисперсія затримки), **Packet Loss** (втрата пакетів) та **Bandwidth** (пропускна здатність). Для швидкісних сенсорів та телеметрії обирають UDP через відсутність затримок повторної відправки (Head-of-Line blocking). Безпечне тунелювання через мобільні мережі реалізується на базі WireGuard VPN.

#### 🔗 Корисні посилання
- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)
- [WireGuard VPN Technical Paper](https://www.wireguard.com/papers/wireguard.pdf)
- [IETF RFC 768: User Datagram Protocol](https://datatracker.ietf.org/doc/html/rfc768)

#### 💬 Відповіді на 5 питань модуля
1. **Switch vs router?**  
   *Switch (L2)* комутує кадри всередині локальної мережі за MAC-адресами. *Router (L3)* маршрутизує пакети між різними мережами за IP-адресами.
2. **TCP vs UDP?**  
   *TCP* встановлює сесію, гарантує порядок та доставку пакетів (ACK), але створює затримки. *UDP* надсилає датаграми без гарантії доставки з мінімальним оверхедом і затримкою.
3. **NAT, DHCP, subnet mask?**  
   *DHCP* автоматично конфігурує IP/шлюз. *Subnet mask* розділяє мережевий та вузловий сегменти IP. *NAT* транслює внутрішні IP робота в одну зовнішню адресу.
4. **VPN vs фізичний канал?**  
   Фізичний канал забезпечує мінімальну затримку, але обмежений радіусом дії. VPN (WireGuard) створює зашифрований тунель поверх будь-якого інтернету (LTE/Starlink).
5. **Latency, jitter, packet loss, bandwidth?**  
   *Latency* — час проходження пакета. *Jitter* — коливання часу затримки між пакетами. *Packet loss* — відсоток втрачених пакетів. *Bandwidth* — пропускна смуга каналу.

---

### 🔹 Модуль 4. ROS 2

#### 📖 Мінілекція
ROS 2 побудований на розподіленому протоколі **DDS (Data Distribution Service)** без центрального вузла `roscore`. Комунікація спирається на три патерни:
- **Topics (Pub/Sub):** односпрямований неперервний потік даних (телеметрія, хмари точок LiDAR).
- **Services (Req/Res):** синхронний короткий виклик (зміна параметра, тригер калібрування).
- **Actions (Goal/Feedback/Result):** тривалі асинхронні задачі з контролем виконання (навігація в точку).
- **QoS:** гнучке налаштування надійності (`Reliable` vs `Best Effort`) та збереження (`Volatile` vs `Transient Local`).

#### 🔗 Корисні посилання
- [ROS 2 Official Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 QoS Policies Deep Dive](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [REP 105: Coordinate Frames for Mobile Robots](https://www.ros.org/reps/rep-0105.html)

#### 💬 Відповіді на 5 питань модуля
1. **Node, topic, publisher/subscriber?**  
   *Node* — обчислювальний процес. *Topic* — пойменована шина повідомлень. *Publisher* відправляє повідомлення, *Subscriber* підписується на них.
2. **Services vs actions?**  
   *Service* блокує клієнта до отримання швидкої відповіді. *Action* виконує довгу операцію, дозволяє надсилати проміжний статус (Feedback) та скасовувати задачу.
3. **DDS і QoS?**  
   DDS — стандарт децентралізованого обміну даними (P2P Discovery). QoS задає правила доставки даних (надійність, глибина черги, довговічність).
4. **Навіщо timestamps і frame_id?**  
   `stamp` потрібен для часової синхронізації вимірювань у фільтрах (EKF). `frame_id` вказує локальну систему координат сенсора (`laser_link`, `base_link`, `map`) для дерева трансформацій TF2.
5. **Як діагностувати відсутні ROS 2 повідомлення?**  
   Утилітами `ros2 topic list`, `ros2 topic hz`, `ros2 topic echo`, перевіркою несумісності QoS (`ros2 topic info --verbose`) та перевіркою `ROS_DOMAIN_ID`.

---

### 🔹 Модуль 5. MAVLink, PX4, ArduPilot

#### 📖 Мінілекція
**MAVLink** — компактний бінарний протокол зв'язку для дронів та роботів. Заголовок становить лише 8–14 байт з перевіркою CRC. Кожен борт має **System ID**, а кожен модуль всередині нього — **Component ID**. Пакет **HEARTBEAT** передається щосекунди: його втрата на 2–3 секунди сигналізує про втрату зв'язку та активує режим безпеки (**Failsafe**).

#### 🔗 Корисні посилання
- [MAVLink Protocol Guide](https://mavlink.io/en/)
- [PX4 Autopilot User Guide](https://docs.px4.io/)
- [ArduRover Control Modes Guide](https://ardupilot.org/rover/docs/rover-control-modes.html)

#### 💬 Відповіді на 5 питань модуля
1. **Що таке MAVLink?**  
   Бінарний протокол з серіалізацією структурованих повідомлень для низькошвидкісних радіоканалів і послідовних портів.
2. **Що таке system ID/component ID?**  
   *System ID* — адреса конкретного робота/борту. *Component ID* — адреса підсистеми всередині робота (1: Автопілот, 194: Companion Computer).
3. **Навіщо HEARTBEAT?**  
   Повідомляє про працездатність вузла, тип машини та активний статус автопілота. При зникненні спрацьовує аварійний алгоритм (Failsafe RTH/Stop).
4. **PX4 vs ArduPilot/ArduRover?**  
   *PX4* побудований на модульній POSIX/uORB архітектурі, орієнтованій на сучасні академічні та комерційні розробки. *ArduPilot* має величезну підтримку різноманітного заліза та дорослі алгоритми для наземних платформ (ArduRover).
5. **Концептуальні відмінності Manual, Guided, Auto, Hold?**  
   - *Manual:* пряме ручне керування оператором.  
   - *Guided:* рух до заданих координат/швидкості за командами з Companion Computer.  
   - *Auto:* автономне проходження місії за точками маршруту (waypoints).  
   - *Hold:* повна зупинка та утримання поточної позиції.

---

### 🔹 Модуль 6. LiDAR, IMU & Sensor Fusion

#### 📖 Мінілекція
- **IMU:** акселерометр вимірює вектор гравітації та прискорення; гіроскоп — кутову швидкість. Орієнтація описується кватерніонами ($w, x, y, z$) для уникнення Gimbal Lock.
- **LiDAR:** вимірює затримку відбиття лазерних імпульсів (Time-of-Flight), генеруючи хмару точок 3D Point Cloud.
- **Sensor Fusion:** Розширений фільтр Калмана (**EKF**) об'єднує високочастотний зашумлений дрейф IMU з точними, але низькочастотними даними LiDAR/одометрії/GPS.

#### 🔗 Корисні посилання
- [Point Cloud Library (PCL)](https://pointclouds.org/)
- [An Introduction to the Kalman Filter (UNC)](https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf)
- [REP 103: Standard Units of Measure and Coordinate Conventions](https://www.ros.org/reps/rep-0103.html)

#### 💬 Відповіді на 5 питань модуля
1. **LiDAR і point cloud?**  
   LiDAR сканує простір лазером. Point Cloud — це масив тривимірних координат $(X, Y, Z)$ з відбивною інтенсивністю $I$ та часовою міткою.
2. **Accelerometer vs gyroscope?**  
   Акселерометр вимірює лінійне прискорення та вектор $g$ (не дрейфує, але чутливий до вібрацій). Гіроскоп вимірює кутову швидкість (точний у динаміці, але накопичує дрейф при інтегруванні).
3. **Roll, pitch, yaw, quaternion?**  
   Кути Ейлера інтуїтивні, але мають сингулярність (Gimbal Lock при Pitch = 90°). Кватерніон ($w, x, y, z$) позбавлений сингулярностей та ефективний для обчислень.
4. **Навіщо калібрування й синхронізація?**  
   Калібрування компенсує нульовий зсув (bias) та температурний дрейф. Синхронізація (апаратний тригер / PTP / ROS stamp) гарантує узгодженість вимірювань у часі.
5. **Sensor fusion і Kalman filter?**  
   Математичний алгоритм оцінки стану, що оптимально мінімізує дисперсію похибок на основі коваріаційних матриць шумів датчиків.

---

### 🔹 Модуль 7. C++ / Python Concurrency & Backpressure

#### 📖 Мінілекція
У високонавантажених системах телеметрії Producer генерує дані швидше, ніж Consumer може їх обробити. Це призводить до переповнення пам'яті (OOM). Рішення — **Bounded Queues** та політика **Backpressure**:
- `DROP_OLDEST` — витіснення застарілих кадрів (ідеально для свіжої телеметрії).
- Безпека пам'яті в C++ досягається за допомогою **RAII**, розумних вказівників `std::unique_ptr`, `std::shared_ptr` та м'ютексів `std::unique_lock`.

#### 🔗 Корисні посилання
- [C++ Reference Concurrency Support](https://en.cppreference.com/w/cpp/thread)
- [C++ Core Guidelines (RAII & Memory)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Python asyncio Official Documentation](https://docs.python.org/3/library/asyncio.html)

#### 💬 Відповіді на 5 питань модуля
1. **Thread, mutex, message queue?**  
   *Thread* — потік виконання. *Mutex* — примітив взаємного блокування для захисту пам'яті. *Message queue* — потокобезпечна черга передачі даних між потоками.
2. **Race condition і deadlock?**  
   *Race condition:* результат залежить від випадкового порядку виконання потоків без синхронізації. *Deadlock:* взаємне блокування потоків, що очікують на ресурси один одного.
3. **asyncio і неблокувальний I/O?**  
   Асинхронний Event Loop в одному потоці, що перемикає задачі під час очікування операцій вводу-виводу без витрат на системні перемикання контексту ядра.
4. **RAII та smart pointers?**  
   RAII зв'язує життєвий цикл ресурсу з часом життя об'єкта у стеку. `std::unique_ptr` гарантує монопольне володіння та автоматичне звільнення пам'яті без `delete`.
5. **Backpressure і bounded queue?**  
   Обмеження максимального розміру буфера та визначення поведінки при переповненні (скидання старих даних або сповільнення відправника) для захисту від OOM.

---

### 🔹 Модуль 8. Testing та Інтеграція

#### 📖 Мінілекція
Піраміда тестування робототехніки:
1. **Unit tests:** ізольована перевірка парсерів повідомлень та алгоритмів.
2. **Integration tests:** перевірка взаємодії декількох нод у Docker Compose.
3. **HIL (Hardware-in-the-Loop):** тестування реального заліза автопілота з фізичними генераторами сигналів/сенсорів.
4. **Fault Injection:** емуляція обриву ліній зв'язку, шумів та втрати живлення для перевірки спрацювання захисних таймерів (**Watchdog**).

#### 🔗 Корисні посилання
- [GoogleTest User's Guide](https://google.github.io/googletest/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Principles of Chaos Engineering](https://principlesofchaos.org/)

#### 💬 Відповіді на 5 питань модуля
1. **Unit/integration/system/HIL tests?**  
   - *Unit:* окремі функції/класи.  
   - *Integration:* взаємодія 2+ компонентів.  
   - *System:* весь стек на стенді.  
   - *HIL:* реальний контролер у замкненому контурі з симулятором середовища.
2. **Як тестувати втрату з'єднання?**  
   Програмними ін'єкціями збоїв (`tc qdisc` в Linux, симуляторами дропів пакетів у коді, розривом віртуального мережевого моста в Docker).
3. **Watchdog, health check, heartbeat?**  
   *Watchdog* — апаратний/програмний таймер скидання системи при зависанні. *Health check* — опитування стану внутрішніх підсистем. *Heartbeat* — регулярний маяк присутності у мережі.
4. **Як організувати observability?**  
   Структуроване логування (`spdlog`/`rclcpp`), збір числових метрик (Prometheus/OpenTelemetry), візуалізація дашбордів (Grafana).
5. **Як інтегрувати незнайоме обладнання?**  
   1) Аналіз документації та протоколу. 2) Запис сирих логів комунікації. 3) Створення ізольованого драйвера з unit-тестами. 4) Інтеграція в ROS 2 з HIL-верифікацією на стенді.

---

## 🔬 БЛОК 2: ТЕМАТИЧНІ DEEP DIVES (РОЗШИРЕНІ ПИТАННЯ СЕСІЇ)

### 📌 1. Що таке IMU?
- **Склад:** 3-осьовий акселерометр ($a_x, a_y, a_z$), 3-осьовий гіроскоп ($\omega_x, \omega_y, \omega_z$), опціонально 3-осьовий магнітометр ($m_x, m_y, m_z$).
- **Фізика MEMS:** мікроелектромеханічні кремнієві датчики (ICM-42688, BMI088).
- **Дрейф проти шуму:** Гіроскоп не має шуму вібрацій, але інтегрує похибку і **дрейфує з часом**. Акселерометр не дрейфує, але **чутливий до механічних вібрацій**.
- **Sensor Fusion:** Комплементарний фільтр, алгоритм Madgwick, або EKF об'єднують їх у фінальну оцінку орієнтації.
- **Тип у ROS 2:** `sensor_msgs/msg/Imu` (містить кватерніон орієнтації, кутові швидкості та лінійні прискорення з матрицями коваріацій $3 \times 3$).

### 📌 2. Що таке NVIDIA Jetson?
- **Архітектура:** ARM CPU + повноцінний CUDA GPU (Ampere/Orin) + Tensor Cores + Unified Memory (UMA — спільна пам'ять без PCIe копіювання).
- **Лінійка:**
  - *Orin Nano:* до 40 TOPS (7–15W) — малі дрони та роботи.
  - *Orin NX:* до 100 TOPS (10–25W) — мобільні платформи, Visual SLAM.
  - *AGX Orin:* до 275 TOPS (15–75W) — безпілотний транспорт, важкі НРК.
- **Екосистема:** NVIDIA Isaac ROS (прискорення нод на GPU), TensorRT (інференс YOLO за 2–4 мс).

### 📌 3. Що таке Intel NUC?
- **Архітектура:** Повноцінний настільний **x86-64** процесор Intel Core i5/i7/i9.
- **Переваги:** Максимальна однопоточна продуктивність C++, відсутність мороки з крос-компіляцією під ARM, швидкісні NVMe диски для гігабайтних `rosbag2` записів, наявність 2–4 мережевих карт 2.5G/10G Ethernet для безпосереднього підключення LiDAR.

### 📌 4. Що таке LiDAR та як далеко він бачить?
- **Принцип:** Time-of-Flight (ToF). Імпульс лазера відбивається від об'єкта, сенсор вимірює час $\Delta t$ і розраховує дистанцію $d = \frac{c \cdot \Delta t}{2}$.
- **Дальність:**
  - 2D побутові: 6–25 м.
  - Складські 2D/3D: 30–100 м.
  - Автомобільні 3D: 200–300+ м.
  - Авіаційні/геодезичні: 1–10+ км.
- **Фізика довжини хвилі:**
  - *905 нм:* найпоширеніші, але обмежені за потужністю безпекою ока (Class 1 Eye Safe), тому темні об'єкти (10% відбиття) бачать лише на 50–80 м.
  - *1550 нм:* поглинаються рогівкою ока і не шкодять сітківці, тому лазер може бути у 100 разів потужнішим і бачить темні об'єкти на 250–400 м.

### 📌 5. Що таке POSIX-подібна архітектура?
- **Стандарт IEEE 1003:** «Все є файлом» (датчики відкриваються через `open("/dev/sensor")`), модель потоків `pthread`, системні виклики `read`, `write`, `ioctl`.
- **Застосування:** PX4 на базі NuttX RTOS. Дозволяє запускати той самий код як на контролері STM32, так і в симуляції **SITL (Software In The Loop)** на macOS/Linux без модифікацій.

### 📌 6. Extended Kalman Filter (EKF) та ряд Тейлора
- **Чому Extended?** Класичний фільтр Калмана працює виключно з лінійними функціями. Рух робота описується нелінійною тригонометрією ($\sin\theta, \cos\theta$).
- **Роль ряду Тейлора:** Наближення нелінійної кривої дотичною прямою лінією в поточній точці:  
  $$f(x) \approx f(x_0) + f'(x_0)(x - x_0)$$  
  Похідні утворюють **матрицю Якобі (Jacobian)**, що дозволяє застосовувати матричний апарат Калмана.
- **Цикл:** `Predict` (прогноз стану моделлю та IMU) $\rightarrow$ `Update` (корекція вимірюваннями GPS/одометрії за коефіцієнтом Kalman Gain $K$).

### 📌 7. Процес проти Потоку (Process vs Thread)
- **Аналогія:** Процес — окремий автономний завод зі своїм парканом; Потік — робітник всередині заводу.
- **Пам'ять:** Процеси мають ізольований віртуальний простір адрес (MMU захист). Потоки ділять спільну динамічну пам'ять Heap, маючи власні стеки.
- **Наслідки крашу:** Падіння одного процесу ізольоване. Падіння одного потоку (SegFault) **вбиває весь процес**.
- **В робототехніці:** Окремі ноди гарантують надійність; композитні ноди в спільних потоках (ROS 2 Component Nodes) дають **Zero-Copy передачу даних**.

---

## 🛠️ БЛОК 3: ПРАКТИЧНІ ЛАБОРАТОРНІ РОБОТИ ТА ТЕСТИ

### 🧪 Лабораторна №1: UDP Telemetry Analyzer (`lab01_udp_telemetry`)
- **`sender.py`:** Відправляє кожні 100 мс на `127.0.0.1:9000` JSON з полями `seq`, `timestamp`, `temperature`, `battery_voltage`. Підтримує ін'єкцію штучних збоїв: `--drop-rate 0.10`, `--jitter 0.05`, `--reorder 0.05`.
- **`receiver.py`:** Фіксує розриви номерів (`GAP_DETECTED`), вимірює затримку (latency), джиттер (std dev інтервалів прибуття) та генерує тривогу `SILENCE DETECTED`, якщо пакети відсутні понад 2 секунди.
- **`test_udp_telemetry.py`:** 5 unit-тестів (послідовність, виявлення втрат, out-of-order, розрахунок latency, таймаут тиші).

#### Результати тестового прогону:
```text
==================================================
          TELEMETRY ANALYSIS SUMMARY          
==================================================
  total_received        : 15
  total_dropped         : 3
  total_out_of_order    : 0
  loss_percentage       : 16.67 %
  avg_latency_ms        : 0.30 ms
  min_latency_ms        : 0.15 ms
  max_latency_ms        : 0.73 ms
  jitter_ms             : 23.35 ms
==================================================
```

### 🧪 Лабораторна №7: Thread-Safe Bounded Queue (`lab07_bounded_queue`)
- **`bounded_queue.py`:** Потокобезпечна черга фіксованого розміру з підтримкою трьох політик витіснення:
  - `DROP_OLDEST` — видаляє найстаріше повідомлення (гарантує свіжість телеметрії).
  - `DROP_NEWEST` — відхиляє нове повідомлення.
  - `BLOCK` — призупиняє Producer до звільнення місця.
- **`test_bounded_queue.py`:** Багатопотокові тести конкурентного доступу Producer/Consumer.

---

## 🚀 Як вивантажити локальний репозиторій на GitHub

Усі файли вже заініціалізовано, закомічено та оформлено:
```bash
cd /Users/oleksiizozulenko/sandbox/github/embedded-robotic-learning-labs

# 1. Створіть порожній репозиторій на GitHub: embedded-robotic-learning-labs
# 2. Підключіть remote та зробіть push:
git remote add origin git@github.com:RollingTL/embedded-robotic-learning-labs.git
git push -u origin main
```
