#include "dns_engine.h"
#include <lwip/etharp.h>
#include <lwip/ip4_addr.h>
#include <lwip/netif.h>
#include <lwip/tcpip.h>

DnsEngine dnsEngine;

DnsEngine::DnsEngine() {
}

bool DnsEngine::begin() {
    stats.startTime = millis();
    lastSpeedCalc = millis();
    lastArpScan = millis();
    bool cOk = clientUdp.begin(53);
    bool uOk = upstreamUdp.begin(0);
    Serial.printf("[DNS] Turbo Engine active on port 53 (ClientUDP=%s, UpstreamUDP=%s)\n", 
                  cOk ? "OK" : "FAIL", uOk ? "OK" : "FAIL");
    return cOk && uOk;
}

void DnsEngine::resetStats() {
    stats.totalQueries = 0;
    stats.blockedQueries = 0;
    stats.cachedQueries = 0;
    stats.forwardQueries = 0;
    stats.startTime = millis();
    stats.totalBytesRx = 0;
    stats.totalBytesTx = 0;
    stats.totalPacketsRx = 0;
    stats.totalPacketsTx = 0;
    stats.speedRxBps = 0;
    stats.speedTxBps = 0;
    stats.packetsPerSec = 0;
    stats.upstreamLatencyMs = 11;

    clientCount = 0;
    topAllowedCount = 0;
    topBlockedCount = 0;
    flushCache();
}

void DnsEngine::flushCache() {
    for (size_t i = 0; i < MAX_CACHE; i++) {
        cache[i].valid = false;
    }
}

String DnsEngine::resolveMac(const IPAddress& clientIp) {
    ip4_addr_t ipaddr;
    ipaddr.addr = static_cast<uint32_t>(clientIp);
    
    char buf[18] = {0};
    bool found = false;

    LOCK_TCPIP_CORE();
    for (size_t i = 0; i < 32; i++) {
        ip4_addr_t *entry_ip = nullptr;
        struct netif *entry_netif = nullptr;
        struct eth_addr *entry_mac = nullptr;
        if (etharp_get_entry(i, &entry_ip, &entry_netif, &entry_mac) == 1) {
            if (entry_ip && entry_ip->addr == ipaddr.addr && entry_mac) {
                snprintf(buf, sizeof(buf), "%02X:%02X:%02X:%02X:%02X:%02X",
                         entry_mac->addr[0], entry_mac->addr[1], entry_mac->addr[2],
                         entry_mac->addr[3], entry_mac->addr[4], entry_mac->addr[5]);
                found = true;
                break;
            }
        }
    }
    if (!found && netif_default) {
        etharp_request(netif_default, &ipaddr);
    }
    UNLOCK_TCPIP_CORE();

    return found ? String(buf) : "";
}

void DnsEngine::recordDiscoveredDevice(const IPAddress& ip, const String& mac) {
    String ipStr = ip.toString();
    for (size_t i = 0; i < clientCount; i++) {
        if (clients[i].ip == ipStr) {
            if (clients[i].mac.length() == 0 || clients[i].mac == "--") {
                clients[i].mac = mac;
            }
            return;
        }
    }
    if (clientCount < MAX_CLIENTS) {
        clients[clientCount].ip = ipStr;
        clients[clientCount].mac = mac;
        clients[clientCount].totalQueries = 0;
        clients[clientCount].totalBytes = 0;
        clients[clientCount].blockedQueries = 0;
        clients[clientCount].lastSeen = millis();
        clients[clientCount].isDiscovered = true;
        clientCount++;
    }
}

