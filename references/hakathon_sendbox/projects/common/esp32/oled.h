// oled.h -- thin helper over Adafruit_SSD1306 for the kit's 128x64 I2C OLED.
// Needs libs in platformio.ini:
//   adafruit/Adafruit SSD1306@^2.5.7
//   adafruit/Adafruit GFX Library@^1.11.5
//
// Usage:
//   Oled oled;
//   void setup() { oled.begin(); }
//   void loop() {
//     oled.start("STATUS");
//     oled.kv("SW1", sw1 ? "ON" : "off");
//     oled.bar("Pot", adcPercent, 100);
//     oled.show();
//   }
#pragma once
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "pin_config.h"

class Oled {
public:
    Oled() : _d(OLED_WIDTH, OLED_HEIGHT, &Wire, -1) {}

    bool begin() {
        Wire.begin(PIN_OLED_SDA, PIN_OLED_SCL);
        _ok = _d.begin(SSD1306_SWITCHCAPVCC, OLED_I2C_ADDR);
        return _ok;
    }
    bool ok() const { return _ok; }

    // Begin a frame with an underlined title; resets the text cursor below it.
    void start(const char* title) {
        if (!_ok) return;
        _d.clearDisplay();
        _d.setTextColor(SSD1306_WHITE);
        _d.setTextSize(1);
        _d.setCursor(0, 0);
        _d.println(title);
        _d.drawFastHLine(0, 10, OLED_WIDTH, SSD1306_WHITE);
        _y = 13;
    }

    void line(const char* s)              { if (!_ok) return; _d.setCursor(0, _y); _d.print(s); _y += 9; }
    void kv(const char* k, const char* v) { if (!_ok) return; _d.setCursor(0, _y); _d.printf("%s: %s", k, v); _y += 9; }
    void kv(const char* k, int v)         { if (!_ok) return; _d.setCursor(0, _y); _d.printf("%s: %d", k, v); _y += 9; }

    // Labeled progress bar (value/maxv).
    void bar(const char* label, int value, int maxv) {
        if (!_ok) return;
        _d.setCursor(0, _y); _d.printf("%s", label); _y += 9;
        int top = _y;
        _d.drawRect(0, top, OLED_WIDTH, 7, SSD1306_WHITE);
        int w = (maxv > 0) ? (int)((long)value * (OLED_WIDTH - 2) / maxv) : 0;
        if (w < 0) w = 0; if (w > OLED_WIDTH - 2) w = OLED_WIDTH - 2;
        _d.fillRect(1, top + 1, w, 5, SSD1306_WHITE);
        _y += 9;
    }

    void show() { if (_ok) _d.display(); }
    Adafruit_SSD1306& raw() { return _d; }

private:
    Adafruit_SSD1306 _d;
    bool _ok = false;
    int  _y  = 13;
};
