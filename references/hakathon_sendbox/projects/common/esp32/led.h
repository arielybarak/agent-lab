// led.h -- simple LED helpers. `Led` is a single GPIO with non-blocking blink;
// `LedChaser` cycles a row of LEDs (the alive_test chasing pattern).
//
// Usage:
//   Led led(PIN_LED_1);
//   const int row[] = {PIN_LED_1, PIN_LED_2, PIN_LED_3};
//   LedChaser chaser(row, 3, 150);
//   void setup() { led.begin(); chaser.begin(); }
//   void loop()  { led.update(); chaser.update(); }
#pragma once
#include <Arduino.h>

class Led {
public:
    explicit Led(uint8_t pin) : _pin(pin) {}
    void begin() { pinMode(_pin, OUTPUT); set(false); }

    void set(bool on) { _on = on; digitalWrite(_pin, on ? HIGH : LOW); }
    void on()         { set(true); }
    void off()        { set(false); }
    void toggle()     { set(!_on); }

    // Non-blocking blink at `ms` half-period; call update() each loop().
    void blink(unsigned long ms) { _period = ms; _blinking = true; }
    void stop()                  { _blinking = false; }

    void update() {
        if (!_blinking) return;
        unsigned long now = millis();
        if (now - _last >= _period) { _last = now; toggle(); }
    }

private:
    uint8_t       _pin;
    bool          _on = false, _blinking = false;
    unsigned long _period = 250, _last = 0;
};

class LedChaser {
public:
    LedChaser(const int* pins, int n, unsigned long stepMs)
        : _pins(pins), _n(n), _step(stepMs) {}

    void begin() { for (int i = 0; i < _n; i++) pinMode(_pins[i], OUTPUT); }

    void update() {
        unsigned long now = millis();
        if (now - _last < _step) return;
        _last = now;
        for (int i = 0; i < _n; i++) digitalWrite(_pins[i], LOW);
        digitalWrite(_pins[_idx], HIGH);
        _idx = (_idx + 1) % _n;
    }

private:
    const int*    _pins;
    int           _n, _idx = 0;
    unsigned long _step, _last = 0;
};
