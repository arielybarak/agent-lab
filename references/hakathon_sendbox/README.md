# CrashTech 2026 Hackathon

24-hour hardware hackathon workspace: **DE10-Lite FPGA** (Quartus / SystemVerilog) + **ESP32**
(PlatformIO / C++), talking over UART; some challenges add **KiCad** PCB work. Goal: solve as many
challenges as possible — fast, and on a tight Claude budget.

## What's here

```
projects/common/        reusable "lego brick" library (pre-built + tested)
  fpga/                 SystemVerilog modules (UART, 7-seg, VGA, sprites, ...) + sim/ testbenches
  esp32/                C++ header utilities (uart_fpga, oled, button, analog, servo, ...)
challenges/             one folder per challenge (fpga/ + esp32/)
  _template/            compiling skeleton to copy for a new challenge
  starters/             ready-to-run bases: uart_echo, clock, vga_game
demos/                  reference demos (alive_test, internet_clock)
.claude/                agent workspace: BKM skills, hardware instructions, settings
```

## Start a challenge

1. Open Claude Code here and invoke the **`challenge-intake`** skill (routes the prompt to the
   right BKM skill and scaffolds the folder).
2. Or by hand: `just new-challenge <name>` → edit `challenges/<name>/{fpga,esp32}/`.
3. Pull bricks instead of rewriting them — see `projects/common/README.md` for the catalog and the
   `.qsf` / `platformio.ini` include lines.

## Build & flash

`Justfile` recipes (details + host split in `SETUP_QUICKSTART.md`):
- `just fpga-build <dir> <project>` · `just fpga-prog <dir> <project>` (program from Windows PowerShell)
- `just esp32-build <dir>` · `just esp32-flash <dir>` · `just esp32-monitor` (from WSL via `usbipd`)
- `just sim <name>` — run a brick's ModelSim testbench (e.g. `just sim uart_loopback`)

## Key docs

- **[CLAUDE.md](CLAUDE.md)** — conventions + budget rules any AI assistant must follow.
- **[projects/common/README.md](projects/common/README.md)** — the brick catalog + how to use it.
- **[SETUP_QUICKSTART.md](SETUP_QUICKSTART.md)** — toolchain quick-ref (FPGA program, ESP32 flash, wiring).
- **[CHALLENGES.md](CHALLENGES.md)** — challenge status board + "bricks ready" checklist.
- **`.claude/instructions/hardware/README.md`** — UART/pin/host-split rules (read before any RTL).

## Environment

- Run network setup before the event: `curl -LsSf https://astral.sh/uv/install.sh | sh`, install
  PlatformIO + `just`, generate any Quartus IP (`pll25`, ADC).
- MCP: `cp .env.example .env` → `just mcp` → run `claude` and approve `.mcp.json` (context7).

## Maintainer

Barak Ariely <barak.ariely@gmail.com>
