# 🛡️ WT32-ETH01 Hardware DNS Sinkhole & Tracker Shield

[![ESP32](https://img.shields.io/badge/Platform-ESP32-blue.svg)](https://www.espressif.com/)
[![Ethernet](https://img.shields.io/badge/Ethernet-LAN8720A%20100Mbps-brightgreen.svg)]()
[![PlatformIO](https://img.shields.io/badge/Build-PlatformIO-orange.svg)](https://platformio.org/)
[![DNS Sinkhole](https://img.shields.io/badge/DNS-UDP%20Port%2053-red.svg)]()
[![Web Dashboard](https://img.shields.io/badge/Web%20UI-Cyber%20Dark%20(Port%2080)-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

A dedicated, ultra-low-latency **hardware network-wide ad blocker and telemetry sinkhole** built for the **Wireless-Tag WT32-ETH01** (ESP32 + LAN8720A 100Mbps Ethernet) board. 

Once plugged into any LAN port on your router, it intercepts and sinkholes ad networks, tracker SDKs, and telemetry domains across every device on your network (Android, iPhone/iOS, Windows, Linux, and IoT devices) with **zero browser extensions or client-side software required**.

---

## ⚡ Why Dedicated Hardware?

| Feature | WT32-ETH01 Hardware Shield | Raspberry Pi / Pi-hole | Browser Ad-Blocker |
| :--- | :--- | :--- | :--- |
| **Power Draw** | **< 1 Watt** (~150mA at 5V) | 3 - 7 Watts | System Dependent |
| **Boot Time** | **< 1.0 second** instant-on | 30 - 60 seconds | Browser startup |
| **Storage Failure** | **Zero** (Solid-state NOR Flash) | High (SD card corruption risk) | N/A |
| **Network Latency** | **< 1 ms** direct silicon response | 2 - 5 ms | In-process overhead |
| **Device Coverage**| **All LAN devices** (IoT, Apps, Mobile) | All LAN devices | Browser only |
| **Maintenance** | **Zero OS updates, no Linux apt updates** | Requires Linux patching | Extension updates |

---

## 🚀 Key Features

* **Dual-Layer Hybrid Protection:**
  * **Layer 1 (Local Hardware):** 400+ targeted high-priority rules sinkholed locally on-chip in `< 1ms` directly to `0.0.0.0`.
  * **Layer 2 (Upstream Cloud Fallback):** Pre-configured with **AdGuard DNS** (`94.140.14.14` and `94.140.15.15`) as default upstream, filtering millions of generic web ads without taxing ESP32 RAM.
* **Curated Targeted Rule Matrix:**
  * 📱 **Android SDKs:** Blocks in-app ad networks & tracking SDKs (Google AdMob, Unity Ads, AppLovin, IronSource, Vungle, Mintegral, InMobi, Adjust, AppsFlyer, Kochava).
  * 🍏 **iPhone / iOS:** Blocks Apple Search Ads SDK (`iadsdk.apple.com`), Apple advertising telemetry, and app tracking beacons.
  * 🏠 **Tuya Smart Home:** Blocks data-leak telemetry and cloud analytics (`airtake.iot.tuya.com`, `log.tuya.com`, `tracking.tuya.com`) while **safely preserving local control and MQTT device automations**.
  * 💻 **Windows 10/11:** Blocks WindowsSpyBlocker feeds, Cortana telemetry, Watson error reporting, and diagnostic trackers.
  * 🐧 **Linux:** Blocks Canonical/Ubuntu Daisy metrics and Mozilla telemetry.
  * 🌐 **Universal Web Trackers:** Blocks DoubleClick, Criteo, Taboola, Outbrain, Facebook Pixels, and TikTok analytics.
* **Modern Pitch-Black Cyber Web Dashboard (`http://<DEVICE-IP>/`):**
  * Real-time query counter, blocked counter, block percentage, cache hit counter, and active client count.
  * Live rolling 45-second latency & traffic canvas graph.
  * Hardware silicon telemetry: CPU core load %, free heap memory, internal die temperature, and flash utilization.
  * Rule Manager & Catalog: Browse built-in rules, search domains, and manage custom blacklists/whitelists.
  * **Bulk Import:** Upload `.txt` / `.hosts` blocklists or paste domain lists directly into flash NVS memory.
  * 1-Click Upstream DNS switcher (AdGuard DNS, Cloudflare, Quad9, Google, Custom).
* **High-Speed RAM DNS Cache:**
  * Caches recently resolved clean domains in RAM for instant sub-millisecond responses without hitting upstream servers.

---

## 🔌 Hardware Setup & Wiring

### 1. WT32-ETH01 Specifications
* **MCU:** ESP32-D0WD-V3 (Dual Core 240MHz, 520KB SRAM, 4MB SPI Flash)
* **Ethernet PHY:** LAN8720A 10/100 Mbps transceiver
* **Default Static IP:** `107.7.97.95` (Subnet: `255.255.255.0`, Gateway: `107.7.97.77`)
* **Default Ports:** UDP `53` (DNS Sinkhole), TCP `80` (Cyber Web UI & REST API)

### 2. Flashing Pinout (FTDI USB-to-UART Adapter)

Connect your FTDI programmer to the WT32-ETH01 programming header:

| FTDI Pin | WT32-ETH01 Pin | Description |
| :--- | :--- | :--- |
| **5V** or **3V3** | **5V** or **3V3** | DC Power Supply |
| **GND** | **GND** | Common Ground |
| **RXD** | **TXD** (GPIO 1) | ESP32 UART Transmit |
| **TXD** | **RXD** (GPIO 3) | ESP32 UART Receive |
| *(Jumper Wire)* | **IO0 ➔ GND** | **Bridge ONLY while flashing!** Disconnect for normal boot. |

> [!IMPORTANT]
> **Bootloader Mode:** `IO0` must be connected to `GND` when plugging in USB power to flash the firmware.
> **Normal Mode:** Once flashing finishes, **disconnect `IO0` from `GND`** and power-cycle the board.

---

## 🌐 Network Deployment

```
                    ┌───────────────────────────┐
                    │       Wi-Fi Router        │
                    │      (107.7.97.77)        │
                    └─────────────┬─────────────┘
                                  │ LAN Port (RJ45)
                                  ▼
     ┌────────────────────────────────────────────────────────┐
     │           WT32-ETH01 Hardware Shield                   │
     │      Static IP: 107.7.97.95  |  Ports: 53, 80          │
     └────────────────────────────────────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
  [Android Phone]         [iPhone / iPad]          [Windows / Linux]
(In-app ads blocked)     (AdSDK telemetry dead)   (OS telemetry blocked)
```

### Router Configuration Steps:
1. Connect an RJ45 Ethernet patch cable from the WT32-ETH01 into any **LAN port** on your router.
2. Open your router's administration interface in a web browser (e.g. `http://107.7.97.77` or `http://192.168.1.1`).
3. Navigate to **DHCP Server Settings** / **LAN Settings**.
4. Set **Primary DNS (DNS Server 1)** to:
   ```text
   107.7.97.95
   ```
5. *(Optional)* Set Secondary DNS to `94.140.14.14` (AdGuard DNS) or leave it blank.
6. Save and reboot your router (or reconnect your devices' Wi-Fi to refresh DHCP leases).

---

## 🖥️ Web Dashboard

Access the onboard dashboard at:
👉 **`http://107.7.97.95`** *(Use plain `http://`, not `https://`)*

### Dashboard Modules:
* **Dashboard Tab:** Live query counters, block percentage, hardware silicon telemetry, and real-time traffic graph.
* **Network Devices Tab:** Automatic LAN client discovery table with per-device query counts and block rates.
* **Terminal Mode:** Live scrolling DNS stream showing every query domain, client IP, query type (A/AAAA), and status (Allowed/Blocked/Cached).
* **Top Domains Tab:** Top 10 most queried allowed domains vs top 10 sinkholed ad/tracking domains.
* **Upstream DNS & WAN Tab:** Change primary and secondary upstream DNS resolvers with 1-click latency benchmarks.
* **Rule Manager & Catalog Tab:** View all 413 active built-in rules, add custom whitelist/blacklist entries, and bulk-import `.txt` / `.hosts` files.
* **Router Setup Tab:** Interactive network instructions and DHCP setup guide.

---

## 📡 REST API Reference

The onboard web server exposes a lightweight JSON REST API:

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/telemetry` | `GET` | Full bundle: stats, logs, clients, top domains, and hardware metrics. |
| `/api/stats` | `GET` | Query counters, block rates, bandwidth, and cache stats. |
| `/api/logs` | `GET` | Recent DNS query history buffer (last 50 queries). |
| `/api/clients` | `GET` | Active LAN client list with query counts and block stats. |
| `/api/top_domains` | `GET` | Top allowed and blocked domain leaderboards. |
| `/api/benchmark` | `GET` | Live ping latency test to primary and secondary upstream DNS. |
| `/api/lists` | `GET` | Custom whitelist and blacklist rules stored in NVS. |
| `/api/add_white` | `POST` | Add domain to whitelist (`domain=<fqdn>`). |
| `/api/remove_white` | `POST` | Remove domain from whitelist (`domain=<fqdn>`). |
| `/api/add_block` | `POST` | Add domain to custom blacklist (`domain=<fqdn>`). |
| `/api/remove_block` | `POST` | Remove domain from custom blacklist (`domain=<fqdn>`). |
| `/api/add_bulk` | `POST` | Bulk import domains (`type=white|black`, `domains=<newline-delimited>`). |
| `/api/clear_list` | `POST` | Clear custom whitelist or blacklist (`type=white|black`). |
| `/api/toggle_blocking` | `POST` | Toggle global DNS sinkhole ON / OFF (`enabled=1|0`). |
| `/api/save_settings` | `POST` | Update upstream DNS servers (`dns1=<ip>`, `dns2=<ip>`). |
| `/api/reboot` | `POST` | Safely reboot the ESP32 module. |

---

## 🛠️ Build & Development

### Project Structure
```text
esp21-eth01-ad-blocker/
├── src/
│   ├── main.cpp              # Ethernet initialization, network setup, core loop
│   ├── dns_engine.cpp        # High-performance UDP 53 DNS sinkhole & parser
│   ├── dns_engine.h          # DNS data structures and cache definitions
│   ├── web_server.cpp        # HTTP Web server and REST API implementation
│   ├── web_server.h          # Web server declarations
│   ├── config_mgr.h          # Non-volatile storage (NVS) configuration manager
│   ├── blocklist.h           # PROGMEM C-array of 413 compiled rules
│   └── web_ui.h              # Gzipped PROGMEM web dashboard assets
├── platformio.ini            # PlatformIO board & compiler flags
├── build_web_ui.py           # Compiles dashboard.html into compressed src/web_ui.h
├── generate_blocklist.py     # Compiles domain lists into src/blocklist.h
├── flash.py                  # High-speed FTDI flasher tool (460,800 baud)
├── monitor.py                # Serial monitor utility (115,200 baud)
├── dashboard.html            # Standalone Cyber Dark Web UI source
└── README.md                 # Project documentation
```

### 1. Build Firmware (PlatformIO)
Make sure [PlatformIO Core](https://platformio.org/) is installed:
```bash
python -m platformio run
```

### 2. Flash to WT32-ETH01
Bridge `IO0` to `GND`, connect your FTDI adapter, and run:
```bash
python flash.py
```
*Disconnect `IO0` from `GND` after flashing and power-cycle.*

### 3. Update Web UI Assets
To modify the web interface:
1. Edit `dashboard.html` or `build_web_ui.py`.
2. Recompile the C++ header:
   ```bash
   python build_web_ui.py
   ```
3. Rebuild and flash the firmware.

### 4. Update Rule Catalog
To add or modify built-in hardware rules:
1. Edit the category lists inside `generate_blocklist.py`.
2. Regenerate `src/blocklist.h`:
   ```bash
   python generate_blocklist.py
   ```
3. Rebuild and flash the firmware.

---

## ❓ FAQ & Troubleshooting

#### Q: The web page shows `ERR_CONNECTION_REFUSED`
* Modern browsers automatically try `https://`. Ensure you type **`http://107.7.97.95`** explicitly. The ESP32 serves HTTP on port 80.

#### Q: The board does not boot after flashing
* Verify that you **removed the wire bridging `IO0` to `GND`**. If `IO0` remains grounded, the ESP32 stays trapped in bootloader mode.

#### Q: Does this break Tuya Smart Life or home automation?
* **No.** Only tracking and telemetry endpoints (`airtake.iot.tuya.com`, `log.tuya.com`) are sinkholed. Local LAN control, MQTT communication, and device provisioning are completely unaffected.

---

## 📄 License
This project is open-source and released under the [MIT License](LICENSE).
