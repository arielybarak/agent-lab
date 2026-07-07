---
name: challenge-intake
description: Start here for any new TechCrash 2026 challenge. Routes the prompt to the right hardware BKM skill, scaffolds the challenge folder from the template, and runs the build/flash/verify loop — token-frugally.
---

# Challenge intake

The entry point for every new hackathon challenge. Keeps work fast and budget-cheap.

## Token discipline (do this every time)

- **Invoke ONE BKM skill** — only the one matching this challenge. Don't load several.
- **Hand boilerplate to Copilot** (separate budget). Use Claude for the hard parts: tricky RTL,
  timing, debugging, FPGA↔ESP32 integration.
- **Scaffold and build with Bash/`just`**, not by generating files in the model.

## 1. Read the prompt → route to a skill

| Challenge involves… | Invoke skill |
| --- | --- |
| Board bring-up, clocks, 7-seg, LEDs, switches, Quartus setup | `de10lite-board-and-build` |
| VGA output, sprites, graphics, text on screen | `de10lite-vga-graphics` |
| Joystick / buttons / wheel (ADC) or add-on LCD | `de10lite-addon-peripherals` |
| ESP32 firmware, WiFi, OLED, sensors, UART bridge | `esp32-firmware` |
| Designing/routing a PCB | `kicad-board-design` |

Most challenges are FPGA + ESP32 together — read the matching FPGA *and* `esp32-firmware` skills,
but one at a time, as you reach that side.

## 2. Scaffold (cheap)

```bash
mkdir -p challenges/<name>
cp -r challenges/_template/fpga  challenges/<name>/fpga    # if FPGA side
cp -r challenges/_template/esp32 challenges/<name>/esp32   # if ESP32 side
```

The template is a compiling alive-test: a valid DE10-Lite top module + working `platformio.ini`.
Rename the project files and edit from there — never start from blank.

**Reuse bricks — don't rewrite.** Before writing any module, check the pre-built library in
`projects/common/` (catalog: `projects/common/README.md`): UART, 7-seg/`hex_display`, debounce,
counters, ASCII parse, VGA sprite stack, plus ESP32 headers (`uart_fpga`, `oled`, `button`,
`analog`, `servo`, `buzzer`, `wifi_ntp`). Pull a brick via the `.qsf` `SV_FILE` line / `-I`
build flag. For common challenge shapes, copy a whole starter from `challenges/starters/`
(`uart_echo`, `clock`, `vga_game`).

## 3. Plan (only if non-trivial)

Use `writing-plans` for multi-part challenges. For small ones, skip straight to code.

## 4. Build (cheap — `just` recipes)

```bash
just fpga-build challenges/<name>/fpga
just esp32-flash challenges/<name>/esp32   # runs on the Windows host
just esp32-monitor
```

## 5. Conventions + verify

- Obey `.claude/instructions/hardware/README.md` (Arduino-header UART, top-module pattern,
  high-Z unused pins, host split for programming/flashing).
- Keep the shared pin contract in sync: `projects/common/{esp32/pin_config.h, fpga/pins.svh}`.
- Use `systematic-debugging` when something misbehaves. **For a dead UART link, read
  `.claude/instructions/hardware/debug-lessons.md` first** — 7-step protocol + the common traps
  (boot-loop strap, silkscreen TXD≠UART2, monitor RTS reset, stale `.sof`, GND).
- `verification-before-completion` before calling it done.
- Update `CHALLENGES.md` with the challenge status.
