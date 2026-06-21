# text_screen — extract on demand (needs Quartus IP)

An 80x60 character text overlay for VGA. It depends on **two generated Quartus
RAM/ROM blocks** (a dual-port `text_ram` for character + metadata, and a
`font_rom` initialized from a font `.mif`), so it isn't a standalone `.sv`. Build
it only when a challenge needs on-screen text; the VGA primitives it sits on top
of (`vga_sync`, `compositor`) are already in this folder.

## Extract from the `de10lite-vga-graphics` skill ("Text Screen Module")

- **`text_screen.sv`** — 3-cycle pipeline: read char from `text_ram`, look up
  glyph row in `font_rom`, output pixel. Per-char 8-bit metadata (FG/BG + underline).
  CPU writes at address range 0x4000–0x5FFF (`addr = row*128 + col`).
- **`font_rom`** (Quartus IP) — 256 chars x 8 rows, 8-bit wide, init from a font `.mif`.
- **`text_ram`** (Quartus IP) — dual-port, 16-bit wide, 8192 deep.

The skill section gives the exact module, the IP wizard settings, and the
memory-map. Generate the IP, add the `.qip` files to your `.qsf`, then composite
`text_screen`'s RGB over your scene with `compositor`.
