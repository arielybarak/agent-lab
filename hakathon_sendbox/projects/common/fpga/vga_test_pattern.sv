// vga_test_pattern -- 8 vertical color bars (80 px each) for VGA bring-up.
// Wire pixel_x/disp_ena from vga_sync; feed red/green/blue to the DE10-Lite
// 4-bit-per-channel VGA DAC. If you see the bars, your clock/sync/DAC wiring is
// good. Bar order: White Yellow Cyan Green Magenta Red Blue Black.

module vga_test_pattern (
    input  logic [9:0] pixel_x,
    input  logic       disp_ena,
    output logic [3:0] red,
    output logic [3:0] green,
    output logic [3:0] blue
);

    logic [2:0]  bar;
    logic [11:0] c;

    assign bar = pixel_x / 80;   // 0..7 across the 640-px line

    always_comb begin
        case (bar)
            3'd0: c = 12'hFFF;   // white
            3'd1: c = 12'hFF0;   // yellow
            3'd2: c = 12'h0FF;   // cyan
            3'd3: c = 12'h0F0;   // green
            3'd4: c = 12'hF0F;   // magenta
            3'd5: c = 12'hF00;   // red
            3'd6: c = 12'h00F;   // blue
            default: c = 12'h000;// black
        endcase
    end

    assign {red, green, blue} = disp_ena ? c : 12'h000;

endmodule
