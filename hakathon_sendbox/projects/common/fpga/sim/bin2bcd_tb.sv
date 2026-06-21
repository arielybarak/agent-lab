// Self-checking test for bin2bcd (16-bit -> 5 digits).
`timescale 1ns/1ps

module bin2bcd_tb;

    logic [15:0] bin;
    logic [19:0] bcd;   // 5 nibbles

    bin2bcd #(.WIDTH(16), .DIGITS(5)) dut (.bin(bin), .bcd(bcd));

    int errors = 0;
    task automatic chk(input logic [15:0] v, input logic [19:0] exp);
        bin = v; #1;
        if (bcd !== exp) begin
            $error("bin %0d: got %05h exp %05h", v, bcd, exp);
            errors++;
        end
    endtask

    initial begin
        chk(16'd0,     20'h00000);
        chk(16'd42,    20'h00042);
        chk(16'd999,   20'h00999);
        chk(16'd1234,  20'h01234);
        chk(16'd65535, 20'h65535);
        if (errors == 0) $display("BIN2BCD: PASS");
        else             $display("BIN2BCD: FAIL (%0d errors)", errors);
        $finish;
    end

endmodule
