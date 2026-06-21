// button.h -- debounced push-button / switch on an active-low INPUT_PULLUP pin.
// Reads LOW when pressed (matches the kit's switches wired pin->GND).
//
// Usage:
//   Button sw1(PIN_SW_1);
//   void setup() { sw1.begin(); }
//   void loop() {
//     sw1.update();
//     if (sw1.pressed())  { /* edge: just pressed  */ }
//     if (sw1.released()) { /* edge: just released */ }
//     if (sw1.held())     { /* level: currently down */ }
//   }
#pragma once
#include <Arduino.h>

class Button {
public:
    explicit Button(uint8_t pin, unsigned long debounceMs = 50)
        : _pin(pin), _debounce(debounceMs) {}

    void begin() { pinMode(_pin, INPUT_PULLUP); }

    // Call once per loop(). Latches edges for pressed()/released().
    void update() {
        bool raw = (digitalRead(_pin) == LOW);
        unsigned long now = millis();
        if (raw != _last) { _changed = now; _last = raw; }
        _pressedEdge = _releasedEdge = false;
        if ((now - _changed) > _debounce && raw != _stable) {
            _stable = raw;
            if (raw) _pressedEdge = true; else _releasedEdge = true;
        }
    }

    bool held()     const { return _stable; }       // current debounced level
    bool pressed()  const { return _pressedEdge; }   // 1-shot on press
    bool released() const { return _releasedEdge; }  // 1-shot on release

private:
    uint8_t       _pin;
    unsigned long _debounce;
    bool          _last = false, _stable = false;
    bool          _pressedEdge = false, _releasedEdge = false;
    unsigned long _changed = 0;
};
