# uart_echo starter

Minimal both-sides ASCII round-trip. FPGA echoes every byte back; ESP32 sends a
counter line each second and prints the echo. Proves UART wiring + baud.

Bricks: `uart_rx`, `uart_tx` (FPGA) · `uart_fpga.h` (ESP32).

## Run
- FPGA: open `fpga/echo.qsf` in Quartus → compile → program (`just fpga-build`,
  then program on Windows; see `SETUP_QUICKSTART.md`).
- ESP32: `just esp32-build challenges/starters/uart_echo/esp32` → flash → monitor.
- Wiring: GPIO16→ARDUINO_IO[0], GPIO17←ARDUINO_IO[1], GND. 9600 8N1.
- Expect: monitor shows `sent -> PINGn` then `echo <- PINGn`. LEDR[7:0] = last byte.
