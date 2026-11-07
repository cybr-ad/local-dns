# 🛡️ WT32-ETH01 Hardware Ad & Tracker Blocker

[![Platform](https://img.shields.io/badge/Platform-ESP32-blue.svg)](https://www.espressif.com/)
[![Ethernet](https://img.shields.io/badge/Ethernet-LAN8720A%20100Mbps-brightgreen.svg)]()
[![DNS Sinkhole](https://img.shields.io/badge/DNS-Port%2053%20(UDP)-red.svg)]()
[![Web Dashboard](https://img.shields.io/badge/Web%20Dashboard-Port%2080%20(HTTP)-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

A standalone, plug-and-play **hardware ad blocker and privacy shield** powered by the **Wireless-Tag WT32-ETH01 (ESP32 + LAN8720A 100Mbps Ethernet)** module.

Once connected to any LAN port on your router, it acts as the primary DNS server for your entire home. Every device connected to your Wi-Fi (Android, iPhone, Windows, Linux, and Smart Home gadgets) automatically blocks ads, telemetry, and tracking SDKs with **zero browser extensions or software installations required**.

```
                           +------------------------+
                           |      Wi-Fi Router      |
                           +-----------+------------+
                                       |
                       Ethernet Cable  | (LAN Port)
                                       v
                     +------------------------------------+
                     |    WT32-ETH01 Hardware Shield      |
                     |  - High-Speed DNS Sinkhole (P53)   |
                     |  - Cyber Web Dashboard (P80)       |
                     +-----------------+------------------+
                                       |
               +-----------------------+-----------------------+
               |                       |                       |
               v                       v                       v
        [Android Phone]         [iPhone / iPad]        [Windows / Linux]
     (In-app ads blocked)     (Trackers blocked)     (Telemetry blocked)
```

---

## 🚀 1-Click Automated Setup (Recommended)

The easiest way to configure, compile, and flash the board is using the included **Setup Wizard**:

👉 **Double-click `SETUP_AND_FLASH.bat`**

The interactive wizard will:
1. **Auto-detect your router gateway** and calculate a matching static IP.
2. **Ask you for your desired board IP & COM port** (or FTDI programmer).
3. **Automatically update the code, rebuild the Web UI, and compile the firmware**.
4. **Flash the board** at high-speed (460,800 baud) once you bridge `IO0` to `GND`.
5. Display the exact DNS IP to enter into your router's DHCP settings.

---

## ⚡ Manual Quick Start in 3 Simple Steps

### Step 1: Wire Programmer & Flash
Connect your FTDI or USB-to-UART programmer (CH340, CP2102, FT232R) to the WT32-ETH01:

| Programmer Pin | WT32-ETH01 Pin | Description |
| :--- | :--- | :--- |
| **5V** or **3V3** | **5V** or **3V3** | Power Supply |
| **GND** | **GND** | Common Ground |
| **TXD** | **RXD** (GPIO 3) | ESP32 Receive |
| **RXD** | **TXD** (GPIO 1) | ESP32 Transmit |
| *(Jumper Wire)* | **IO0 ➔ GND** | **Bridge ONLY while flashing!** |

1. Bridge **`IO0` to `GND`** and connect the USB cable to enter download mode.
2. Run:
   ```bash
   python flash.py
   ```
3. **Disconnect the `IO0` wire from `GND`**, and unplug/replug the power cable to boot normally.

---

### Step 2: Connect Ethernet to Your Router
* Plug an RJ45 Ethernet patch cable from the **WT32-ETH01** into any free **LAN port** on your Wi-Fi router.

---

### Step 3: Set Board IP as Router DNS (Crucial)
To enable network-wide blocking across all phones, PCs, and TVs:

1. Open your router's setup page in a browser (e.g. `http://192.168.1.1` or `http://107.7.97.77`).
2. Go to **DHCP Settings**:
   * **TP-Link (Archer):** *Advanced ➔ Network ➔ DHCP Server*
   * **Asus (Asuswrt):** *LAN ➔ DHCP Server*
   * **Netgear:** *Advanced ➔ Setup ➔ LAN Setup*
   * **OpenWrt:** *Network ➔ Interfaces ➔ LAN ➔ DHCP Server*
   * **Others:** *Network / LAN / DHCP Server*
3. Set **Primary DNS (DNS Server 1)** to the board's IP:
   ```text
   107.7.97.95
   ```
   *(Or your custom IP if you configured a different one).*
4. *(Optional)* Set Secondary DNS to `94.140.14.14` (AdGuard DNS) or leave it blank.
5. Click **Save** and reconnect your devices to Wi-Fi. **All ads are now blocked network-wide!**

---

## 🖥️ Live Cyber Web Dashboard

Open your browser and navigate to:
👉 **`http://107.7.97.95`** *(Use plain `http://`, not `https://`)*

### Key Dashboard Features:
* **Real-time DNS Stats:** Live total queries, blocked ads, block percentage, cache hits, and active client count.
* **Rolling 45-Second Latency Graph:** Visual traffic and upstream latency stream.
* **Network Devices Table:** Automatically discovers devices on your LAN with per-client query counters and block rates.
* **Terminal Mode:** Live streaming feed of every DNS request on your network (domain, client IP, query type, latency, and status).
* **Rule Manager & Catalog:** Browse 400+ built-in rules, add custom whitelists/blacklists, or upload `.txt` / `.hosts` blocklists.
* **1-Click Upstream DNS:** Switch between AdGuard DNS, Cloudflare, Quad9, Google, or custom DNS with built-in latency benchmark testing.

---

## ⚙️ Changing the IP for Your Network

By default, the board uses static IP `107.7.97.95` with gateway `107.7.97.77`.

If you prefer not using `SETUP_AND_FLASH.bat`, you can easily adjust it manually in **`src/config_mgr.h`**:

### Option A: Automatic DHCP Mode (Zero Configuration)
Set `useStaticIp` to `false` so your router gives the board an IP automatically:
```cpp
// In src/config_mgr.h (Line 14)
bool useStaticIp = false;
```

### Option B: Custom Static IP
Change the IP and Gateway to match your network subnet:
```cpp
// In src/config_mgr.h (Lines 14-18)
bool useStaticIp     = true;
String staticIp      = "192.168.1.50";   // An unused IP on your network
String staticGateway = "192.168.1.1";    // Your router's LAN IP
String staticSubnet  = "255.255.255.0";  // Subnet mask
```
Then compile and flash:
```bash
python -m platformio run
python flash.py
```

---

## 🛡️ What Gets Blocked?

* 📱 **Android:** In-app ad networks and tracking SDKs (Google AdMob, UnityAds, AppLovin, Vungle, IronSource, Mintegral, InMobi, Adjust, AppsFlyer, Kochava).
* 🍏 **iPhone / iOS:** Apple Search Ads SDK (`iadsdk.apple.com`), Apple advertising telemetry, and analytics beacons.
* 💻 **Windows 10/11:** Diagnostic telemetry (WindowsSpyBlocker feeds), Cortana data collection, Watson error diagnostics.
* 🐧 **Linux:** Ubuntu/Canonical Daisy metrics and Mozilla telemetry.
* 🏠 **Tuya Smart Home:** Cloud telemetry and tracking (`airtake.iot.tuya.com`, `log.tuya.com`) while **safely preserving local control and MQTT smart automations**.
* 🌐 **Universal Web Ads:** DoubleClick, Criteo, Taboola, Outbrain, Facebook Pixels, and TikTok analytics.

---

## ❓ Frequently Asked Questions (FAQ)

#### Q: The browser shows `ERR_CONNECTION_REFUSED` when opening the dashboard
* Make sure you typed **`http://107.7.97.95`** explicitly and not `https://`. Modern browsers often auto-upgrade to HTTPS, but the ESP32 serves HTTP on port 80.

#### Q: The board will not boot after flashing
* Ensure you **disconnected the jumper wire between `IO0` and `GND`**. If `IO0` remains connected to `GND`, the ESP32 stays trapped in bootloader mode.

#### Q: Can I whitelist a domain if a site or service breaks?
* Yes! Go to the Web Dashboard ➔ **Rule Manager & Catalog** ➔ enter the domain under **Whitelist Domain** and click **Add Domain**. It saves instantly to non-volatile flash memory (NVS).

---

## 📄 License
Released under the [MIT License](LICENSE). Free for personal and commercial use.
