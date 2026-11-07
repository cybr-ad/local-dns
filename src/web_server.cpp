#include "web_server.h"
#include "web_ui.h"
#include "dns_engine.h"
#include "config_mgr.h"

WebServerManager webServerMgr;

WebServerManager::WebServerManager() : server(80) {}

void WebServerManager::begin() {
    server.enableCORS(true);

    // Serve Web UI
    server.on("/", HTTP_GET, [this]() {
        server.send_P(200, "text/html", INDEX_HTML);
    });

    // Unified Ultra-Fast Telemetry API (Stats + Logs + Clients + TopDomains in 1 Request)
    server.on("/api/telemetry", HTTP_GET, [this]() {
        String json;
        dnsEngine.getTelemetryJson(json);
        server.send(200, "application/json", json);
    });

    // API: Stats
    server.on("/api/stats", HTTP_GET, [this]() {
        String json;
        dnsEngine.getStatsJson(json);
        server.send(200, "application/json", json);
    });

    // API: Logs
    server.on("/api/logs", HTTP_GET, [this]() {
        String json;
        dnsEngine.getLogsJson(json);
        server.send(200, "application/json", json);
    });

    // API: Clients
    server.on("/api/clients", HTTP_GET, [this]() {
        String json;
        dnsEngine.getClientsJson(json);
        server.send(200, "application/json", json);
    });

    // API: Top Domains
    server.on("/api/top_domains", HTTP_GET, [this]() {
        String json;
        dnsEngine.getTopDomainsJson(json);
        server.send(200, "application/json", json);
    });

    // API: Trigger LAN ARP Scan
    server.on("/api/scan_lan", HTTP_POST, [this]() {
        dnsEngine.triggerFullLanScan();
        server.send(200, "application/json", "{\"status\":\"scanning\"}");
    });

    // API: Flush Cache
    server.on("/api/flush_cache", HTTP_POST, [this]() {
        dnsEngine.flushCache();
        server.send(200, "application/json", "{\"status\":\"flushed\"}");
    });

    // API: Benchmark Upstream DNS
    server.on("/api/benchmark", HTTP_GET, [this]() {
        AppConfig& cfg = configMgr.getConfig();
        uint32_t lat1 = dnsEngine.benchmarkDns(cfg.upstreamDns1);
        uint32_t lat2 = dnsEngine.benchmarkDns(cfg.upstreamDns2);

        String json = "{";
        json += "\"dns1\":\"" + cfg.upstreamDns1 + "\",\"lat1\":" + String(lat1) + ",";
        json += "\"dns2\":\"" + cfg.upstreamDns2 + "\",\"lat2\":" + String(lat2);
        json += "}";
        server.send(200, "application/json", json);
    });

    // API: Lists
    server.on("/api/lists", HTTP_GET, [this]() {
        const auto& wl = configMgr.getWhitelist();
        const auto& bl = configMgr.getBlacklist();

        String json = "{\"whitelist\":[";
        for (size_t i = 0; i < wl.size(); i++) {
            if (i > 0) json += ",";
            json += "\"" + wl[i] + "\"";
        }
        json += "],\"blacklist\":[";
        for (size_t i = 0; i < bl.size(); i++) {
            if (i > 0) json += ",";
            json += "\"" + bl[i] + "\"";
        }
        json += "]}";
        server.send(200, "application/json", json);
    });

    // API: Add Whitelist
    server.on("/api/add_white", HTTP_POST, [this]() {
        if (server.hasArg("domain")) {
            configMgr.addWhitelist(server.arg("domain"));
            server.send(200, "application/json", "{\"status\":\"ok\"}");
        } else {
            server.send(400, "application/json", "{\"status\":\"missing domain\"}");
        }
    });

    // API: Remove Whitelist
    server.on("/api/remove_white", HTTP_POST, [this]() {
        if (server.hasArg("domain")) {
            configMgr.removeWhitelist(server.arg("domain"));
            server.send(200, "application/json", "{\"status\":\"ok\"}");
        } else {
            server.send(400, "application/json", "{\"status\":\"missing domain\"}");
        }
    });

    // API: Add Blacklist
    server.on("/api/add_block", HTTP_POST, [this]() {
        if (server.hasArg("domain")) {
            configMgr.addBlacklist(server.arg("domain"));
            server.send(200, "application/json", "{\"status\":\"ok\"}");
        } else {
            server.send(400, "application/json", "{\"status\":\"missing domain\"}");
        }
    });

    // API: Remove Blacklist
    server.on("/api/remove_block", HTTP_POST, [this]() {
        if (server.hasArg("domain")) {
            configMgr.removeBlacklist(server.arg("domain"));
            server.send(200, "application/json", "{\"status\":\"ok\"}");
        } else {
            server.send(400, "application/json", "{\"status\":\"missing domain\"}");
        }
    });

    // API: Bulk Add Rules (Fast batch import for .txt / .hosts files)
    server.on("/api/add_bulk", HTTP_POST, [this]() {
        if (server.hasArg("domains")) {
            String raw = server.arg("domains");
            bool isWhite = (server.arg("type") == "white");
            std::vector<String> domainList;
            int start = 0;
            for (int i = 0; i <= raw.length(); i++) {
                if (i == raw.length() || raw[i] == '\n' || raw[i] == ',' || raw[i] == ';') {
                    if (i > start) {
                        String d = raw.substring(start, i);
                        d.trim();
                        if (d.length() > 0) domainList.push_back(d);
                    }
                    start = i + 1;
                }
            }
            size_t added = configMgr.addBulk(domainList, isWhite);
            server.send(200, "application/json", "{\"status\":\"ok\",\"added\":" + String(added) + "}");
        } else {
            server.send(400, "application/json", "{\"status\":\"missing domains\"}");
        }
    });

    // API: Clear List
    server.on("/api/clear_list", HTTP_POST, [this]() {
        if (server.hasArg("type")) {
            bool isWhite = (server.arg("type") == "white");
            configMgr.clearList(isWhite);
            server.send(200, "application/json", "{\"status\":\"cleared\"}");
        } else {
            server.send(400, "application/json", "{\"status\":\"missing type\"}");
        }
    });

    // API: Toggle Blocking
    server.on("/api/toggle_blocking", HTTP_POST, [this]() {
        if (server.hasArg("enabled")) {
            bool en = (server.arg("enabled") == "1");
            configMgr.getConfig().blockingEnabled = en;
            configMgr.saveConfig();
            server.send(200, "application/json", "{\"status\":\"ok\"}");
        } else {
            server.send(400, "application/json", "{\"status\":\"missing param\"}");
        }
    });

    // API: Save Settings
    server.on("/api/save_settings", HTTP_POST, [this]() {
        if (server.hasArg("dns1")) {
            configMgr.getConfig().upstreamDns1 = server.arg("dns1");
        }
        if (server.hasArg("dns2")) {
            configMgr.getConfig().upstreamDns2 = server.arg("dns2");
        }
        configMgr.saveConfig();
        server.send(200, "application/json", "{\"status\":\"ok\"}");
    });

    // API: Reset Stats
    server.on("/api/reset_stats", HTTP_POST, [this]() {
        dnsEngine.resetStats();
        server.send(200, "application/json", "{\"status\":\"ok\"}");
    });

    // API: Reboot
    server.on("/api/reboot", HTTP_POST, [this]() {
        server.send(200, "application/json", "{\"status\":\"rebooting\"}");
        delay(500);
        ESP.restart();
    });

    server.begin();
    Serial.println("[HTTP] Web Dashboard running on port 80");
}

void WebServerManager::handle() {
    server.handleClient();
}
