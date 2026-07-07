---
name: De10Lite Vga Graphics
description: >
  Game graphics architecture — sprites, compositing, frame sync. Text
  screen module (80×60 chars with font ROM). VGA display system (640×480
  @ 60Hz) for DE10-Lite.
---

# De10Lite Vga Graphics

## VGA Display System for DE10-Lite (640×480 @ 60Hz)

**For Future Projects**: Complete VGA output implementation with parameterized controller, multi-mode display hub, and 12-bit RGB output.

---

## VGA Timing (640×480 @ 60Hz)

| Parameter | Horizontal | Vertical |
|-----------|-----------|----------|
| **Active pixels** | 640 | 480 |
| **Front porch** | 16 | 10 |
| **Sync pulse** | 96 | 2 |
| **Back porch** | 48 | 33 |
| **Total** | 800 | 525 |
| **Pixel clock** | 25.175 MHz (use 25 MHz from PLL) |

## PLL Configuration

Generate 25 MHz pixel clock from 50 MHz input:

```systemverilog
pll25 pll_inst (
    .inclk0(MAX10_CLK1_50),   // 50 MHz in
    .c0(clk_25),               // 25 MHz (VGA pixel clock)
    .c1(clk_50),               // 50 MHz (system clock)
    .c2(clk_100)               // 100 MHz (optional fast clock)
);
```

Use Quartus IP Catalog → ALTPLL to generate.

## Parameterized VGA Controller

```systemverilog
module vga_controller #(
    parameter h_pixels   = 640,
    parameter h_fp       = 16,
    parameter h_pulse    = 96,
    parameter h_bp       = 48,
    parameter v_pixels   = 480,
    parameter v_fp       = 10,
    parameter v_pulse    = 2,
    parameter v_bp       = 33
)(
    input              pixel_clk,
    input              reset_n,
    output reg         h_sync,
    output reg         v_sync,
    output reg         disp_ena,
    output reg [31:0]  column,
    output reg [31:0]  row
);
```

**Key outputs:**
- `disp_ena` = HIGH only during active pixel area (use to blank RGB)
- `column` = current X pixel (0-639)
- `row` = current Y pixel (0-479)
- `h_sync`, `v_sync` = active-low sync pulses

## Multi-Mode Display Hub (vga_ctrl.sv)

Switch between display modes using `cfg[1:0]`:

```systemverilog
// Mode selection mux
always @(*) begin
    case(cfg)
        2'b00: begin Red = game_R; Green = game_G; Blue = game_B; end   // Game mode
        2'b01: begin Red = text_R; Green = text_G; Blue = text_B; end   // Text screen
        2'b11: begin Red = pat_R;  Green = pat_G;  Blue = pat_B;  end   // Test pattern
        default: begin Red = 4'h0; Green = 4'h0; Blue = 4'h0; end
    endcase
end
```

## Start-of-Frame Detection

Edge-detect `v_sync` for frame-rate operations:

```systemverilog
reg v_sync_d;
always @(posedge clk) v_sync_d <= v_sync;
wire start_of_frame = v_sync && !v_sync_d;  // Rising edge of v_sync
```

## DE10-Lite VGA DAC

The DE10-Lite has a 4-bit resistor DAC per channel (total 12-bit color = 4096 colors):

```systemverilog
// Final output (active only during display area)
assign VGA_R = disp_ena ? Red : 4'h0;
assign VGA_G = disp_ena ? Green : 4'h0;
assign VGA_B = disp_ena ? Blue : 4'h0;
assign VGA_HS = h_sync;
assign VGA_VS = v_sync;
```

## Test Pattern Generator

Useful for verifying VGA output without complex logic:

```systemverilog
// Color bars (top half of screen)
if (row < 240) begin
    case (column[9:7])  // 8 bars of 80 pixels each
        3'd0: {R,G,B} = 12'hFFF;  // White
        3'd1: {R,G,B} = 12'hFF0;  // Yellow
        3'd2: {R,G,B} = 12'h0FF;  // Cyan
        3'd3: {R,G,B} = 12'h0F0;  // Green
        3'd4: {R,G,B} = 12'hF0F;  // Magenta
        3'd5: {R,G,B} = 12'hF00;  // Red
        3'd6: {R,G,B} = 12'h00F;  // Blue
        3'd7: {R,G,B} = 12'h000;  // Black
    endcase
end
```

## Source Files Reference

| File | Purpose |
|------|---------|
| `vga_controller.v` | Parameterized sync generator |
| `sync_gen.sv` | Simple sync gen with built-in clock divider |
| `vga_ctrl.sv` | Multi-mode display hub |
| `pattern_generator.sv` | Color bars test pattern |

---

## Game Graphics Architecture — Sprites, Compositing & Frame Sync

**For Future Projects**: Sprite-based 2D game graphics on DE10-Lite with priority compositing, bitmap rendering, and frame-synchronized movement.

---

## Architecture Pattern