void DnsEngine::harvestArpTable() {
    LOCK_TCPIP_CORE();
    for (size_t i = 0; i < 32; i++) {
        ip4_addr_t *entry_ip = nullptr;
        struct netif *entry_netif = nullptr;
        struct eth_addr *entry_mac = nullptr;
        if (etharp_get_entry(i, &entry_ip, &entry_netif, &entry_mac) == 1) {
            if (entry_ip && entry_mac) {
                IPAddress ip(entry_ip->addr);
                // Ignore broadcast / multicast
                if (ip[0] != 224 && ip[0] != 239 && ip[3] != 255 && ip[3] != 0) {
                    char buf[18];
                    snprintf(buf, sizeof(buf), "%02X:%02X:%02X:%02X:%02X:%02X",
                             entry_mac->addr[0], entry_mac->addr[1], entry_mac->addr[2],
                             entry_mac->addr[3], entry_mac->addr[4], entry_mac->addr[5]);
                    recordDiscoveredDevice(ip, String(buf));
                }
            }
        }
    }
    UNLOCK_TCPIP_CORE();
}

void DnsEngine::scanNextLanHost() {
    if (!netif_default) return;
    AppConfig& cfg = configMgr.getConfig();
    IPAddress baseIp;
    if (!baseIp.fromString(cfg.staticIp)) {
        baseIp = IPAddress(107, 7, 97, 95);
    }

    LOCK_TCPIP_CORE();
    for (int k = 0; k < 2; k++) {
        if (nextScanHost > 115) nextScanHost = 70;
        if (nextScanHost != baseIp[3]) {
            ip4_addr_t target;
            IP4_ADDR(&target, baseIp[0], baseIp[1], baseIp[2], nextScanHost);
            etharp_request(netif_default, &target);
        }
        nextScanHost++;
    }
    UNLOCK_TCPIP_CORE();
}

void DnsEngine::triggerFullLanScan() {
    if (!netif_default) return;
    AppConfig& cfg = configMgr.getConfig();
    IPAddress baseIp;
    if (!baseIp.fromString(cfg.staticIp)) {
        baseIp = IPAddress(107, 7, 97, 95);
    }
    LOCK_TCPIP_CORE();
    for (uint8_t h = 70; h <= 115; h++) {
        if (h != baseIp[3]) {
            ip4_addr_t target;
            IP4_ADDR(&target, baseIp[0], baseIp[1], baseIp[2], h);
            etharp_request(netif_default, &target);
        }
    }
    UNLOCK_TCPIP_CORE();
}

void DnsEngine::recordClientQuery(const IPAddress& clientIp, bool blocked, size_t bytes) {
    String ipStr = clientIp.toString();
    for (size_t i = 0; i < clientCount; i++) {
        if (clients[i].ip == ipStr) {
            clients[i].totalQueries++;
            clients[i].totalBytes += bytes;
            if (blocked) clients[i].blockedQueries++;
            clients[i].lastSeen = millis();
            clients[i].isDiscovered = false;
            if (clients[i].mac.length() == 0 || clients[i].mac == "--") {
                clients[i].mac = resolveMac(clientIp);
            }
            return;
        }
    }
    if (clientCount < MAX_CLIENTS) {
        clients[clientCount].ip = ipStr;
        clients[clientCount].mac = resolveMac(clientIp);
        clients[clientCount].totalQueries = 1;
        clients[clientCount].totalBytes = bytes;
        clients[clientCount].blockedQueries = blocked ? 1 : 0;
        clients[clientCount].lastSeen = millis();
        clients[clientCount].isDiscovered = false;
        clientCount++;
    }
}

void DnsEngine::recordDomainRank(const String& domain, bool blocked) {
    DomainRank* list = blocked ? topBlocked : topAllowed;
    size_t& count = blocked ? topBlockedCount : topAllowedCount;

    for (size_t i = 0; i < count; i++) {
        if (list[i].domain == domain) {
            list[i].count++;
            while (i > 0 && list[i].count > list[i-1].count) {
                DomainRank temp = list[i];
                list[i] = list[i-1];
                list[i-1] = temp;
                i--;
            }
            return;
        }
    }

    if (count < MAX_TOP) {
        list[count].domain = domain;
        list[count].count = 1;
        count++;
    }
}

