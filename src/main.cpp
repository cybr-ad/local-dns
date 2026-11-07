#include <Arduino.h>
#include <ETH.h>
#include "config_mgr.h"
#include "dns_engine.h"
#include "web_server.h"

ConfigManager configMgr;
static bool ethConnected = false;
static bool servicesStarted = false;

void onEthEvent(arduino_event_id_t event) {
    switch (event) {
        case ARDUINO_EVENT_ETH_START:
            Serial.println("[ETH] Ethernet Interface Started");
            ETH.setHostname("esp32-adblocker");
            break;

        case ARDUINO_EVENT_ETH_CONNECTED:
            Serial.println("[ETH] Link UP! Cable connected to router.");
            break;

        case ARDUINO_EVENT_ETH_GOT_IP:
            Serial.println("\n========================================================");
            Serial.println("  ESP32-ETH01 AD & TRACKER BLOCKER ONLINE");
            Serial.println("========================================================");
            Serial.print("  IP Address:    ");
            Serial.println(ETH.localIP());
            Serial.print("  Subnet Mask:   ");
            Serial.println(ETH.subnetMask());
            Serial.print("  Gateway:       ");
            Serial.println(ETH.gatewayIP());
            Serial.print("  DNS Server:    ");
            Serial.println(ETH.dnsIP());
            Serial.print("  MAC Address:   ");
            Serial.println(ETH.macAddress());
            Serial.print("  Link Speed:    ");
            Serial.print(ETH.linkSpeed());
            Serial.println(" Mbps");
            Serial.println("--------------------------------------------------------");
            Serial.println("  Web Dashboard: http://" + ETH.localIP().toString() + "/");
            Serial.println("  DNS Port:      53 (UDP)");
            Serial.println("========================================================\n");

            ethConnected = true;

            if (!servicesStarted) {
                dnsEngine.begin();
                webServerMgr.begin();
                servicesStarted = true;
            }
            break;

        case ARDUINO_EVENT_ETH_DISCONNECTED:
            Serial.println("[ETH] Link DOWN! Cable unplugged.");
            ethConnected = false;
            break;

        case ARDUINO_EVENT_ETH_STOP:
            Serial.println("[ETH] Ethernet Interface Stopped");
            ethConnected = false;
            break;

        default:
            break;
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n\n========================================================");
    Serial.println("  WT32-ETH01 Hardware Ad & Tracker Shield Initializing  ");
    Serial.println("========================================================");

    // 1. Initialize persistent configuration
    configMgr.begin();
    AppConfig& cfg = configMgr.getConfig();
    Serial.printf("[CFG] Blocking: %s, Upstream DNS: %s\n", 
                  cfg.blockingEnabled ? "ENABLED" : "DISABLED", 
                  cfg.upstreamDns1.c_str());

    // 2. Attach Ethernet event listener
    Network.onEvent(onEthEvent);

    // 3. Initialize WT32-ETH01 LAN8720 PHY
    // Pin mapping: PHY Addr=1, MDC=23, MDIO=18, Power/Oscillator=16, Clock=GPIO0_IN
    Serial.println("[ETH] Initializing LAN8720 PHY...");
    ETH.begin(ETH_PHY_LAN8720, 1, 23, 18, 16, ETH_CLOCK_GPIO0_IN);

    // If static IP is configured:
    if (cfg.useStaticIp) {
        IPAddress ip, gw, sub, dns;
        if (ip.fromString(cfg.staticIp) && gw.fromString(cfg.staticGateway) &&
            sub.fromString(cfg.staticSubnet) && dns.fromString(cfg.staticDns)) {
            Serial.println("[ETH] Applying Static IP configuration...");
            ETH.config(ip, gw, sub, dns);
        }
    }
}

void loop() {
    if (servicesStarted) {
        dnsEngine.handle();
        webServerMgr.handle();
    }

    // Status heartbeat to Serial every 15 seconds
    static uint32_t lastPrint = 0;
    if (millis() - lastPrint > 15000) {
        lastPrint = millis();
        if (ethConnected) {
            const DnsStats& stats = dnsEngine.getStats();
            float rate = (stats.totalQueries > 0) ? 
                         ((float)stats.blockedQueries / stats.totalQueries * 100.0f) : 0.0f;
            Serial.printf("[STATUS] Queries: %lu | Blocked: %lu (%.1f%%) | Cached: %lu | Free Heap: %lu B\n",
                          (unsigned long)stats.totalQueries, 
                          (unsigned long)stats.blockedQueries, 
                          rate, 
                          (unsigned long)stats.cachedQueries, 
                          (unsigned long)ESP.getFreeHeap());
        } else {
            Serial.println("[STATUS] Waiting for Ethernet cable link...");
        }
    }
}
