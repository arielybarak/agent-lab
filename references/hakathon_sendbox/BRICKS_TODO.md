# Bricks to build — Copilot work-list (Tiers 2–4 + starters)

> **SUPERSEDED — all tiers are now built.** Tiers 2–4 + starters were completed in Claude; see
> `projects/common/README.md` and `CHALLENGES.md`. This file is kept only as a record of the
> sources/interfaces and as a guide for building the deferred IP-bound modules
> (`hack_cpu`/`mem_arbiter`, `text_screen`, `lcd_ctrl`) if a matching challenge appears.

Tier 1 is done (see `projects/common/README.md`). **This file is for GitHub Copilot** to build the
rest cheaply. Build top-to-bottom; each item is independent. Mirror the existing Tier-1 bricks'
style and add a testbench for every FPGA module.

## Rules (match Tier 1 exactly)

**FPGA SystemVerilog** (`projects/common/fpga/`)
- Header comment explaining the module + ports. `snake_case`. Parametric where sensible.
- Sequential logic: `always_ff @(posedge clk or negedge rst_n)`, **async active-low reset**.
- Look at `uart_tx.sv`, `button_debounce.sv`, `hex_display.sv` for the exact pattern.
- **Add a self-checking testbench** `sim/<name>_tb.sv` (prints `PASS`/`FAIL`, has a timeout) **and**
  a `sim/<name>_tb.do` (copy the 5-line pattern from `sim/uart_loopback_tb.do`). Use a small baud/
  count so sims finish fast. Verify with `just sim <name>`.

**ESP32 C++** (`projects/common/esp32/`, header-only classes)
- `#pragma once`, `#include "pin_config.h"`, a usage example in the header comment.
- Mirror `button.h` / `analog.h`: non-blocking `update()`, no blocking delays in loop helpers.