bool DnsEngine::parseDnsQuestion(const uint8_t* buf, size_t len, size_t& offset, String& outDomain, uint16_t& outQtype) {
    if (len < 12) return false;
    offset = 12;
    outDomain = "";

    while (offset < len) {
        uint8_t labelLen = buf[offset++];
        if (labelLen == 0) break;
        if ((labelLen & 0xC0) == 0xC0) {
            offset++;
            break;
        }
        if (offset + labelLen > len) return false;
        if (outDomain.length() > 0) outDomain += ".";
        for (uint8_t i = 0; i < labelLen; i++) {
            char c = (char)buf[offset++];
            if (c >= 'A' && c <= 'Z') c += ('a' - 'A');
            outDomain += c;
        }
    }

    if (offset + 4 > len) return false;
    outQtype = (buf[offset] << 8) | buf[offset + 1];
    offset += 4;
    return true;
}

void DnsEngine::sendSinkholeResponse(const uint8_t* queryBuf, size_t queryLen, size_t questionEnd, const IPAddress& clientIp, uint16_t clientPort, uint16_t id, uint16_t qtype) {
    uint8_t resp[512];
    if (questionEnd > 400) return;

    memcpy(resp, queryBuf, questionEnd);
    resp[0] = (uint8_t)(id >> 8);
    resp[1] = (uint8_t)(id & 0xFF);
    resp[2] = 0x81;
    resp[3] = 0x80;
    resp[4] = 0x00;
    resp[5] = 0x01;

    size_t respLen = questionEnd;

    if (qtype == 1) { // Type A (IPv4)
        resp[6] = 0x00; resp[7] = 0x01; // 1 Answer
        resp[8] = 0x00; resp[9] = 0x00;
        resp[10] = 0x00; resp[11] = 0x00;

        resp[respLen++] = 0xC0; resp[respLen++] = 0x0C; // Pointer to QNAME
        resp[respLen++] = 0x00; resp[respLen++] = 0x01; // TYPE A
        resp[respLen++] = 0x00; resp[respLen++] = 0x01; // CLASS IN
        resp[respLen++] = 0x00; resp[respLen++] = 0x00; resp[respLen++] = 0x01; resp[respLen++] = 0x2C; // TTL 300s
        resp[respLen++] = 0x00; resp[respLen++] = 0x04; // RDLENGTH 4
        resp[respLen++] = 0x00; resp[respLen++] = 0x00; resp[respLen++] = 0x00; resp[respLen++] = 0x00; // 0.0.0.0
    } else {
        resp[6] = 0x00; resp[7] = 0x00; // NODATA
        resp[8] = 0x00; resp[9] = 0x00;
        resp[10] = 0x00; resp[11] = 0x00;
    }

    clientUdp.beginPacket(clientIp, clientPort);
    clientUdp.write(resp, respLen);
    clientUdp.endPacket();

    stats.totalBytesTx += respLen;
    stats.totalPacketsTx++;
    windowBytesTx += respLen;
    windowPackets++;
}

void DnsEngine::logQuery(const IPAddress& clientIp, const String& clientMac, const String& domain, uint16_t qtype, QueryVerdict verdict, uint16_t durationMs) {
    queryLogs[logIndex].clientIp = clientIp.toString();
    queryLogs[logIndex].clientMac = clientMac.length() > 0 ? clientMac : resolveMac(clientIp);
    queryLogs[logIndex].domain = domain;
    queryLogs[logIndex].qtype = qtype;
    queryLogs[logIndex].verdict = (uint8_t)verdict;
    queryLogs[logIndex].durationMs = durationMs;
    queryLogs[logIndex].timestamp = millis();

    logIndex = (logIndex + 1) % MAX_LOGS;
    if (logCount < MAX_LOGS) logCount++;
}

int DnsEngine::findCache(const String& domain, uint16_t qtype) {
    uint32_t now = millis();
    for (size_t i = 0; i < MAX_CACHE; i++) {
        if (cache[i].valid && cache[i].qtype == qtype && cache[i].domain == domain) {
            if (now < cache[i].expireAt) return (int)i;
            cache[i].valid = false;
        }
    }
    return -1;
}

