// Self-checking test for hex_display: digit placement + leading-zero blanking.
`timescale 1ns/1ps

module hex_display_tb;

    logic [23:0] value;
    logic [7:0]  HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;

    hex_display #(.LEADING_ZERO_BLANK(1)) dut (
        .value(value), .HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2),
        .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5));

    // local copy of the decode table (0-F)
    function automatic logic [7:0] dec(input logic [3:0] d);
        case (d)
            4'h0: dec=8'b1100_0000; 4'h1: dec=8'b1111_1001; 4'h2: dec=8'b1010_0100;
            4'h3: dec=8'b1011_0000; 4'h4: dec=8'b1001_1001; 4'h5: dec=8'b1001_0010;
            4'h6: dec=8'b1000_0010; 4'h7: dec=8'b1111_1000; 4'h8: dec=8'b1000_0000;
            4'h9: dec=8'b1001_0000; 4'hA: dec=8'b1000_1000; 4'hB: dec=8'b1000_0011;
            4'hC: dec=8'b1100_0110; 4'hD: dec=8'b1010_0001; 4'hE: dec=8'b1000_0110;
            4'hF: dec=8'b1000_1110; default: dec=8'hFF;
        endcase
    endfunction

    int errors = 0;
    task automatic chk(input string name, input logic [7:0] got, exp);
        if (got !== exp) begin $error("%s: got %08b exp %08b", name, got, exp); errors++; end
    endtask

    initial begin
        // 0x000042 -> "    42", high 4 digits blanked
        value = 24'h000042; #1;
        chk("HEX0", HEX0, dec(4'h2));
        chk("HEX1", HEX1, dec(4'h4));
        chk("HEX2", HEX2, 8'hFF);
        chk("HEX5", HEX5, 8'hFF);

        // 0 -> "     0", least-significant digit never blanked
        value = 24'h000000; #1;
        chk("zero HEX0", HEX0, dec(4'h0));
        chk("zero HEX1", HEX1, 8'hFF);

        // full hex value, no blanking
        value = 24'hABCDEF; #1;
        chk("full HEX0", HEX0, dec(4'hF));
        chk("full HEX5", HEX5, dec(4'hA));

        if (errors == 0) $display("HEX_DISPLAY: PASS");
        else             $display("HEX_DISPLAY: FAIL (%0d errors)", errors);
        $finish;
    end

endmodule
