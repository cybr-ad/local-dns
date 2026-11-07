#ifndef DNS_ENGINE_H
#define DNS_ENGINE_H

#include <Arduino.h>
#include <WiFiUdp.h>
#include <IPAddress.h>
#include <vector>
#include "config_mgr.h"
#include "blocklist.h"

enum QueryVerdict {
    VERDICT_ALLOWED = 0,
    VERDICT_BLOCKED = 1,
    VERDICT_CACHED = 2
};

struct DnsStats {
    uint32_t totalQueries = 0;
    uint32_t blockedQueries = 0;
    uint32_t cachedQueries = 0;
    uint32_t forwardQueries = 0;
    uint32_t startTime = 0;
    
    // Throughput & Packet counters
    uint64_t totalBytesRx = 0;
    uint64_t totalBytesTx = 0;
    uint32_t totalPacketsRx = 0;
    uint32_t totalPacketsTx = 0;
    uint32_t speedRxBps = 0; // Bytes per second
    uint32_t speedTxBps = 0; // Bytes per second
    uint32_t packetsPerSec = 0;
    uint16_t upstreamLatencyMs = 11; // Last measured upstream DNS latency
};

struct QueryLogEntry {
    String clientIp;
    String clientMac;
    String domain;
    uint16_t qtype;
    uint8_t verdict; // 0=Allowed, 1=Blocked, 2=Cached
    uint16_t durationMs;
    uint32_t timestamp; // millis()
};

struct PendingQuery {
    bool active = false;
    uint16_t upstreamId = 0;
    uint16_t origId = 0;
    IPAddress clientIp;
    String clientMac;
    uint16_t clientPort = 0;
    String domain;
    uint16_t qtype = 1;
    uint32_t sendTime = 0;
    bool retriedSecondary = false;
};

struct CacheEntry {
    bool valid = false;
    String domain;
    uint16_t qtype = 1;
    uint32_t expireAt = 0; // millis()
    uint16_t dataLen = 0;
    uint8_t data[512];
};

struct ClientInfo {
    String ip;
    String mac;
    String hostname;
    uint32_t totalQueries = 0;
    uint32_t blockedQueries = 0;
    uint64_t totalBytes = 0;
    uint32_t lastSeen = 0;
    bool isDiscovered = false;
};

struct DomainRank {
    String domain;
    uint32_t count = 0;
};

class DnsEngine {
private:
    WiFiUDP clientUdp;
    WiFiUDP upstreamUdp;
    DnsStats stats;
    
    static const size_t MAX_PENDING = 64;
    PendingQuery pendingQueries[MAX_PENDING];
    uint16_t nextUpstreamId = 1000;

    static const size_t MAX_LOGS = 60;
    QueryLogEntry queryLogs[MAX_LOGS];
    size_t logIndex = 0;
    size_t logCount = 0;

    static const size_t MAX_CACHE = 64;
    CacheEntry cache[MAX_CACHE];
    size_t cacheNextIdx = 0;

    // Local client monitor (up to 40 clients)
    static const size_t MAX_CLIENTS = 40;
    ClientInfo clients[MAX_CLIENTS];
    size_t clientCount = 0;

    // Top domains
    static const size_t MAX_TOP = 15;
    DomainRank topAllowed[MAX_TOP];
    size_t topAllowedCount = 0;
    DomainRank topBlocked[MAX_TOP];
    size_t topBlockedCount = 0;

    // Throughput timer & smoothing
    uint32_t lastSpeedCalc = 0;
    uint32_t windowBytesRx = 0;
    uint32_t windowBytesTx = 0;
    uint32_t windowPackets = 0;

    // Background ARP Scanner
    uint32_t lastArpScan = 0;
    uint8_t nextScanHost = 70;

    bool parseDnsQuestion(const uint8_t* buf, size_t len, size_t& offset, String& outDomain, uint16_t& outQtype);
    void sendSinkholeResponse(const uint8_t* queryBuf, size_t queryLen, size_t questionEnd, const IPAddress& clientIp, uint16_t clientPort, uint16_t id, uint16_t qtype);
    void logQuery(const IPAddress& clientIp, const String& clientMac, const String& domain, uint16_t qtype, QueryVerdict verdict, uint16_t durationMs);

    int findCache(const String& domain, uint16_t qtype);
    void addCache(const String& domain, uint16_t qtype, uint32_t ttlSec, const uint8_t* respBuf, size_t respLen);

    String resolveMac(const IPAddress& clientIp);
    void recordClientQuery(const IPAddress& clientIp, bool blocked, size_t bytes);
    void recordDomainRank(const String& domain, bool blocked);

    void scanNextLanHost();
    void harvestArpTable();
    void recordDiscoveredDevice(const IPAddress& ip, const String& mac);

public:
    DnsEngine();
    bool begin();
    void handle();

    const DnsStats& getStats() const { return stats; }
    void resetStats();
    void flushCache();
    void triggerFullLanScan();
    
    // JSON generation
    void getTelemetryJson(String& outJson) const;
    void getLogsJson(String& outJson) const;
    void getStatsJson(String& outJson) const;
    void getClientsJson(String& outJson) const;
    void getTopDomainsJson(String& outJson) const;
    
    // Upstream benchmark
    uint32_t benchmarkDns(const String& serverIp);
};

extern DnsEngine dnsEngine;

#endif // DNS_ENGINE_H
