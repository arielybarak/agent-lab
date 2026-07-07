// ascii_num_parser -- pull digit fields out of an ASCII line.
// Feed it the byte stream from uart_rx (byte_in + byte_valid). It captures the
// digit characters '0'..'9', ignores any non-digit separators (':', spaces,
// etc.), and on a line end ('\n' or '\r') pulses `valid` with the digits packed
// in `digits` (nibble 0 = first digit received) and how many in `count`.
//
// Example: "12:34:56\n" -> digits = {6,5,4,3,2,1} (field0=1..field5=6), count=6.
// Generalizes the HH:MM:SS parser from the internet_clock demo.

module ascii_num_parser #(
    parameter FIELDS = 6
)(
    input  logic                          clk,
    input  logic                          rst_n,
    input  logic [7:0]                    byte_in,
    input  logic                          byte_valid,
    output logic [4*FIELDS-1:0]           digits,
    output logic [$clog2(FIELDS+1)-1:0]   count,
    output logic                          valid       // 1-cycle pulse on line end
);

    logic [4*FIELDS-1:0]         acc;
    logic [$clog2(FIELDS+1)-1:0] idx;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            acc    <= '0;
            idx    <= '0;
            digits <= '0;
            count  <= '0;
            valid  <= 1'b0;
        end else begin
            valid <= 1'b0;
            if (byte_valid) begin
                if (byte_in == 8'h0A || byte_in == 8'h0D) begin   // line end
                    if (idx != 0) begin
                        digits <= acc;
                        count  <= idx;
                        valid  <= 1'b1;
                    end
                    acc <= '0;
                    idx <= '0;
                end else if (byte_in >= 8'h30 && byte_in <= 8'h39) begin  // '0'..'9'
                    if (idx < FIELDS) begin
                        acc[4*idx +: 4] <= byte_in[3:0];
                        idx             <= idx + 1;
                    end
                end
                // any other byte (':', ' ', ...) is ignored
            end
        end
    end

endmodule
