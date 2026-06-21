# lcd_ctrl — extract on demand (add-on LCD, large FSM)

Drives the add-on 480x800 LCD (ILI9488-class) over the Arduino header, streaming
RGB565 pixels. It's a large, board-specific FSM that needs a 100 MHz clock (PLL
IP) and precise init timing, so it's documented rather than pre-built blind.
Build it only if a challenge uses the LCD add-on.

## Extract from the `de10lite-addon-peripherals` skill ("LCD Controller Architecture")

- **`lcd_ctrl.sv`** — FSM `IDLE -> INIT_SEQUENCE -> WAIT_FRAME -> STREAM_PIXELS`.
  Packs 4-bit-per-channel VGA color into 16-bit RGB565 (2 bytes/pixel). Clocked at
  100 MHz (generate via the `pll25` wizard's c2 output, or a dedicated PLL).
- Wiring: 8-bit data bus + control signals on the Arduino header (see the skill's
  pin table). RGB packing: `Byte1 = RRRRR_GGG`, `Byte2 = GGG_BBBBB`.

The skill section has the full module, the init sequence, and the exact pin map.
