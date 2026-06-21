// bcd_counter -- DIGITS-wide BCD up-counter with ripple carry.
// Pulse `inc` (1 cycle) to add one. Each nibble counts 0-9 then carries to the
// next; wraps at all-nines. Output is packed BCD (nibble 0 = ones).
// Drive a display straight from `bcd` via hex_display.

module bcd_counter #(
    parameter DIGITS = 4
)(
    input  logic                clk,
    input  logic                rst_n,
    input  logic                inc,      // 1-cycle pulse = +1
    output logic [4*DIGITS-1:0] bcd
);

    logic carry;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bcd <= '0;
        end else if (inc) begin
            carry = 1'b1;                       // ones digit always increments
            for (int d = 0; d < DIGITS; d++) begin
                if (carry) begin
                    if (bcd[4*d +: 4] == 4'd9) begin
                        bcd[4*d +: 4] <= 4'd0;
                        carry = 1'b1;           // propagate to next digit
                    end else begin
                        bcd[4*d +: 4] <= bcd[4*d +: 4] + 4'd1;
                        carry = 1'b0;
                    end
                end
            end
        end
    end

endmodule