void DnsEngine::addCache(const String& domain, uint16_t qtype, uint32_t ttlSec, const uint8_t* respBuf, size_t respLen) {
    if (respLen > sizeof(cache[0].data)) return;
    size_t idx = cacheNextIdx;
    cacheNextIdx = (cacheNextIdx + 1) % MAX_CACHE;

    cache[idx].valid = true;
    cache[idx].domain = domain;
    cache[idx].qtype = qtype;
    cache[idx].expireAt = millis() + (ttlSec * 1000);
    cache[idx].dataLen = respLen;
    memcpy(cache[idx].data, respBuf, respLen);
}

void DnsEngine::handle() {
    uint32_t now = millis();

    // 1. Throughput & Packets Calculation (Every 1000ms with smoothing)
    if (now - lastSpeedCalc >= 1000) {
        uint32_t elapsedMs = now - lastSpeedCalc;
        uint32_t instRx = (windowBytesRx * 1000) / elapsedMs;
        uint32_t instTx = (windowBytesTx * 1000) / elapsedMs;
        uint32_t instPkts = (windowPackets * 1000) / elapsedMs;

        stats.speedRxBps = (stats.speedRxBps * 3 + instRx * 7) / 10;
        stats.speedTxBps = (stats.speedTxBps * 3 + instTx * 7) / 10;
        stats.packetsPerSec = (stats.packetsPerSec * 3 + instPkts * 7) / 10;

        windowBytesRx = 0;
        windowBytesTx = 0;
        windowPackets = 0;
        lastSpeedCalc = now;
    }

    // 2. Background LAN Discovery & ARP Harvesting (safe interval)
    if (now > 8000 && now - lastArpScan >= 3500) {
        scanNextLanHost();
        harvestArpTable();
        lastArpScan = now;
    }

    // 3. Multi-Packet Client Query Drain Loop (Up to 16 packets per tick)
    int clientBatch = 16;
    int packetSize = 0;
    while ((packetSize = clientUdp.parsePacket()) >= 12 && packetSize <= 512 && --clientBatch >= 0) {
        uint8_t buf[512];
        int bytesRead = clientUdp.read(buf, sizeof(buf));
        if (bytesRead >= 12) {
            stats.totalBytesRx += bytesRead;
            stats.totalPacketsRx++;
            windowBytesRx += bytesRead;
            windowPackets++;

            IPAddress clientIp = clientUdp.remoteIP();
            uint16_t clientPort = clientUdp.remotePort();
            String clientMac = resolveMac(clientIp);

            uint16_t id = (buf[0] << 8) | buf[1];
            uint16_t flags = (buf[2] << 8) | buf[3];
            bool isQuery = ((flags & 0x8000) == 0);

            if (isQuery) {
                stats.totalQueries++;
                size_t questionEnd = 0;
                String domain;
                uint16_t qtype = 1;

                if (parseDnsQuestion(buf, bytesRead, questionEnd, domain, qtype)) {
                    bool blocked = false;
                    AppConfig& cfg = configMgr.getConfig();

                    if (cfg.blockingEnabled) {
                        if (configMgr.isCustomWhitelisted(domain)) {
                            blocked = false;
                        } else if (configMgr.isCustomBlacklisted(domain)) {
                            blocked = true;
                        } else if (isDomainBlockedBuiltin(domain.c_str())) {
                            blocked = true;
                        }
                    }

                    recordClientQuery(clientIp, blocked, bytesRead);
                    recordDomainRank(domain, blocked);

                    if (blocked) {
                        stats.blockedQueries++;
                        sendSinkholeResponse(buf, bytesRead, questionEnd, clientIp, clientPort, id, qtype);
                        logQuery(clientIp, clientMac, domain, qtype, VERDICT_BLOCKED, 0);
                    } else {
                        // Check local cache
                        int cIdx = findCache(domain, qtype);
                        if (cIdx >= 0) {
                            stats.cachedQueries++;
                            uint8_t cacheBuf[512];
                            memcpy(cacheBuf, cache[cIdx].data, cache[cIdx].dataLen);
                            cacheBuf[0] = (uint8_t)(id >> 8);
                            cacheBuf[1] = (uint8_t)(id & 0xFF);

                            clientUdp.beginPacket(clientIp, clientPort);
                            clientUdp.write(cacheBuf, cache[cIdx].dataLen);
                            clientUdp.endPacket();

                            stats.totalBytesTx += cache[cIdx].dataLen;
                            stats.totalPacketsTx++;
                            windowBytesTx += cache[cIdx].dataLen;
                            windowPackets++;

                            logQuery(clientIp, clientMac, domain, qtype, VERDICT_CACHED, 1);
                        } else {
                            // Forward query to upstream DNS
                            stats.forwardQueries++;
                            uint16_t upId = nextUpstreamId++;
                            if (nextUpstreamId > 60000) nextUpstreamId = 1000;

                            size_t slot = upId % MAX_PENDING;
                            pendingQueries[slot].active = true;
                            pendingQueries[slot].upstreamId = upId;
                            pendingQueries[slot].origId = id;
                            pendingQueries[slot].clientIp = clientIp;
                            pendingQueries[slot].clientMac = clientMac;
                            pendingQueries[slot].clientPort = clientPort;
                            pendingQueries[slot].domain = domain;
                            pendingQueries[slot].qtype = qtype;
                            pendingQueries[slot].sendTime = millis();
                            pendingQueries[slot].retriedSecondary = false;

                            buf[0] = (uint8_t)(upId >> 8);
                            buf[1] = (uint8_t)(upId & 0xFF);

                            IPAddress upstreamIp;
                            if (!upstreamIp.fromString(cfg.upstreamDns1)) {
                                upstreamIp = IPAddress(94, 140, 14, 14); // Default to AdGuard DNS
                            }

                            upstreamUdp.beginPacket(upstreamIp, 53);
                            upstreamUdp.write(buf, bytesRead);
                            upstreamUdp.endPacket();

                            stats.totalBytesTx += bytesRead;
                            stats.totalPacketsTx++;
                            windowBytesTx += bytesRead;
                            windowPackets++;
                        }
                    }
                }
            }
        }
    }

    // 4. Multi-Packet Upstream Response Drain Loop (Up to 16 packets per tick)
    int upBatch = 16;
    int upPacketSize = 0;
    while ((upPacketSize = upstreamUdp.parsePacket()) >= 12 && upPacketSize <= 512 && --upBatch >= 0) {
        uint8_t upBuf[512];
        int upRead = upstreamUdp.read(upBuf, sizeof(upBuf));
        if (upRead >= 12) {
            stats.totalBytesRx += upRead;
            stats.totalPacketsRx++;
            windowBytesRx += upRead;
            windowPackets++;

            uint16_t upId = (upBuf[0] << 8) | upBuf[1];
            size_t slot = upId % MAX_PENDING;

            if (pendingQueries[slot].active && pendingQueries[slot].upstreamId == upId) {
                uint16_t duration = (uint16_t)(millis() - pendingQueries[slot].sendTime);
                stats.upstreamLatencyMs = duration;

                upBuf[0] = (uint8_t)(pendingQueries[slot].origId >> 8);
                upBuf[1] = (uint8_t)(pendingQueries[slot].origId & 0xFF);

                clientUdp.beginPacket(pendingQueries[slot].clientIp, pendingQueries[slot].clientPort);
                clientUdp.write(upBuf, upRead);
                clientUdp.endPacket();

                stats.totalBytesTx += upRead;
                stats.totalPacketsTx++;
                windowBytesTx += upRead;
                windowPackets++;

                logQuery(pendingQueries[slot].clientIp, pendingQueries[slot].clientMac, pendingQueries[slot].domain, 
                         pendingQueries[slot].qtype, VERDICT_ALLOWED, duration);

                uint16_t ancount = (upBuf[6] << 8) | upBuf[7];
                if (ancount > 0) {
                    addCache(pendingQueries[slot].domain, pendingQueries[slot].qtype, 300, upBuf, upRead);
                }

                pendingQueries[slot].active = false;
            }
        }
    }

    // 5. Secondary DNS Failover check: retry if pending > 700ms
    for (size_t i = 0; i < MAX_PENDING; i++) {
        if (pendingQueries[i].active) {
            uint32_t age = now - pendingQueries[i].sendTime;
            AppConfig& cfg = configMgr.getConfig();

            if (!pendingQueries[i].retriedSecondary && age > 700 && cfg.upstreamDns2.length() > 0) {
                IPAddress secIp;
                if (secIp.fromString(cfg.upstreamDns2)) {
                    pendingQueries[i].retriedSecondary = true;
                }
            } else if (age > 4000) {
                pendingQueries[i].active = false; // Expire query
            }
        }
    }
}

