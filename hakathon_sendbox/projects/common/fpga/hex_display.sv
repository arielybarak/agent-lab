// Six-digit display driver for HEX0..HEX5.
// Takes a 24-bit value and shows it as 6 hex nibbles (0-F), driving the six
// active-low 7-segment outputs. Set DECIMAL=1 and feed a packed BCD value
// (6 nibbles, each 0-9) to show decimal instead -- the decoder handles 0-9
// identically either way.
//
// LEADING_ZERO_BLANK=1 blanks high-order zero digits (e.g. 0x000042 -> "  42"),
// but never blanks digit 0 so a value of 0 still shows "0".

module hex_display #(
    parameter LEADING_ZERO_BLANK = 1,
    parameter DECIMAL            = 0   // documentation only; decode is 0-F
)(
    input  logic [23:0] value,
    output logic [7:0]  HEX0,
    output logic [7:0]  HEX1,
    output logic [7:0]  HEX2,
    output logic [7:0]  HEX3,
    output logic [7:0]  HEX4,
    output logic [7:0]  HEX5
);

    // active-low {DP,G,F,E,D,C,B,A}; 0 = segment on
    function automatic logic [7:0] decode(input logic [3:0] d);
        case (d)
            4'h0: decode = 8'b1100_0000;
            4'h1: decode = 8'b1111_1001;
            4'h2: decode = 8'b1010_0100;
            4'h3: decode = 8'b1011_0000;
            4'h4: decode = 8'b1001_1001;
            4'h5: decode = 8'b1001_0010;
            4'h6: decode = 8'b1000_0010;
            4'h7: decode = 8'b1111_1000;
            4'h8: decode = 8'b1000_0000;
            4'h9: decode = 8'b1001_0000;
            4'hA: decode = 8'b1000_1000;
            4'hB: decode = 8'b1000_0011;
            4'hC: decode = 8'b1100_0110;
            4'hD: decode = 8'b1010_0001;
            4'hE: decode = 8'b1000_0110;
            4'hF: decode = 8'b1000_1110;
            default: decode = 8'b1111_1111;
        endcase
    endfunction

    logic [3:0] nib [0:5];
    logic [7:0] raw [0:5];
    logic       blank [0:5];

    always_comb begin
        integer i;
        logic seen_nonzero;
        for (i = 0; i < 6; i = i + 1)
            nib[i] = value[4*i +: 4];

        // leading-zero blanking, scanning from the most-significant digit (5)
        seen_nonzero = 1'b0;
        for (i = 5; i >= 0; i = i - 1) begin
            if (nib[i] != 4'h0) seen_nonzero = 1'b1;
            // blank only high zeros, and never the least-significant digit
            blank[i] = (LEADING_ZERO_BLANK != 0) && !seen_nonzero && (i != 0);
            raw[i]   = blank[i] ? 8'hFF : decode(nib[i]);
        end
    end

    assign HEX0 = raw[0];
    assign HEX1 = raw[1];
    assign HEX2 = raw[2];
    assign HEX3 = raw[3];
    assign HEX4 = raw[4];
    assign HEX5 = raw[5];

endmodule
