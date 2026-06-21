// Self-checking test for compositor: z-order (sprite1 > sprite2 > bg) + channel split.
`timescale 1ns/1ps

module compositor_tb;

    logic [11:0] bg = 12'h111, s1 = 12'hF00, s2 = 12'h0F0;
    logic        s1d, s2d;
    logic [11:0] rgb;
    logic [3:0]  r, g, b;

    compositor dut (.bg_rgb(bg), .s1_rgb(s1), .s1_draw(s1d), .s2_rgb(s2), .s2_draw(s2d),
                    .rgb(rgb), .red(r), .green(g), .blue(b));

    int errors = 0;
    task automatic chk(input string name, input logic [11:0] exp);
        #1;
        if (rgb !== exp) begin $error("%s: rgb=%03h exp %03h", name, rgb, exp); errors++; end
    endtask

    initial begin
        s1d = 1; s2d = 1; chk("both -> s1 wins", 12'hF00);
        if (r !== 4'hF || g !== 4'h0 || b !== 4'h0) begin $error("split bad"); errors++; end
        s1d = 0; s2d = 1; chk("s2 only", 12'h0F0);
        s1d = 0; s2d = 0; chk("background", 12'h111);

        if (errors == 0) $display("COMPOSITOR: PASS");
        else             $display("COMPOSITOR: FAIL (%0d errors)", errors);
        $finish;
    end

endmodule
