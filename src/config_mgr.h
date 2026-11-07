#ifndef CONFIG_MGR_H
#define CONFIG_MGR_H

#include <Arduino.h>
#include <Preferences.h>
#include <vector>

struct AppConfig {
    bool blockingEnabled = true;
    String upstreamDns1 = "94.140.14.14"; // AdGuard DNS (Ad & Tracker Blocking)
    String upstreamDns2 = "94.140.15.15"; // AdGuard DNS Secondary (Failover)
    
    // IP mode: true = Static (107.7.97.95), false = DHCP
    bool useStaticIp = true;
    String staticIp = "107.7.97.95";
    String staticGateway = "107.7.97.77";
    String staticSubnet = "255.255.255.0";
    String staticDns = "1.1.1.1";
};

class ConfigManager {
private:
    Preferences prefs;
    AppConfig config;
    std::vector<String> customWhitelist;
    std::vector<String> customBlacklist;

public:
    void begin() {
        prefs.begin("adblocker", false);
        config.blockingEnabled = prefs.getBool("blk_en", true);
        config.upstreamDns1 = prefs.getString("dns1", "1.1.1.1");
        config.upstreamDns2 = prefs.getString("dns2", "8.8.8.8");
        config.useStaticIp = prefs.getBool("static_en", true);
        config.staticIp = prefs.getString("ip", "107.7.97.95");
        config.staticGateway = prefs.getString("gw", "107.7.97.77");
        config.staticSubnet = prefs.getString("sub", "255.255.255.0");
        config.staticDns = prefs.getString("sdns", "1.1.1.1");
        
        loadLists();
    }

    AppConfig& getConfig() {
        return config;
    }

    void saveConfig() {
        prefs.putBool("blk_en", config.blockingEnabled);
        prefs.putString("dns1", config.upstreamDns1);
        prefs.putString("dns2", config.upstreamDns2);
        prefs.putBool("static_en", config.useStaticIp);
        prefs.putString("ip", config.staticIp);
        prefs.putString("gw", config.staticGateway);
        prefs.putString("sub", config.staticSubnet);
        prefs.putString("sdns", config.staticDns);
    }

    void loadLists() {
        customWhitelist.clear();
        customBlacklist.clear();
        
        String wlStr = prefs.getString("wl", "");
        if (wlStr.length() > 0) {
            int start = 0;
            int idx = wlStr.indexOf(',');
            while (idx != -1) {
                String d = wlStr.substring(start, idx);
                d.trim();
                d.toLowerCase();
                if (d.length() > 0) customWhitelist.push_back(d);
                start = idx + 1;
                idx = wlStr.indexOf(',', start);
            }
            String last = wlStr.substring(start);
            last.trim();
            last.toLowerCase();
            if (last.length() > 0) customWhitelist.push_back(last);
        }

        String blStr = prefs.getString("bl", "");
        if (blStr.length() > 0) {
            int start = 0;
            int idx = blStr.indexOf(',');
            while (idx != -1) {
                String d = blStr.substring(start, idx);
                d.trim();
                d.toLowerCase();
                if (d.length() > 0) customBlacklist.push_back(d);
                start = idx + 1;
                idx = blStr.indexOf(',', start);
            }
            String last = blStr.substring(start);
            last.trim();
            last.toLowerCase();
            if (last.length() > 0) customBlacklist.push_back(last);
        }
    }

    void saveLists() {
        String wlStr = "";
        for (size_t i = 0; i < customWhitelist.size(); i++) {
            if (i > 0) wlStr += ",";
            wlStr += customWhitelist[i];
        }
        prefs.putString("wl", wlStr);

        String blStr = "";
        for (size_t i = 0; i < customBlacklist.size(); i++) {
            if (i > 0) blStr += ",";
            blStr += customBlacklist[i];
        }
        prefs.putString("bl", blStr);
    }

    bool isCustomWhitelisted(const String& domain) {
        String lower = domain;
        lower.toLowerCase();
        for (const auto& item : customWhitelist) {
            if (lower == item || lower.endsWith("." + item)) {
                return true;
            }
        }
        return false;
    }

    bool isCustomBlacklisted(const String& domain) {
        String lower = domain;
        lower.toLowerCase();
        for (const auto& item : customBlacklist) {
            if (lower == item || lower.endsWith("." + item)) {
                return true;
            }
        }
        return false;
    }

    bool addWhitelist(const String& domain) {
        String d = domain;
        d.trim();
        d.toLowerCase();
        if (d.length() == 0) return false;
        for (const auto& item : customWhitelist) {
            if (item == d) return false;
        }
        customWhitelist.push_back(d);
        saveLists();
        return true;
    }

    bool removeWhitelist(const String& domain) {
        String d = domain;
        d.trim();
        d.toLowerCase();
        for (auto it = customWhitelist.begin(); it != customWhitelist.end(); ++it) {
            if (*it == d) {
                customWhitelist.erase(it);
                saveLists();
                return true;
            }
        }
        return false;
    }

    bool addBlacklist(const String& domain) {
        String d = domain;
        d.trim();
        d.toLowerCase();
        if (d.length() == 0) return false;
        for (const auto& item : customBlacklist) {
            if (item == d) return false;
        }
        customBlacklist.push_back(d);
        saveLists();
        return true;
    }

    bool removeBlacklist(const String& domain) {
        String d = domain;
        d.trim();
        d.toLowerCase();
        for (auto it = customBlacklist.begin(); it != customBlacklist.end(); ++it) {
            if (*it == d) {
                customBlacklist.erase(it);
                saveLists();
                return true;
            }
        }
        return false;
    }

    size_t addBulk(const std::vector<String>& domains, bool isWhitelist) {
        size_t added = 0;
        auto& list = isWhitelist ? customWhitelist : customBlacklist;
        for (String d : domains) {
            d.trim();
            d.toLowerCase();
            if (d.length() == 0) continue;
            bool exists = false;
            for (const auto& item : list) {
                if (item == d) { exists = true; break; }
            }
            if (!exists) {
                list.push_back(d);
                added++;
            }
        }
        if (added > 0) {
            saveLists();
        }
        return added;
    }

    void clearList(bool isWhitelist) {
        if (isWhitelist) customWhitelist.clear();
        else customBlacklist.clear();
        saveLists();
    }

    const std::vector<String>& getWhitelist() const { return customWhitelist; }
    const std::vector<String>& getBlacklist() const { return customBlacklist; }
};

extern ConfigManager configMgr;

#endif // CONFIG_MGR_H
