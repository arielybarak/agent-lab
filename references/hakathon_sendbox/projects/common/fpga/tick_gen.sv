// Periodic tick generator -- asserts `tick` for exactly 1 clock cycle every
// COUNT cycles. Default COUNT = 50_000_000 -> one tick per second at 50 MHz.
// Use for "do X once per second/frame" timing.

module tick_gen #(
    parameter COUNT = 50_000_000
)(
    input  logic clk,
    input  logic rst_n,
    output logic tick
);

    localparam W = (COUNT <= 1) ? 1 : $clog2(COUNT);
    logic [W-1:0] cnt;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt  <= '0;
            tick <= 1'b0;
        end else if (cnt == COUNT - 1) begin
            cnt  <= '0;
            tick <= 1'b1;
        end else begin
            cnt  <= cnt + 1;
            tick <= 1'b0;
        end
    end

endmodule
