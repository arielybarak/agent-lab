# vga_game starter

16x16 red sprite bouncing on a 640x480 VGA screen. The biggest event-day head
start for any graphics/game challenge — VGA timing + motion + compositing already
wired. FPGA-only (no ESP32 needed; `esp32/` left empty).

Bricks: `vga_sync`, `frame_move`, `sprite`, `obj_rect`, `compositor` (+ `pll25` IP).

## Setup (required before it compiles)
1. **Generate `pll25`** (50→25 MHz) and add `pll25.qip` to `fpga/game.qsf`.
   See `projects/common/fpga/pll25.README.md`. Match the instance port names in
   `game_top.sv` (`.inclk0`, `.c0`) to your wizard output.
2. **Add VGA pin assignments** to `fpga/game.qsf` (VGA_R/G/B[3:0], VGA_HS, VGA_VS)
   from the `de10lite-board-and-build` skill (verified DE10-Lite VGA pins).

## Run
- Compile `fpga/game.qsf` → program. Reset = KEY[0], pause = SW[0].
- Expect: red square bounces off the screen edges on a dark-blue field.

## Extend
- Drive `sprite.pos_x/pos_y` from a joystick instead of `frame_move`
  (`analog_input` + `periphery_control`, see `adc.README.md`).
- Add a second sprite into `compositor` (s2_rgb/s2_draw) for a player + ball.
- Swap the solid `sprite` color for a bitmap ROM (see the vga skill).
