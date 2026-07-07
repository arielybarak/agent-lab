# CrashTech 2026 Hackathon — Claude instructions

24-hour hardware hackathon. **DE10-Lite FPGA** (Intel MAX 10, Quartus, SystemVerilog) +
**ESP32 DevKit** (PlatformIO, C++), talking over UART; some challenges add **KiCad** PCB work.
Goal: solve as many challenges as possible. Budget is tight (Claude Pro) — **token frugality is a
first-class constraint.**

## Budget rules (read first)

- **Division of labor.** Use **GitHub Copilot** (separate budget) for bulk/boilerplate generation
  and repetitive edits. Reserve **Claude** for hard reasoning: tricky RTL/timing, debugging,
  integration. Don't spend Claude tokens on rote scaffolding.
- **One skill at a time.** Invoke a single domain skill for the task at hand; don't pre-load
  several. The big BKM skills are large — they cost only when actually invoked.
- **Let Bash do rote work.** Scaffold a challenge by copying the template and build with `just`
  recipes — these cost ~zero model tokens. Don't hand-generate boilerplate.
- **No sub-agent fan-out.** Spawning agents re-derives full context and burns budget fastest.

## How to work a challenge

1. Use the **`challenge-intake`** skill — it routes the prompt to the right BKM skill and gives the
   per-challenge steps.
2. Scaffold: `cp -r challenges/_template/<fpga|esp32> challenges/<name>/<...>` (a compiling start).
3. Plan with `writing-plans` if non-trivial; build with the `Justfile` recipes.
4. **Program/flash on the Windows host**, not WSL (see hardware rules below).
5. Verify on hardware; log status in `CHALLENGES.md`.

## Reusable bricks (`projects/common/`) — assemble, don't rewrite

A pre-built, tested library exists. **Check it before writing any module.** Catalog +
include-line conventions: `projects/common/README.md`.
- FPGA (`projects/common/fpga/`): UART (`uart_rx/uart_tx/uart_line_rx`), display
  (`seven_segment`, `hex_display`), timing (`clock_divider`, `tick_gen`), input
  (`button_debounce`, `sync_2ff`, `edge_detect`), counters/parse (`bin2bcd`, `bcd_counter`,
  `ascii_num_parser`), VGA/game (`vga_sync`, `vga_test_pattern`, `obj_rect`, `sprite`,
  `compositor`, `frame_move`, `periphery_control`), heavy (`pipeline_accumulator`, `alu`,
  `packet_decoder`). Each has a `sim/<name>_tb` → `just sim <name>`.
- IP-bound (generate in Quartus, see the matching `*.README.md`): `pll25`, `analog_input` (ADC),
  `hack_cpu`/`mem_arbiter`, `text_screen`, `lcd_ctrl`.
- ESP32 (`projects/common/esp32/`): `uart_fpga`, `oled`, `button`, `analog`, `buzzer`, `servo`,
  `led`, `wifi_ntp`, `packet` (+ `pin_config`).
- Ready-to-copy bases: `challenges/starters/{uart_echo,clock,vga_game}`.

## Domain knowledge — BKM skills (`.claude/skills/`)

Invoke the one that matches the task:
- `de10lite-board-and-build` — board bring-up, Quartus toolchain, full pin map, FPGA cookbook, IP.
- `de10lite-vga-graphics` — VGA 640×480, sprites, compositing, text screen.
- `de10lite-addon-peripherals` — ADC joystick/buttons/wheel + LCD via Arduino header.
- `esp32-firmware` — PlatformIO, pin map, LVGL, UART bridge, hard-won BKMs.
- `kicad-board-design` — schematic → ERC → PCB → DRC → Gerber.

Discipline skills: `systematic-debugging`, `writing-plans`, `executing-plans`,
`verification-before-completion`. Subagent `code-reviewer` available but use sparingly (token cost).

## Hardware conventions

**Authoritative:** `.claude/instructions/hardware/README.md` — read it before any RTL or wiring.
**When a UART link is dead, read `.claude/instructions/hardware/debug-lessons.md` first** (7-step
protocol: boot-loop strap, silkscreen-TXD trap, monitor RTS reset, stale `.sof`, GND, loopbacks).
Key points: UART on the **Arduino header** (`ARDUINO_IO[0]/[1]`, **never** JP1 GPIO), 9600 8N1
3.3V, unused `ARDUINO_IO` pins held `1'bz`; shared pin contract in
`projects/common/{esp32/pin_config.h, fpga/pins.svh}`. **Host split: edit/build-script in WSL;
FPGA programming runs from Windows PowerShell (Quartus can't use WSL paths); ESP32 build + upload
run from WSL after `usbipd attach` → `/dev/ttyUSB0`.**

## Layout

```
challenges/<name>/fpga/   <project>.qpf + .qsf + src/<top>.sv
challenges/<name>/esp32/  platformio.ini + src/main.cpp
challenges/_template/     compiling skeleton to copy from
projects/common/          shared pin contract (esp32/, fpga/)
demos/                    smoke / reference demos
```

DDD layering and mandatory TDD from the generic instruction tree **do not apply** to hardware work
here — they're left in `.claude/instructions/general/` for reference only.

## Build & MCP

- `Justfile`: `just fpga-build <dir>`, `just fpga-prog`, `just esp32-flash <dir>`,
  `just esp32-monitor`. Quick refs in `SETUP_QUICKSTART.md`.
- MCP `context7` (library/datasheet docs) is preconfigured in `.mcp.json`. One-time:
  `cp .env.example .env` → `just mcp` → run `claude` and approve the server.
