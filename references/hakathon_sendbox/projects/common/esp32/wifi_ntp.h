// wifi_ntp.h -- connect to WiFi and get NTP time (from the internet_clock demo).
// Defaults are Israel time (UTC+2, +1h DST). Build a "HH:MM:SS" string to stream
// to the FPGA.
//
// Usage:
//   WifiNtp clock;
//   void setup() {
//     clock.connect("ssid", "pass");
//     clock.syncTime();              // or syncTime(gmtOffset, dstOffset)
//   }
//   void loop() {
//     char buf[9];
//     if (clock.getString(buf)) fpga.sendLine(buf);
//   }
#pragma once
#include <Arduino.h>
#include <WiFi.h>
#include <time.h>

class WifiNtp {
public:
    // Blocks until connected or timeoutMs elapses. Returns true if connected.
    bool connect(const char* ssid, const char* pass, unsigned long timeoutMs = 20000) {
        WiFi.begin(ssid, pass);
        unsigned long start = millis();
        while (WiFi.status() != WL_CONNECTED) {
            if (millis() - start > timeoutMs) return false;
            delay(250);
        }
        return true;
    }

    // Configure NTP and block until the first sync (or timeout).
    bool syncTime(long gmtOffsetSec = 2 * 3600, int dstOffsetSec = 3600,
                  const char* server = "pool.ntp.org", unsigned long timeoutMs = 15000) {
        configTime(gmtOffsetSec, dstOffsetSec, server);
        struct tm t;
        unsigned long start = millis();
        while (!getLocalTime(&t)) {
            if (millis() - start > timeoutMs) return false;
            delay(250);
        }
        return true;
    }

    // Fill h/m/s. Returns false if time isn't available.
    bool getTime(int& h, int& m, int& s) {
        struct tm t;
        if (!getLocalTime(&t)) return false;
        h = t.tm_hour; m = t.tm_min; s = t.tm_sec;
        return true;
    }

    // Fill an 8-char "HH:MM:SS" string (buf must be >= 9 bytes).
    bool getString(char* buf) {
        int h, m, s;
        if (!getTime(h, m, s)) return false;
        snprintf(buf, 9, "%02d:%02d:%02d", h, m, s);
        return true;
    }

    bool connected() const { return WiFi.status() == WL_CONNECTED; }
};