**Sources** (read these, don't reinvent):
- Demos: `/home/barak/TechCrash2026/demos/{alive_test,internet_clock}/{fpga/src,esp32/src}/`
- BKM skills: `.claude/skills/de10lite-board-and-build/SKILL.md`,
  `.claude/skills/de10lite-vga-graphics/SKILL.md`,
  `.claude/skills/de10lite-addon-peripherals/SKILL.md`, `.claude/skills/esp32-firmware/SKILL.md`

---

## Tier 2 — counters, parsing, more ESP32 IO

### FPGA
| File | Source | Interface / behavior | Verify |
|------|--------|----------------------|--------|
| `bin2bcd.sv` | new (double-dabble) | `#(WIDTH=16, DIGITS=5)` `input [WIDTH-1:0] bin` → `output [4*DIGITS-1:0] bcd` (combinational or small FSM). Feeds `hex_display` for decimal. | `bin2bcd_tb`: check 0, 42, 999, 65535 → digits |
| `bcd_counter.sv` | **extract** `alive_test_top.sv` lines ~44–71 (cascaded rollover) | `#(DIGITS=4)` `input clk,rst_n,inc` (1-cycle pulse) → `output [4*DIGITS-1:0] bcd`. Each digit 0-9, carry up, wrap. | `bcd_counter_tb`: pulse 9×→carry; wrap at all-9 |
| `ascii_num_parser.sv` | **extract+generalize** `internet_clock_top.sv` parser (~lines 47–95) | Feed bytes (`byte_in`,`byte_valid` from `uart_rx`). Capture digit chars `'0'..'9'`, skip non-digits, commit on `\n`. Param `#(FIELDS=6)` → `output [4*FIELDS-1:0] digits, output valid`. | `ascii_num_parser_tb`: feed `"12:34:56\n"`→ 6 BCD digits |

### ESP32 (`esp32/`)
| File | Source | API |
|------|--------|-----|
| `buzzer.h` | **extract** `alive_test/esp32/src/main.cpp` lines ~150–165 | `Buzzer(PIN_BUZZER)`: `tone(freq)`, `beep(freq,ms)` non-blocking via `update()`, `off()`. Presets `LOW=800,MID=1500,HIGH=2000`. |
| `servo.h` | **extract** same file lines ~39–43, 95–97 | `Servo(PIN_SERVO)`: `begin()` (`ledcAttach(pin,50,16)`), `write(deg)` using `us=500+deg*2000/180`, `duty=us*65536/20000`. |
| `led.h` | **extract** same file lines ~130–136 | `Led(pin)`: `on/off/toggle/blink(ms)` (non-blocking `update()`). Plus `LedChaser(pins[],n,ms)` cycling pattern. |
| `wifi_ntp.h` | **extract** `internet_clock/esp32/src/main.cpp` | `WifiNtp`: `connect(ssid,pass)`, `syncTime(gmtOffset,dstOffset,"pool.ntp.org")`, `getTime(h,m,s)` + `getString("HH:MM:SS")`. Uses `WiFi.h` + `time.h`. |

---

## Tier 3 — VGA / game stack

Read `de10lite-vga-graphics/SKILL.md`. These mostly already exist there as code — extract verbatim,
keep names below. `pll25` is a Quartus IP (not plain `.sv`): document the MegaWizard steps in
`fpga/pll25.README.md` (50→25/50/100 MHz) instead of an `.sv`.

| File | Skill section | Notes |
|------|---------------|-------|
| `vga_sync.sv` | "Parameterized VGA Controller" / "sync_gen" | 640×480@60 → `h_sync,v_sync,disp_ena,pixel_x,pixel_y`. Needs 25 MHz pixel clk from `pll25`. |
| `vga_test_pattern.sv` | "Test Pattern Generator" | 8 color bars — bring-up sanity. |
| `obj_rect.sv` | "Rectangle Bounds Check (obj_rect.sv)" | Param `OBJECT_WIDTH/HEIGHT`, signed coords → `drawingRequest, offsetX/Y`. |
| `sprite.sv` | "Template Sprite Unit" (Move+Draw) | Combine move + bitmap draw + `obj_rect`. |
| `compositor.sv` | "Priority Compositing" | Mux RGB by z-order (sprite1 > sprite2 > bg). |
| `frame_move.sv` | "Frame-Synchronized Movement" + "Bounce Physics" | End-of-frame pulse + rate-limited move + wall bounce. |
| `analog_input.sv` + `periphery_control.sv` | `de10lite-addon-peripherals` "ADC FSM" + "Periphery Control Wrapper" | Joystick/buttons from ADC. **Needs a Qsys ADC IP** — document the Qsys steps in a README. |

Testbenches: at least `vga_sync_tb` (check h/v sync pulse widths + active window) and `obj_rect_tb`,
`compositor_tb` (bounds + z-order). Sprites/frame_move can be smoke-checked on hardware.

---

## Tier 4 — heavy / stretch (only if time)

| File | Skill section | Notes |
|------|---------------|-------|
| `pipeline_accumulator.sv` | board-and-build "Pipeline Accumulator" | Single-adder N-input sum FSM. `pipeline_accumulator_tb`. |
| `hack_cpu.sv`,`alu.sv`,`mem_arbiter.sv` | board-and-build "Hack CPU"/"ALU"/"Memory Space Arbiter" | nand2tetris CPU; big. Only if a CPU challenge appears. |
| `text_screen.sv` | vga-graphics "Text Screen Module" | 80×60 text overlay; needs `font_rom` + `text_ram` Qsys IP (document). |
| `lcd_ctrl.sv` | addon-peripherals "LCD Controller Architecture" | 480×800 add-on LCD, RGB565, 100 MHz. |
| `packet.h` + `packet_decoder.sv` | new (optional) | Framed binary `[0xAA][len][cmd][payload][crc8]` both sides. Only if ASCII is too slow for a challenge. |

---

## Starters (assemble from bricks) — `challenges/starters/`

Each is a ready-to-copy challenge base with parallel `fpga/` + `esp32/`. Model the folder on
`challenges/_template/`; pull bricks via the `.qsf SV_FILE` line and `-I` build flag (see
`projects/common/README.md`).

| Starter | Build from |
|---------|-----------|
| `uart_echo/` | `uart_rx`+`uart_tx` (FPGA echo) ⇄ `uart_fpga.h` (`readLine`→`sendLine`). Minimal both-sides ASCII echo. |
| `clock/` | `uart_line_rx`+`ascii_num_parser`+`hex_display` (FPGA) ⇄ `wifi_ntp.h`+`uart_fpga.h` (ESP32 streams `HH:MM:SS\n`). |
| `vga_game/` | `pll25`+`vga_sync`+`sprite`+`compositor`+`frame_move` + joystick (`analog_input`). A sprite you can move. **Biggest event-day head start.** |

When done, tick the boxes in `CHALLENGES.md` → "Bricks ready", and run each FPGA brick's
`just sim <name>` to confirm `PASS`.
