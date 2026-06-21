# clock starter

NTP clock. ESP32 gets internet time, streams "HH:MM:SS\n"; FPGA parses + shows it
on HEX5..HEX0 (HH MM SS). Rebuild of the internet_clock demo on shared bricks.

Bricks: `uart_rx`, `ascii_num_parser`, `hex_display` (FPGA) · `wifi_ntp.h`,
`uart_fpga.h` (ESP32).

## Run
- Edit `esp32/src/main.cpp` → set `WIFI_SSID` / `WIFI_PASS`.
- FPGA: `fpga/clock.qsf` → compile → program. Reset = SW[9].
- ESP32: `just esp32-build challenges/starters/clock/esp32` → flash.
- Wiring: GPIO16→ARDUINO_IO[0], GND. 9600 8N1.
- Expect: HEX shows live time; shows `00:00:00` until first NTP line arrives.