uint32_t DnsEngine::benchmarkDns(const String& serverIp) {
    IPAddress ip;
    if (!ip.fromString(serverIp)) return 999;

    WiFiUDP testUdp;
    testUdp.begin(0);
    uint32_t start = millis();

    uint8_t q[] = {
        0xAA, 0x55, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x0a, 'c','l','o','u','d','f','l','a','r','e',
        0x03, 'c','o','m', 0x00, 0x00, 0x01, 0x00, 0x01
    };

    testUdp.beginPacket(ip, 53);
    testUdp.write(q, sizeof(q));
    testUdp.endPacket();

    while (millis() - start < 1500) {
        if (testUdp.parsePacket() > 0) {
            uint32_t lat = millis() - start;
            testUdp.stop();
            return lat;
        }
        delay(5);
    }
    testUdp.stop();
    return 999;
}

void DnsEngine::getStatsJson(String& outJson) const {
    uint32_t uptimeSec = (millis() - stats.startTime) / 1000;
    float blockPct = 0.0f;
    if (stats.totalQueries > 0) {
        blockPct = ((float)stats.blockedQueries / (float)stats.totalQueries) * 100.0f;
    }

    uint32_t freeHeap = ESP.getFreeHeap();
    uint32_t minHeap = ESP.getMinFreeHeap();
    uint32_t totalHeap = ESP.getHeapSize();
    uint32_t cpuFreq = ESP.getCpuFreqMHz();
    uint32_t flashSize = ESP.getFlashChipSize();
    uint32_t sketchSize = ESP.getSketchSize();
    uint32_t freeSketch = ESP.getFreeSketchSpace();
    float chipTemp = temperatureRead();

    outJson = "{";
    outJson += "\"total\":" + String(stats.totalQueries) + ",";
    outJson += "\"blocked\":" + String(stats.blockedQueries) + ",";
    outJson += "\"cached\":" + String(stats.cachedQueries) + ",";
    outJson += "\"forward\":" + String(stats.forwardQueries) + ",";
    outJson += "\"blockRate\":" + String(blockPct, 1) + ",";
    outJson += "\"uptime\":" + String(uptimeSec) + ",";
    outJson += "\"heap\":" + String(freeHeap) + ",";
    outJson += "\"minHeap\":" + String(minHeap) + ",";
    outJson += "\"totalHeap\":" + String(totalHeap) + ",";
    outJson += "\"cpuFreq\":" + String(cpuFreq) + ",";
    outJson += "\"flashSize\":" + String(flashSize) + ",";
    outJson += "\"sketchSize\":" + String(sketchSize) + ",";
    outJson += "\"freeSketch\":" + String(freeSketch) + ",";
    outJson += "\"tempC\":" + String(chipTemp, 1) + ",";
    outJson += "\"blocking\":" + String(configMgr.getConfig().blockingEnabled ? "true" : "false") + ",";
    outJson += "\"builtinCount\":" + String(BUILTIN_BLOCKLIST_COUNT) + ",";
    outJson += "\"whitelistCount\":" + String(configMgr.getWhitelist().size()) + ",";
    outJson += "\"blacklistCount\":" + String(configMgr.getBlacklist().size()) + ",";
    outJson += "\"upstreamDns\":\"" + configMgr.getConfig().upstreamDns1 + "\",";
    outJson += "\"upstreamDns2\":\"" + configMgr.getConfig().upstreamDns2 + "\",";
    outJson += "\"rxBytes\":" + String((uint32_t)stats.totalBytesRx) + ",";
    outJson += "\"txBytes\":" + String((uint32_t)stats.totalBytesTx) + ",";
    outJson += "\"totalPackets\":" + String(stats.totalPacketsRx + stats.totalPacketsTx) + ",";
    outJson += "\"speedRx\":" + String(stats.speedRxBps) + ",";
    outJson += "\"speedTx\":" + String(stats.speedTxBps) + ",";
    outJson += "\"packetsPerSec\":" + String(stats.packetsPerSec) + ",";
    outJson += "\"pingMs\":" + String(stats.upstreamLatencyMs) + ",";
    outJson += "\"clientCount\":" + String(clientCount);
    outJson += "}";
}

