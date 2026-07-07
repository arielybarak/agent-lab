// Self-checking timing test for vga_sync: active-line length, hsync pulse
// width, and frame_start coordinate.
`timescale 1ns/1ps

module vga_sync_tb;

    logic       clk = 0, rst_n = 0;
    logic       hsync, vsync, disp_ena, frame_start;
    logic [9:0] px, py;

    vga_sync dut (.pixel_clk(clk), .rst_n(rst_n), .hsync(hsync), .vsync(vsync),
                  .disp_ena(disp_ena), .pixel_x(px), .pixel_y(py),
                  .frame_start(frame_start));

    always #20 clk = ~clk;

    int errors = 0;
    int cnt;

    initial begin
        repeat (3) @(posedge clk);
        rst_n = 1;
        @(posedge clk);

        // one active-display run should be exactly 640 pixels
        while (!disp_ena) @(posedge clk);
        cnt = 0;
        while (disp_ena) begin cnt++; @(posedge clk); end
        if (cnt !== 640) begin $error("active run = %0d (exp 640)", cnt); errors++; end

        // hsync low pulse should be 96 cycles
        while (hsync) @(posedge clk);
        cnt = 0;
        while (!hsync) begin cnt++; @(posedge clk); end
        if (cnt !== 96) begin $error("hsync low = %0d (exp 96)", cnt); errors++; end

        // frame_start should fire at (x=0, y=480)
        do @(posedge clk); while (!frame_start);
        if (px !== 10'd0 || py !== 10'd480)
            begin $error("frame_start at (%0d,%0d) exp (0,480)", px, py); errors++; end

        if (errors == 0) $display("VGA_SYNC: PASS");
        else             $display("VGA_SYNC: FAIL (%0d errors)", errors);
        $finish;
    end

    initial begin #50_000_000; $error("timeout"); $finish; end

endmodule
