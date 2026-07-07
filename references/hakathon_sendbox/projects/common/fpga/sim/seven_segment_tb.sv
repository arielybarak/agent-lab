// Self-checking test for seven_segment: digits 0-9 decode, blank works,
// non-digit blanks.
`timescale 1ns/1ps

module seven_segment_tb;

    logic [3:0] data;
    logic       blank;
    logic [7:0] seg;

    seven_segment dut (.data(data), .blank(blank), .seg(seg));

    // expected active-low codes for 0-9
    logic [7:0] expect_tbl [0:9] = '{
        8'b11000000, 8'b11111001, 8'b10100100, 8'b10110000, 8'b10011001,
        8'b10010010, 8'b10000010, 8'b11111000, 8'b10000000, 8'b10010000};

    int errors = 0;

    initial begin
        blank = 0;
        for (int d = 0; d <= 9; d++) begin
            data = d[3:0]; #1;
            if (seg !== expect_tbl[d]) begin
                $error("digit %0d: got %08b exp %08b", d, seg, expect_tbl[d]);
                errors++;
            end
        end

        // blank input forces all-off
        data = 4'd5; blank = 1; #1;
        if (seg !== 8'hFF) begin $error("blank failed: %08b", seg); errors++; end

        // non-digit blanks
        blank = 0; data = 4'hC; #1;
        if (seg !== 8'hFF) begin $error("non-digit not blanked: %08b", seg); errors++; end

        if (errors == 0) $display("SEVEN_SEGMENT: PASS");
        else             $display("SEVEN_SEGMENT: FAIL (%0d errors)", errors);
        $finish;
    end

endmodule
