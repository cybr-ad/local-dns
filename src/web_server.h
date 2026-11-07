#ifndef WEB_SERVER_H
#define WEB_SERVER_H

#include <Arduino.h>
#include <WebServer.h>

class WebServerManager {
private:
    WebServer server;

public:
    WebServerManager();
    void begin();
    void handle();
};

extern WebServerManager webServerMgr;

#endif // WEB_SERVER_H

