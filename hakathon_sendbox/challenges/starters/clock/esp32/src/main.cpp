// clock starter -- ESP32 side.
// Connect WiFi, sync NTP, then stream "HH:MM:SS\n" to the FPGA once per second.
// Set your WiFi creds below before flashing.
#include <Arduino.h>
#include "wifi_ntp.h"
#include "uart_fpga.h"

const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASS = "YOUR_PASS";

WifiNtp   clk;
UartFpga  fpga;
unsigned long last = 0;

void setup() {
    Serial.begin(115200);
    fpga.begin();
    if (!clk.connect(WIFI_SSID, WIFI_PASS)) { Serial.println("WiFi failed"); }
    if (!clk.syncTime())                    { Serial.println("NTP failed");  }
    Serial.println("clock starter: streaming HH:MM:SS");
}

void loop() {
    unsigned long now = millis();
    if (now - last < 1000) return;
    last = now;

    char buf[9];
    if (clk.getString(buf)) {
        fpga.sendLine(buf);     // "HH:MM:SS\n"
        Serial.println(buf);
    }
}
