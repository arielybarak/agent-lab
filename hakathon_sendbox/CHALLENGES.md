# Challenges — status board

Track each challenge here so progress survives across sessions (and saves re-asking the agent).
Status: ⬜ todo · 🟡 in-progress · ✅ done · ⛔ blocked.

| # | Challenge | Skill used | FPGA | ESP32 | Status | Notes |
|---|-----------|------------|------|-------|--------|-------|
| – | _(example)_ vga-sprite | de10lite-vga-graphics | ⬜ | – | ⬜ | |

## Bricks ready (pre-built reusable library — `projects/common/`)

**Tier 1 — built + testbenched** ✅
- FPGA: `uart_rx`, `uart_tx`, `uart_line_rx`, `seven_segment`, `hex_display`, `clock_divider`,
  `tick_gen`, `button_debounce`, `sync_2ff`, `edge_detect` (sim: `just sim <name>`)
- ESP32: `uart_fpga.h`, `oled.h`, `button.h`, `analog.h`

**Tier 2 — built + testbenched** ✅
- FPGA: `bin2bcd`, `bcd_counter`, `ascii_num_parser`
- ESP32: `buzzer.h`, `servo.h`, `led.h`, `wifi_ntp.h`

**Tier 3 (VGA/game) — built** ✅
- FPGA: `vga_sync`, `vga_test_pattern`, `obj_rect`, `sprite`, `compositor`, `frame_move`,
  `periphery_control` (sim: `vga_sync`, `obj_rect`, `compositor`)
- IP-dependent (README + generate steps): `pll25.README.md`, `adc.README.md` (`analog_input`)

**Tier 4 — built + READMEs** ✅
- Built + testbenched: `pipeline_accumulator`, `alu`, `packet_decoder` + `packet.h`
- Deferred (need generated IP / large; extraction READMEs): `hack_cpu`+`mem_arbiter`,
  `text_screen`, `lcd_ctrl`

**Starters — built** ✅ `uart_echo`, `clock` (both run as-is), `vga_game` (needs `pll25` IP +
VGA pins — see its README)

All FPGA bricks have a `just sim <name>` testbench (run on Windows ModelSim to confirm PASS).
`BRICKS_TODO.md` was the Copilot spec — now superseded by the built library.

## Workflow reminder
1. `challenge-intake` skill → route to the right BKM skill.
2. `just new-challenge <name>` → scaffold from the compiling template.
3. Build: `just fpga-build` / `just esp32-build`; program/flash per `SETUP_QUICKSTART.md`.
4. Update the row above.
