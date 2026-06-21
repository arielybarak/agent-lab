// analog.h -- ADC reader with optional smoothing + handy conversions.
// Default pin is the kit's analog input (GPIO34, input-only, ADC1, WiFi-safe).
//
// Usage:
//   Analog pot;                 // or Analog pot(PIN_ANALOG_IN, 0.2f);
//   void loop() {
//     pot.update();
//     int pct = pot.percent();  // 0..100
//     float v = pot.volts();    // 0..3.3
//   }
#pragma once
#include <Arduino.h>
#include "pin_config.h"

class Analog {
public:
    // smooth = EMA factor in (0,1]; 1.0 = no smoothing, lower = smoother.
    explicit Analog(uint8_t pin = PIN_ANALOG_IN, float smooth = 0.3f)
        : _pin(pin), _alpha(smooth) {}

    // Sample once; applies exponential smoothing.
    int update() {
        int raw = analogRead(_pin);
        _ema = (_init) ? (_alpha * raw + (1.0f - _alpha) * _ema) : (_init = true, (float)raw);
        return (int)_ema;
    }

    int   raw()     { return analogRead(_pin); }      // instantaneous, unsmoothed
    int   value()   const { return (int)_ema; }        // last smoothed value
    float volts()   const { return _ema * 3.3f / 4095.0f; }
    int   percent() const { return (int)(_ema * 100.0f / 4095.0f + 0.5f); }
    // Map smoothed value into [outMin, outMax].
    int   mapTo(int outMin, int outMax) const {
        return outMin + (int)((long)(int)_ema * (outMax - outMin) / 4095);
    }

private:
    uint8_t _pin;
    float   _alpha;
    float   _ema  = 0.0f;
    bool    _init = false;
};
