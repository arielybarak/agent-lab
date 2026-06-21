// uart_echo starter -- ESP32 side.
// Sends a counter line once per second; prints whatever the FPGA echoes back.
// If wiring + baud are right, USB serial shows each line returning intact.
#include <Arduino.h>
#include "uart_fpga.h"

UartFpga fpga;
unsigned long last = 0;
int n = 0;

void setup() {
    Serial.begin(115200);
    fpga.begin();          // 9600 8N1 on GPIO16/17
    Serial.println("uart_echo starter: send + listen");
}

void loop() {
    String line;
    if (fpga.readLine(line)) Serial.printf("echo <- %s\n", line.c_str());

    unsigned long now = millis();
    if (now - last >= 1000) {
        last = now;
        char msg[16];
        snprintf(msg, sizeof(msg), "PING%d", n++);
        fpga.sendLine(msg);
        Serial.printf("sent -> %s\n", msg);
    }
}
