// Clock divider -- produces a ~50% duty square wave from a fast clock.
// clk_out toggles every COUNT_MAX cycles, so f_out = f_in / (2 * COUNT_MAX).
// Default COUNT_MAX = 25_000_000 -> 1 Hz from 50 MHz.
//
// For a 1-cycle periodic *pulse* (not a divided clock), use tick_gen instead.

module clock_divider #(
    parameter COUNT_MAX = 25_000_000
)(
    input  logic clk,
    input  logic rst_n,
    output logic clk_out
);

    localparam W = (COUNT_MAX <= 1) ? 1 : $clog2(COUNT_MAX);
    logic [W-1:0] cnt;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt     <= '0;
            clk_out <= 1'b0;
        end else if (cnt == COUNT_MAX - 1) begin
            cnt     <= '0;
            clk_out <= ~clk_out;
        end else begin
            cnt <= cnt + 1;
        end
    end

endmodule
