# Reusable bricks (shared library)

Pre-built, tested modules + utilities to assemble challenges fast. Copy nothing — reference these
in place.

## FPGA (SystemVerilog) — `fpga/`

Pull a brick into a challenge by adding it to that challenge's `.qsf`:
```
set_global_assignment -name SV_FILE ../../../projects/common/fpga/uart_rx.sv
```
Pin/UART contract: `fpga/pins.svh`.

| Brick | Does | Key ports/params |
|-------|------|------------------|
| `uart_rx.sv` | UART receive, 8N1 | `#(CLK_FREQ,BAUD)` → `rx_data, rx_valid` |
| `uart_tx.sv` | UART transmit, 8N1 | `tx_start, tx_data` → `tx, tx_busy` |
| `uart_line_rx.sv` | Buffer bytes into a line until `\n` | → `line[], len, line_valid` |
| `seven_segment.sv` | BCD digit → active-low segs (0-9, blank) | `data, blank` → `seg` |
| `hex_display.sv` | One value → all 6 HEX digits, 0-F, leading-zero blank | `value[23:0]` → `HEX0..5` |
| `clock_divider.sv` | Divided ~50% clock | `#(COUNT_MAX)` → `clk_out` |
| `tick_gen.sv` | 1-cycle pulse every N cycles (default 1 Hz) | `#(COUNT)` → `tick` |
| `button_debounce.sv` | Debounce active-low KEY + edge pulses | `btn_n` → `level, press, release_p` |
| `sync_2ff.sv` | 2-FF synchronizer for async inputs | `#(WIDTH)` `d` → `q` |
| `edge_detect.sv` | Rising/falling/either pulses | `sig` → `rising, falling, either` |

**Sim:** each brick has a self-checking testbench in `fpga/sim/`. Run one with
`just sim <name>` (e.g. `just sim uart_loopback`) — needs ModelSim. Each prints `PASS`/`FAIL`.

## ESP32 (C++ headers) — `esp32/`

In a challenge's `platformio.ini`:
```
build_flags = -I ../../../projects/common/esp32
```
then `#include "uart_fpga.h"`. All headers include `pin_config.h`.

| Header | Class / use |
|--------|-------------|
| `pin_config.h` | All GPIO/pin defines |
| `uart_fpga.h` | `UartFpga` — `begin()`, `sendLine()`, non-blocking `readLine()` |
| `oled.h` | `Oled` — `start(title)`, `kv()`, `bar()`, `show()` (Adafruit SSD1306) |
| `button.h` | `Button` — `update()`, `pressed()/released()/held()` (50 ms debounce) |
| `analog.h` | `Analog` — `update()`, `raw()/value()/volts()/percent()/mapTo()` (EMA smoothing) |

## More bricks (Tiers 2–4)

FPGA (`fpga/`): `bin2bcd`, `bcd_counter`, `ascii_num_parser` (counters/parsing) ·
`vga_sync`, `vga_test_pattern`, `obj_rect`, `sprite`, `compositor`, `frame_move`,
`periphery_control` (VGA/game) · `pipeline_accumulator`, `alu`, `packet_decoder` (heavy).
Each has a `sim/<name>_tb` where it's testable.

IP-dependent (generate in Quartus, see the matching README): `pll25` (pixel clock),
`analog_input` (ADC, `adc.README.md`), `hack_cpu`/`mem_arbiter`, `text_screen`, `lcd_ctrl`.

ESP32 (`esp32/`): `buzzer.h`, `servo.h`, `led.h`, `wifi_ntp.h`, `packet.h`.

## Starters

`challenges/starters/`: `uart_echo`, `clock` (run as-is), `vga_game` (needs `pll25` IP + VGA
pins). See each starter's README.

## Status

**All tiers built.** Self-contained FPGA bricks have passing-by-design testbenches (run on
Windows ModelSim via `just sim <name>` to confirm). IP-bound bricks are documented with generate
steps. ESP32 headers verified by on-hardware smoke.
