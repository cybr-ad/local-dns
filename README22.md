# 🛡️ WT32-ETH01 Hardware Ad & Tracker Blocker

A standalone, plug-and-play **hardware ad blocker** built for the **WT32-ETH01 (ESP32 + Ethernet)** board.

Plug it into your router, and it automatically blocks ads, tracking SDKs, and telemetry on **every device** connected to your Wi-Fi (Android, iPhone, Windows, Linux, and Smart Home gadgets) — **no software or browser extensions needed!**

---

## ⚡ Quick Start in 3 Simple Steps

```
[Router LAN Port] <=== Ethernet Cable ===> [WT32-ETH01 Board]
                                                   │
                         Blocks ads on all Wi-Fi devices automatically!
```

### Step 1: Flash the Board
1. Connect your FTDI programmer to the WT32-ETH01:
   * **5V** ➔ **5V**
   * **GND** ➔ **GND**
   * **TXD** (FTDI) ➔ **RXD** (ESP32)
   * **RXD** (FTDI) ➔ **TXD** (ESP32)
   * **IO0** ➔ **GND** *(Connect this jumper wire ONLY while flashing!)*
2. Plug in the USB cable and run:
   ```bash
   python flash.py
   ```
3. **Remove the IO0 wire** from GND, and unplug/replug the power cable to boot normally.

---

### Step 2: Plug into Your Router
* Connect an Ethernet cable from the **WT32-ETH01** into any free **LAN port** on your Wi-Fi router.

---

### Step 3: Set Board IP as Router DNS (Crucial)
1. Open your router's setup page in a browser (e.g., `http://192.168.1.1` or `http://107.7.97.77`).
2. Go to **DHCP Settings**:
   * **TP-Link:** *Advanced ➔ Network ➔ DHCP Server*
   * **Asus:** *LAN ➔ DHCP Server*
   * **Netgear:** *Advanced ➔ Setup ➔ LAN Setup*
   * **Others:** *Network / LAN / DHCP Server*
3. Set **Primary DNS (DNS 1)** to the board's IP:
   ```text
   107.7.97.95
   ```
   *(Or your custom IP if you changed it in config).*
4. Click **Save**.
5. Disconnect and reconnect Wi-Fi on your phone or laptop. **You're all done! Ads are now blocked network-wide.**

---

## 🖥️ Live Web Dashboard

Open your browser and visit:
👉 **`http://107.7.97.95`** *(Use `http://`, not `https://`)*

Here you can:
* See live blocked queries and percentage in real-time.
* View which devices on your network are making DNS queries.
* Add your own custom Whitelist or Blacklist rules.
* Upload `.txt` domain lists.
* Switch upstream DNS providers (AdGuard DNS, Cloudflare, Quad9, Google) with 1 click.

---

## ⚙️ Changing the IP for Your Home Network

By default, the board uses static IP `107.7.97.95` with gateway `107.7.97.77`.

To adapt it to your router (e.g. `192.168.1.1`), open **`src/config_mgr.h`**:

### Option A: Automatic DHCP (Easiest)
Set `useStaticIp` to `false` so your router gives the board an IP automatically:
```cpp
// In src/config_mgr.h (Line 14)
bool useStaticIp = false;
```

### Option B: Custom Static IP
Change the IP and Gateway to match your network:
```cpp
// In src/config_mgr.h (Lines 14-18)
bool useStaticIp     = true;
String staticIp      = "192.168.1.50";   // An unused IP on your network
String staticGateway = "192.168.1.1";    // Your router's IP
String staticSubnet  = "255.255.255.0";  // Subnet mask
```
After editing, compile and re-flash:
```bash
python -m platformio run
python flash.py
```

---

## 🛡️ What Gets Blocked?

* 📱 **Android:** In-app ads (AdMob, UnityAds, AppLovin, Vungle, IronSource, Mintegral, Adjust, AppsFlyer).
* 🍏 **iPhone / iOS:** Apple Search Ads SDK and analytics tracking.
* 💻 **Windows 10/11:** Diagnostic telemetry, Cortana tracking, Watson error reporting.
* 🐧 **Linux:** Ubuntu/Canonical Daisy metrics and Mozilla telemetry.
* 🏠 **Tuya Smart Home:** Cloud telemetry data-leakage *(Local control and smart home automations stay 100% safe!)*.
* 🌐 **Universal Ads:** DoubleClick, Criteo, Taboola, Outbrain, Facebook & TikTok tracking pixels.

---

## ❓ Frequently Asked Questions (FAQ)

**Q: Why does the web dashboard show `ERR_CONNECTION_REFUSED`?**  
A: Make sure to type **`http://`** and not `https://`. The ESP32 uses standard HTTP on port 80.

**Q: The board won't boot after flashing?**  
A: You must **remove the jumper wire between IO0 and GND**. If IO0 is grounded, the board stays stuck in flashing mode.

**Q: Can I whitelist a domain if a site breaks?**  
A: Yes! Go to the Web Dashboard ➔ **Rule Manager & Catalog** ➔ type the domain under Whitelist and click **Add Domain**.

---

## 📄 License
MIT License - Free to use, modify, and distribute.
