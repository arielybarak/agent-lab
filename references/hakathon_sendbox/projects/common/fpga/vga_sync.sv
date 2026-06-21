// vga_sync -- 640x480 @ 60 Hz VGA timing generator.
// Drive pixel_clk at 25 MHz (use the pll25 IP: 50 -> 25 MHz). Outputs the
// sync pulses, the active-display enable, the current pixel coordinate, and a
// 1-cycle frame_start pulse at the end of each frame (for frame-synced motion).
//
// Standard timing: H 640 + FP16 + SYNC96 + BP48 = 800; V 480 + FP10 + SYNC2 + BP33 = 525.
// hsync/vsync are active-LOW. On the DE10-Lite, gate the 4-bit RGB DACs with disp_ena.

module vga_sync (
    input  logic       pixel_clk,   // 25 MHz
    input  logic       rst_n,
    output logic       hsync,
    output logic       vsync,
    output logic       disp_ena,    // high in the visible 640x480 region
    output logic [9:0] pixel_x,     // 0..799 (valid 0..639 when disp_ena)
    output logic [9:0] pixel_y,     // 0..524 (valid 0..479 when disp_ena)
    output logic       frame_start  // 1-cycle pulse at start of vertical blanking
);

    localparam H_VISIBLE = 640, H_FP = 16, H_SYNC = 96, H_BP = 48, H_TOTAL = 800;
    localparam V_VISIBLE = 480, V_FP = 10, V_SYNC = 2,  V_BP = 33, V_TOTAL = 525;

    logic [9:0] hc, vc;

    always_ff @(posedge pixel_clk or negedge rst_n) begin
        if (!rst_n) begin
            hc <= 0;
            vc <= 0;
        end else if (hc == H_TOTAL - 1) begin
            hc <= 0;
            vc <= (vc == V_TOTAL - 1) ? 10'd0 : vc + 1;
        end else begin
            hc <= hc + 1;
        end
    end

    assign pixel_x     = hc;
    assign pixel_y     = vc;
    assign disp_ena    = (hc < H_VISIBLE) && (vc < V_VISIBLE);
    assign hsync       = ~((hc >= H_VISIBLE + H_FP) && (hc < H_VISIBLE + H_FP + H_SYNC));
    assign vsync       = ~((vc >= V_VISIBLE + V_FP) && (vc < V_VISIBLE + V_FP + V_SYNC));
    assign frame_start = (hc == 0) && (vc == V_VISIBLE);

endmodule
