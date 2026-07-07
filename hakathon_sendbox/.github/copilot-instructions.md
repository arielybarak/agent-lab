# Copilot Instructions — CrashTech 2026 Hackathon

This project is **Claude-canonical**; the full source of truth is `CLAUDE.md` and the instruction
tree in `.claude/`. Skills live in `.claude/skills/` (domain BKM + `challenge-intake`). Below are
the hardware conventions inlined so Copilot has them directly.

## Project overview

24h hackathon: **DE10-Lite FPGA** (Intel MAX 10, Quartus, SystemVerilog) + **ESP32 DevKit**
(PlatformIO, C++) over UART; some challenges add **KiCad** PCB work.

## Budget / division of labor

Use **Copilot for bulk and boilerplate generation and repetitive edits** — that's its job here.
Hard reasoning (tricky RTL/timing, debugging, integration) is handled in Claude Code. Don't fan out
to sub-agents.

## Workflow per challenge

Each challenge lives in `challenges/<name>/` with parallel `fpga/` and `esp32/` folders. Start from
the compiling skeleton: `cp -r challenges/_template/<fpga|esp32> challenges/<name>/<...>`. Build via
the `Justfile` recipes (`just fpga-build <dir>`, `just esp32-flash <dir>`). Track status in
`CHALLENGES.md`.

## FPGA ↔ ESP32 communication

- **Use the Arduino header** on the DE10-Lite, **NOT** JP1 GPIO.
- FPGA RX `ARDUINO_IO[0]` (PIN_AB5); FPGA TX `ARDUINO_IO[1]` (PIN_AB6).
- ESP32 TX GPIO16; ESP32 RX GPIO17. UART 9600 8N1, 3.3V.
- Unused `ARDUINO_IO` pins → high-Z (`1'bz`).
- Shared pins: `projects/common/esp32/pin_config.h` and `projects/common/fpga/pins.svh` (keep synced).

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

## Toolchains (host split)

- FPGA: Quartus Prime Lite 17.1. Compile `quartus_sh --flow compile <project>`; **program from
  Windows PowerShell** (`.exe` can't use WSL paths):
  `quartus_pgm -c "USB-Blaster [USB-0]" -m JTAG -o "P;output_files/<project>.sof"`.
- ESP32: PlatformIO, **from WSL** after `usbipd attach --wsl` → `/dev/ttyUSB0`. `pio run` /
  `pio run -t upload` / `pio device monitor` from the `esp32/` folder.

## Reusable brick library

A pre-built, tested "lego brick" library lives in `projects/common/` (FPGA SystemVerilog modules +
ESP32 C++ headers). **Reuse it before writing any module** — catalog: `projects/common/README.md`.
All tiers are built; `BRICKS_TODO.md` is superseded (kept only as a guide for the deferred IP-bound
modules: `hack_cpu`, `text_screen`, `lcd_ctrl`). New FPGA bricks get a testbench + `.do` in
`projects/common/fpga/sim/`.

## What NOT to do

- No JP1 GPIO pins (Arduino header only). No `.venv/` (use `env/`). Don't hardcode COM ports
  (PlatformIO auto-detects). Don't hand-install the ESP32 toolchain.
