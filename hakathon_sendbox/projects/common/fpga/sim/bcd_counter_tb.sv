// Self-checking test for bcd_counter: increment N times, check packed BCD,
// and check carry across a digit boundary.
`timescale 1ns/1ps

module bcd_counter_tb;

    logic clk = 0, rst_n = 0, inc = 0;
    logic [15:0] bcd;   // 4 digits

    bcd_counter #(.DIGITS(4)) dut (.clk(clk), .rst_n(rst_n), .inc(inc), .bcd(bcd));

    always #10 clk = ~clk;

    int errors = 0;
    task automatic pulse(); @(negedge clk); inc = 1; @(negedge clk); inc = 0; endtask

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1;
        @(negedge clk);

        // 23 increments -> 0x0023 (digit1=2, digit0=3)
        repeat (23) pulse();
        if (bcd !== 16'h0023) begin $error("after 23: got %04h exp 0023", bcd); errors++; end

        // 77 more -> 100 total -> 0x0100 (carry through two digits)
        repeat (77) pulse();
        if (bcd !== 16'h0100) begin $error("after 100: got %04h exp 0100", bcd); errors++; end

        if (errors == 0) $display("BCD_COUNTER: PASS");
        else             $display("BCD_COUNTER: FAIL (%0d errors)", errors);
        $finish;
    end

    initial begin #2_000_000; $error("timeout"); $finish; end

endmodule
