# Hardware conventions — CrashTech VLSI 2026

DE10-Lite FPGA (Intel MAX 10) + ESP32 DevKit over UART. These rules are authoritative for all RTL,
firmware, and wiring. (Adapted from the TechCrash2026 Copilot instructions.)

> Authoritative board fallback for anything not covered here (timing, connectors, SDRAM, ADC,
> accelerometer): `docs/manual/DE10-Lite_User_Manual.pdf` (kept local, gitignored).

## Host split (important)

- **Edit and run build scripts in WSL/Linux.**
- **FPGA programming runs from Windows PowerShell** — `quartus_pgm.exe` can't handle WSL/UNC paths.
- **ESP32 build + upload run from WSL**, after bridging the USB serial device with
  `usbipd attach --wsl` → `/dev/ttyUSB0` (load `cp210x`, `chmod 666`). See `SETUP_QUICKSTART.md`.

## FPGA ↔ ESP32 communication

- **Use the Arduino header** on the DE10-Lite, **NOT** the JP1 40-pin GPIO header.
- FPGA RX from ESP32: `ARDUINO_IO[0]` (PIN_AB5).
- FPGA TX to ESP32: `ARDUINO_IO[1]` (PIN_AB6).
- ESP32 TX: GPIO 16; ESP32 RX: GPIO 17.
- UART: **9600 baud, 8N1, 3.3V** logic.
- All unused `ARDUINO_IO` pins must be high-Z (`1'bz`).
- GND: tie ESP32 GND to an Arduino-header GND pin.

## Shared pin contract

- ESP32: `projects/common/esp32/pin_config.h` (include with the correct relative path from each
  project's `src/`).
- FPGA: `projects/common/fpga/pins.svh` (mirror of the same UART map — keep both in sync to avoid
  pin drift).

## RTL top-module pattern

```systemverilog
module project_top (
    input           MAX10_CLK1_50,
    input   [9:0]   SW,
    input   [1:0]   KEY,
    output  [9:0]   LEDR,
    output  [7:0]   HEX0, HEX1, HEX2, HEX3, HEX4, HEX5,
    inout   [15:0]  ARDUINO_IO,
    inout           ARDUINO_RESET_N
);
```

## Toolchains

- **FPGA:** Quartus Prime Lite 17.1 (`C:\intelFPGA_lite\17.1\`).
  - Compile: `quartus_sh --flow compile <project_name>`.
  - Program: `quartus_pgm -c "USB-Blaster [USB-0]" -m JTAG -o "P;output_files/<project>.sof"`.
- **ESP32:** PlatformIO. Build `pio run`, upload `pio run -t upload`, monitor `pio device monitor`
  — from the project's `esp32/` folder. PlatformIO auto-detects the port and owns the toolchain.

## Project structure

Each challenge/demo has parallel `esp32/` and `fpga/` folders:
- `esp32/platformio.ini` + `esp32/src/main.cpp`
- `fpga/<project>.qpf` + `fpga/<project>.qsf` + `fpga/src/<top>.sv`

## Debugging a dead UART link

**Before changing any code**, follow the 7-step protocol in
[`debug-lessons.md`](debug-lessons.md) — hard-won lessons from live sessions. Top hazards:

- **ESP32 boot loop** — `PIN_SW_2 = GPIO0` is the boot strap; held LOW at power-on → ROM download
  mode, app never runs (serial spews `rst:ets...`). Release SW2, press EN.
- **Silkscreen `TXD`/`RXD` ≠ UART2** — those are GPIO1/3 (USB debug, 115200). FPGA UART2 is
  GPIO16/17. Count pins physically.
- **Monitor resets the ESP on close** — CP2102 RTS/DTR pulse EN/GPIO0. Templates already set
  `monitor_rts = 0` / `monitor_dtr = 0`; keep them.
- **Stale `.sof`** — always recompile before debugging IO; a committed bitstream can predate the
  `.sv`.
- **Both directions dead** → check the common **GND** first.
- Loopback tests: bridge `ARDUINO_IO[0]↔[1]` (FPGA) or `GPIO16↔GPIO17` (ESP32) to isolate which
  side is broken.

## What NOT to do

- Do NOT use JP1 GPIO pins — always the Arduino header (`ARDUINO_IO[0..15]`).
- Do NOT use `.venv/` — the Python venv is `env/`.
- Do NOT hardcode COM ports — PlatformIO auto-detects.
- Do NOT install the ESP32 toolchain manually — PlatformIO handles it.
