// game_top -- VGA "moving sprite" starter for the DE10-Lite.
// A 16x16 red sprite bounces around a 640x480 screen. Built from
// pll25 + vga_sync + frame_move + sprite + compositor.
//
// BEFORE THIS COMPILES you must:
//   1. Generate the pll25 PLL IP (50 -> 25 MHz) and add pll25.qip to game.qsf
//      (see projects/common/fpga/pll25.README.md). Match the port names below.
//   2. Add the DE10-Lite VGA pin assignments to game.qsf (VGA_R/G/B[3:0],
//      VGA_HS, VGA_VS) from the de10lite-board-and-build skill.
// Reset = KEY[0]. Pause = SW[0].

module game_top (
    input         MAX10_CLK1_50,
    input  [9:0]  SW,
    input  [1:0]  KEY,
    output [9:0]  LEDR,
    output [7:0]  HEX0, HEX1, HEX2, HEX3, HEX4, HEX5,
    // VGA (4-bit DAC per channel)
    output [3:0]  VGA_R,
    output [3:0]  VGA_G,
    output [3:0]  VGA_B,
    output        VGA_HS,
    output        VGA_VS
);

    wire rst_n = KEY[0];

    // ---- 25 MHz pixel clock from the PLL IP (generate pll25 first) ----
    wire pix_clk;
    pll25 u_pll (.inclk0(MAX10_CLK1_50), .c0(pix_clk));   // adjust port names to your wizard

    // ---- VGA timing ----
    wire        disp_ena, frame_start;
    wire [9:0]  px, py;
    vga_sync u_vga (
        .pixel_clk(pix_clk), .rst_n(rst_n),
        .hsync(VGA_HS), .vsync(VGA_VS), .disp_ena(disp_ena),
        .pixel_x(px), .pixel_y(py), .frame_start(frame_start));

    // ---- bouncing position (one step per frame) ----
    wire signed [11:0] sx, sy;
    frame_move #(.X_MAX(624), .Y_MAX(464), .STEP(2)) u_move (
        .clk(pix_clk), .rst_n(rst_n), .frame_tick(frame_start), .ena(~SW[0]),
        .pos_x(sx), .pos_y(sy));

    // ---- sprite (16x16 red) ----
    wire        s_draw;
    wire [11:0] s_rgb;
    sprite #(.WIDTH(16), .HEIGHT(16), .COLOR(12'hF00)) u_sprite (
        .pixel_x($signed({2'b0, px})), .pixel_y($signed({2'b0, py})),
        .pos_x(sx), .pos_y(sy), .drawing(s_draw), .rgb(s_rgb));

    // ---- composite over a dark-blue background, gate with disp_ena ----
    wire [3:0] r, g, b;
    compositor u_comp (
        .bg_rgb(12'h001), .s1_rgb(s_rgb), .s1_draw(s_draw),
        .s2_rgb(12'h000), .s2_draw(1'b0),
        .rgb(), .red(r), .green(g), .blue(b));

    assign VGA_R = disp_ena ? r : 4'h0;
    assign VGA_G = disp_ena ? g : 4'h0;
    assign VGA_B = disp_ena ? b : 4'h0;

    assign LEDR = 10'b0;
    assign {HEX5, HEX4, HEX3, HEX2, HEX1, HEX0} = {6{8'hFF}};

endmodule