```
Background Unit ──────────────────┐
                                  ├── Drawing_priority (compositor) ──► VGA RGB
Sprite Unit 1 (player) ──────────┤
                                  │
Sprite Unit 2 (enemy) ───────────┘
```

Each sprite unit follows the **Move + Draw** decomposition:

```
Sprite_unit
├── Move_module  (position logic, collision, boundary)
│   ├── Input: controls (joystick/buttons), collision flags
│   └── Output: topLeft_x, topLeft_y
└── Draw_module  (pixel rendering)
    ├── Input: pxl_x, pxl_y, topLeft_x, topLeft_y
    └── Output: Red[3:0], Green[3:0], Blue[3:0], Drawing (bool)
```

## Rectangle Bounds Check (obj_rect.sv)

Reusable parameterized module for sprite hit testing:

```systemverilog
module obj_rect #(
    parameter OBJECT_WIDTH_X  = 32,
    parameter OBJECT_HEIGHT_Y = 16
)(
    input  signed [31:0] pxl_x, pxl_y,
    input  signed [31:0] topLeft_x, topLeft_y,
    output        [10:0] offsetX, offsetY,
    output               drawingRequest
);

wire signed [31:0] rightX  = topLeft_x + OBJECT_WIDTH_X;
wire signed [31:0] bottomY = topLeft_y + OBJECT_HEIGHT_Y;

assign drawingRequest = (pxl_x >= topLeft_x) && (pxl_x < rightX)
                     && (pxl_y >= topLeft_y) && (pxl_y < bottomY);
assign offsetX = pxl_x - topLeft_x;
assign offsetY = pxl_y - topLeft_y;
```

**Key**: Uses `signed` math so sprites can be partially off-screen (negative topLeft).

## Bitmap Sprite Rendering

Two proven approaches:

### 1. Inline Bitmap (Draw_Intel pattern)

Large bitmap stored as SystemVerilog array literal:

```systemverilog
logic [0:63][0:127][11:0] Bitmap = { ... };  // 128×64 × 12-bit RGB

// Transparency check
localparam TRANSPARENT = 12'hFFF;
if (in_rectangle && Bitmap[offset_y][offset_x] != TRANSPARENT) begin
    Drawing <= 1;
    {Red, Green, Blue} <= Bitmap[offset_y][offset_x];
end
```

### 2. ROM-based Bitmap (smileyBitMap pattern)

8-bit packed color with ROM lookup:

```systemverilog
// RRRGGGBB packed format
localparam TRANSPARENT_ENCODING = 8'h00;
wire [7:0] pixel = bitmap_data[offsetY][offsetX];
assign Red   = {pixel[7:5], 1'b0};   // 3-bit → 4-bit
assign Green = {pixel[4:2], 1'b0};
assign Blue  = {pixel[1:0], 2'b00};  // 2-bit → 4-bit
```

## Horizontal Sprite Flip (Zero Cost)

Mirror sprite based on movement direction:

```systemverilog
wire [31:0] bitmap_x = x_direction ? (width - offset_x - 1) : offset_x;
// Use bitmap_x for ROM/array lookup
```

## Edge Detection for Collision

Detect which edge of a sprite is at a boundary:

```systemverilog
wire hitLeft   = (offsetX == 0);
wire hitTop    = (offsetY == 0);
wire hitRight  = (offsetX == OBJECT_WIDTH_X - 1);
wire hitBottom = (offsetY == OBJECT_HEIGHT_Y - 1);
```

## Priority Compositing (Drawing_priority.sv)

Simple priority mux — first sprite with `Drawing=1` wins:

```systemverilog
always @(posedge clk or negedge resetN) begin
    if (!resetN) {Red, Green, Blue} <= 12'hFFF;
    else if (draw_1)      {Red, Green, Blue} <= RGB_1;   // Highest priority
    else if (draw_2)      {Red, Green, Blue} <= RGB_2;   // Next priority
    else                  {Red, Green, Blue} <= RGB_bg;   // Background (lowest)
end
```

**Scale**: Add more `else if` branches for additional sprites. Order = z-priority.

## Frame-Synchronized Movement

All position updates happen once per frame:

```systemverilog
// End-of-frame detection
wire end_of_frame = (pxl_x == 0) && (pxl_y == 0);

// Rate-limited movement (optional: slower than frame rate)
reg [31:0] speed_counter;
wire move_pulse = (speed_counter == 0);
always @(posedge clk) begin
    if (end_of_frame) speed_counter <= (speed_counter == 0) ? SPEED_DIV : speed_counter - 1;
end

// Update position only on move_pulse
always @(posedge clk) begin
    if (move_pulse) begin
        topLeft_x <= topLeft_x + x_speed;
        topLeft_y <= topLeft_y + y_speed;
    end
end
```

## Bounce Physics

Simple boundary bounce for autonomous sprites:

