// servo.h -- SG90-style servo on a GPIO via ESP32 LEDC PWM (50 Hz, 16-bit).
// 0deg = 0.5 ms pulse, 180deg = 2.5 ms. Matches the alive_test angleToDuty().
// Note: ledcAttach/ledcWrite signature here is Arduino-ESP32 core 3.x.
//
// Usage:
//   Servo sv(PIN_SERVO);
//   void setup() { sv.begin(); sv.write(90); }
//   void loop()  { sv.write(pot.mapTo(0,180)); }
#pragma once
#include <Arduino.h>
#include "pin_config.h"

class Servo {
public:
    explicit Servo(uint8_t pin = PIN_SERVO) : _pin(pin) {}

    void begin() {
        ledcAttach(_pin, 50, 16);   // 50 Hz, 16-bit resolution
        write(90);                  // center
    }

    // Move to angle in [0,180] degrees.
    void write(int deg) {
        if (deg < 0)   deg = 0;
        if (deg > 180) deg = 180;
        uint32_t us   = 500 + ((uint32_t)deg * 2000 / 180);   // 500..2500 us
        uint32_t duty = (uint32_t)((uint64_t)us * 65536UL / 20000UL);
        ledcWrite(_pin, duty);
        _angle = deg;
    }

    int angle() const { return _angle; }

private:
    uint8_t _pin;
    int     _angle = 90;
};