void DnsEngine::getLogsJson(String& outJson) const {
    outJson = "[";
    size_t count = 0;
    for (size_t i = 0; i < logCount; i++) {
        size_t idx = (logIndex + MAX_LOGS - 1 - i) % MAX_LOGS;
        if (queryLogs[idx].domain.length() == 0) continue;
        if (count > 0) outJson += ",";
        outJson += "{";
        outJson += "\"ip\":\"" + queryLogs[idx].clientIp + "\",";
        outJson += "\"mac\":\"" + queryLogs[idx].clientMac + "\",";
        outJson += "\"domain\":\"" + queryLogs[idx].domain + "\",";
        outJson += "\"qtype\":" + String(queryLogs[idx].qtype) + ",";
        outJson += "\"verdict\":" + String(queryLogs[idx].verdict) + ",";
        outJson += "\"ms\":" + String(queryLogs[idx].durationMs) + ",";
        outJson += "\"age\":" + String((millis() - queryLogs[idx].timestamp) / 1000);
        outJson += "}";
        count++;
    }
    outJson += "]";
}

void DnsEngine::getClientsJson(String& outJson) const {
    outJson = "[";
    for (size_t i = 0; i < clientCount; i++) {
        if (i > 0) outJson += ",";
        float pct = (clients[i].totalQueries > 0) ? 
                    ((float)clients[i].blockedQueries / clients[i].totalQueries * 100.0f) : 0.0f;
        outJson += "{";
        outJson += "\"ip\":\"" + clients[i].ip + "\",";
        outJson += "\"mac\":\"" + (clients[i].mac.length() > 0 ? clients[i].mac : "--") + "\",";
        outJson += "\"total\":" + String(clients[i].totalQueries) + ",";
        outJson += "\"blocked\":" + String(clients[i].blockedQueries) + ",";
        outJson += "\"bytes\":" + String((uint32_t)clients[i].totalBytes) + ",";
        outJson += "\"rate\":" + String(pct, 1) + ",";
        outJson += "\"seen\":" + String((millis() - clients[i].lastSeen) / 1000) + ",";
        outJson += "\"isDiscovered\":" + String(clients[i].isDiscovered ? "true" : "false");
        outJson += "}";
    }
    outJson += "]";
}

