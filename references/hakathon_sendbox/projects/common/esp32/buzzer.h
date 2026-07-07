// buzzer.h -- piezo buzzer on a GPIO via Arduino tone()/noTone().
// Presets match the alive_test demo. beep() is non-blocking: call update() each
// loop() and it auto-stops after the duration.
//
// Usage:
//   Buzzer buz(PIN_BUZZER);
//   void loop() { buz.update(); if (sw.pressed()) buz.beep(Buzzer::MID, 120); }
#pragma once
#include <Arduino.h>
#include "pin_config.h"

class Buzzer {
public:
    enum Tone { LOW_TONE = 800, MID = 1500, HIGH_TONE = 2000 };

    explicit Buzzer(uint8_t pin = PIN_BUZZER) : _pin(pin) {}
    void begin() { pinMode(_pin, OUTPUT); }

    void on(int freq)  { tone(_pin, freq); _on = true; }
    void off()         { if (_on) { noTone(_pin); _on = false; } }

    // Non-blocking timed beep; auto-stops in update() after ms.
    void beep(int freq, unsigned long ms) {
        tone(_pin, freq);
        _on = true;
        _until = millis() + ms;
        _timed = true;
    }

    void update() {
        if (_timed && _on && (long)(millis() - _until) >= 0) {
            off();
            _timed = false;
        }
    }

private:
    uint8_t       _pin;
    bool          _on = false, _timed = false;
    unsigned long _until = 0;
};
