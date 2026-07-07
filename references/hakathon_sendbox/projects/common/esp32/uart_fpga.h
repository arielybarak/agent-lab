// uart_fpga.h -- ESP32<->FPGA UART bridge (newline-terminated ASCII).
// Wraps HardwareSerial(2) on the kit's FPGA pins (GPIO16/17, 9600 8N1).
//
// Usage:
//   UartFpga fpga;
//   void setup() { fpga.begin(); }
//   void loop() {
//     String line;
//     if (fpga.readLine(line)) { /* got a full line from the FPGA */ }
//     fpga.sendLine("HELLO");
//   }
//
// readLine() is non-blocking: call it every loop(); it returns true once per
// completed line. '\r' is ignored so "HH:MM:SS\r\n" works.
#pragma once
#include <Arduino.h>
#include "pin_config.h"

class UartFpga {
public:
    explicit UartFpga(int uartNum = 2) : _serial(uartNum) {}

    void begin(uint32_t baud = FPGA_BAUD) {
        _serial.begin(baud, SERIAL_8N1, PIN_FPGA_RX, PIN_FPGA_TX);
        _buf.reserve(_maxLen + 1);
    }

    // Send a string followed by '\n'.
    void sendLine(const String& s) { _serial.print(s); _serial.print('\n'); }
    void sendLine(const char* s)   { _serial.print(s); _serial.print('\n'); }

    // printf-style send (no automatic newline -- add \n in the format).
    void printf(const char* fmt, ...) {
        char tmp[64];
        va_list ap; va_start(ap, fmt);
        vsnprintf(tmp, sizeof(tmp), fmt, ap);
        va_end(ap);
        _serial.print(tmp);
    }

    // Non-blocking. Returns true once when a full '\n'-terminated line is ready.
    bool readLine(String& out) {
        while (_serial.available()) {
            char c = (char)_serial.read();
            if (c == '\n') {
                out = _buf;
                _buf = "";
                return true;
            } else if (c != '\r' && _buf.length() < _maxLen) {
                _buf += c;
            }
        }
        return false;
    }

    HardwareSerial& raw() { return _serial; }

private:
    HardwareSerial _serial;
    String         _buf;
    const uint16_t _maxLen = 32;
};
