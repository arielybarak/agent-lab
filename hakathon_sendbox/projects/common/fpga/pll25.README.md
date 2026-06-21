# pll25 — VGA pixel clock (Quartus IP, not a .sv)

VGA 640x480@60 needs a ~25 MHz pixel clock. The DE10-Lite has a 50 MHz input, so
generate a PLL with the Quartus IP Catalog (it produces encrypted IP + a wrapper,
which is why this isn't a plain SystemVerilog file).

## Generate it (once)

1. Quartus → **Tools → IP Catalog** → search **ALTPLL** (or "PLL").
2. Name it `pll25`. Output language: **SystemVerilog/Verilog**.
3. Input clock: **50 MHz**.
4. Outputs:
   - `c0` = **25 MHz** (VGA pixel clock) — the one you need.
   - (optional) `c1` = 50 MHz system, `c2` = 100 MHz (LCD).
5. Generate. Add the produced `pll25.qip` to your project `.qsf`:
   `set_global_assignment -name QIP_FILE pll25.qip`

## Use it

```systemverilog
wire pix_clk;
pll25 u_pll (.inclk0(MAX10_CLK1_50), .c0(pix_clk));   // port names per your wizard

vga_sync u_vga (.pixel_clk(pix_clk), .rst_n(rst_n), ...);
```

Reference: the `de10lite-board-and-build` and `de10lite-vga-graphics` skills
("pll25", "Parameterized VGA Controller").
