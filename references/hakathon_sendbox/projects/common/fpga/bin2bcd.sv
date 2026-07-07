// bin2bcd -- combinational binary-to-BCD (double-dabble).
// Converts a WIDTH-bit unsigned value into DIGITS BCD nibbles (packed,
// nibble 0 = least-significant digit). Pair with hex_display (DECIMAL) to show
// a binary count in decimal on the HEX displays.
//
// Make sure DIGITS is big enough: 2^WIDTH-1 must fit (16-bit -> 65535 -> 5 digits).

module bin2bcd #(
    parameter WIDTH  = 16,
    parameter DIGITS = 5
)(
    input  logic [WIDTH-1:0]    bin,
    output logic [4*DIGITS-1:0] bcd
);

    always_comb begin
        bcd = '0;
        for (int i = WIDTH - 1; i >= 0; i--) begin
            // add 3 to any digit currently >= 5
            for (int d = 0; d < DIGITS; d++)
                if (bcd[4*d +: 4] >= 5)
                    bcd[4*d +: 4] = bcd[4*d +: 4] + 4'd3;
            // shift left, bring in the next binary bit
            bcd = {bcd[4*DIGITS-2:0], bin[i]};
        end
    end

endmodule