void DnsEngine::getTopDomainsJson(String& outJson) const {
    outJson = "{\"allowed\":[";
    for (size_t i = 0; i < topAllowedCount; i++) {
        if (i > 0) outJson += ",";
        outJson += "{\"domain\":\"" + topAllowed[i].domain + "\",\"count\":" + String(topAllowed[i].count) + "}";
    }
    outJson += "],\"blocked\":[";
    for (size_t i = 0; i < topBlockedCount; i++) {
        if (i > 0) outJson += ",";
        outJson += "{\"domain\":\"" + topBlocked[i].domain + "\",\"count\":" + String(topBlocked[i].count) + "}";
    }
    outJson += "]}";
}

void DnsEngine::getTelemetryJson(String& outJson) const {
    outJson.reserve(6144);
    outJson = "{\"stats\":";
    String statsPart;
    getStatsJson(statsPart);
    outJson += statsPart;

    outJson += ",\"logs\":";
    String logsPart;
    getLogsJson(logsPart);
    outJson += logsPart;

    outJson += ",\"clients\":";
    String clientsPart;
    getClientsJson(clientsPart);
    outJson += clientsPart;

    outJson += ",\"topDomains\":";
    String topPart;
    getTopDomainsJson(topPart);
    outJson += topPart;

    outJson += "}";
}