```systemverilog
if (topLeft_x <= 0 || topLeft_x >= 640-WIDTH) x_speed <= -x_speed;
if (topLeft_y <= 0 || topLeft_y >= 480-HEIGHT) y_speed <= -y_speed;

// Collision response: reverse and back away
if (collision) begin
    x_speed <= -x_speed;
    y_speed <= -y_speed;
    topLeft_x <= topLeft_x + (-x_speed);
    topLeft_y <= topLeft_y + (-y_speed);
end
```

## Template Sprite Unit

```systemverilog
module My_sprite_unit (
    input         clk, resetN,
    input  [31:0] pxl_x, pxl_y,
    // Control inputs (from periphery_control)
    input         Up, Down, Left, Right,
    input  [11:0] Wheel,
    // VGA output
    output [3:0]  Red, Green, Blue,
    output        Draw
);
    wire [31:0] topLeft_x, topLeft_y;

    My_move move_inst (.clk, .resetN, .Up, .Down, .Left, .Right,
                       .Wheel, .topLeft_x, .topLeft_y);

    My_draw draw_inst (.clk, .resetN, .pxl_x, .pxl_y,
                       .topLeft_x, .topLeft_y,
                       .Red, .Green, .Blue, .Drawing(Draw));
endmodule
```

---

## Text Screen Module (80×60 Characters with Font ROM)

**For Future Projects**: Reusable 80×60 character text display using dual-port RAM and 8×8 font ROM, for CPU-driven text output or debug displays.

---

## Architecture Overview

```
CPU write bus ──► text_ram_a (port B) ──► character data
                  text_ram_a (port A) ◄── VGA pixel scanner
                         │
                    font_rom ◄── {ASCII[7:0], row[2:0]}
                         │
                    bit select ──► pixel on/off ──► RGB output
```

## Specifications

| Parameter | Value |
|-----------|-------|
| **Grid** | 80 columns × 60 rows = 4,800 characters |
| **Character size** | 8×8 pixels |
| **Screen resolution** | 640×480 (80×8 = 640, 60×8 = 480) |
| **Font** | 8×8 pixel font in ROM (256 characters × 8 bytes) |
| **RAM size** | 8K × 16 bits (dual-port, Quartus IP) |
| **Color mode** | Per-character 8-bit metadata (FG/BG RGB + underline) |

## Memory Map (from CPU perspective)

Text screen occupies address range `0x4000–0x5FFF` (8K words):

```
Address = {row[5:0], column[6:0]}
        = row × 128 + column  (row 0-59, column 0-79)
```

Write 16-bit value: `{metadata[7:0], ASCII[7:0]}`

### Metadata Byte Format

```
Bit 7: Underline
Bit 6: Background Red
Bit 5: Background Green
Bit 4: Background Blue
Bit 3: Foreground Red
Bit 2: Foreground Green
Bit 1: Foreground Blue
Bit 0: (reserved)
```

## Pipeline (3-cycle latency)

```
Cycle 1: RAM read address = {pxl_y[8:3], pxl_x[9:3]}
          → Reads character code + metadata from text_ram_a (port A)

Cycle 2: Font ROM address = {char_code[7:0], pxl_y[2:0]}
          → Reads 8-bit font row data

Cycle 3: Bit select = font_data[7 - pxl_x_d2[2:0]]
          → 1 = foreground color, 0 = background color
```

**Important**: Pipeline delays require buffering pixel position:
```systemverilog
reg [9:0] pxl_x_d1, pxl_x_d2;
always @(posedge clk) begin
    pxl_x_d1 <= pxl_x;
    pxl_x_d2 <= pxl_x_d1;
end
```

## Dual-Port RAM Configuration (Quartus IP)

Create via IP Catalog → RAM: 2-PORT:

| Setting | Value |
|---------|-------|
| **Type** | Simple dual-port (one read, one write) |
| **Width** | 16 bits |
| **Depth** | 8192 words |
| **Port A** | Read only (VGA scan) |
| **Port B** | Write only (CPU) |
| **Read-during-write** | Don't care |
| **Clock** | Both ports same clock |
| **Init file** | Optional `.mif` for boot screen content |

## Font ROM Configuration

| Setting | Value |
|---------|-------|
| **Type** | ROM: 1-PORT |
| **Width** | 8 bits |
| **Depth** | 2048 (256 chars × 8 rows) |
| **Init file** | `font.hex` (Intel HEX or MIF format) |
| **Address** | `{char_code[7:0], row[2:0]}` = 11 bits |

## Integration Example

```systemverilog
text_screen text_inst (
    .clk(clk_25),
    .resetN(resetN),
    // VGA scan inputs
    .pxl_x(column),
    .pxl_y(row),
    // CPU write interface
    .text_data(cpu_data_out),
    .text_add(cpu_address[12:0]),
    .text_we(vga_text_wr),
    // RGB output
    .Red(text_R),
    .Green(text_G),
    .Blue(text_B)
);
```

## Usage Tips

- Clear screen: Write `0x0020` (space + white-on-black) to all 4800 positions
- Cursor: Toggle character at cursor position between char and inverse
- Scrolling: Requires shifting RAM contents (CPU-side operation)
- Boot message: Pre-load RAM with `.mif` init file
