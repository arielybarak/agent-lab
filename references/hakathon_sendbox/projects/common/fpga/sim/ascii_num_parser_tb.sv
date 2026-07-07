// Self-checking test for ascii_num_parser: feed "12:34:56\n" and check the
// six captured digits + count + valid pulse.
`timescale 1ns/1ps

module ascii_num_parser_tb;

    logic       clk = 0, rst_n = 0;
    logic [7:0] byte_in = 0;
    logic       byte_valid = 0;
    logic [23:0] digits;   // 6 nibbles
    logic [2:0]  count;
    logic        valid;

    ascii_num_parser #(.FIELDS(6)) dut (
        .clk(clk), .rst_n(rst_n), .byte_in(byte_in), .byte_valid(byte_valid),
        .digits(digits), .count(count), .valid(valid));

    always #10 clk = ~clk;

    int errors = 0;
    logic got_valid = 0;
    always @(posedge clk) if (valid) got_valid = 1;

    task automatic feed(input logic [7:0] b);
        @(negedge clk); byte_in = b; byte_valid = 1;
        @(negedge clk); byte_valid = 0;
    endtask

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1;
        @(negedge clk);

        feed("1"); feed("2"); feed(":");
        feed("3"); feed("4"); feed(":");
        feed("5"); feed("6"); feed(8'h0A);   // newline

        @(negedge clk);
        if (!got_valid)        begin $error("no valid pulse"); errors++; end
        if (count   !== 3'd6)  begin $error("count = %0d exp 6", count); errors++; end
        // field0=1, field1=2, ... field5=6  -> packed 0x654321
        if (digits  !== 24'h654321) begin $error("digits = %06h exp 654321", digits); errors++; end

        if (errors == 0) $display("ASCII_NUM_PARSER: PASS");
        else             $display("ASCII_NUM_PARSER: FAIL (%0d errors)", errors);
        $finish;
    end

    initial begin #3_000_000; $error("timeout"); $finish; end

endmodule
