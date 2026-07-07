// Two-flip-flop synchronizer for crossing async signals into `clk` domain.
// Use on every async/cross-domain input (raw UART rx, async switches) to avoid
// metastability. WIDTH lets you sync a small bus (each bit independently).

module sync_2ff #(
    parameter WIDTH    = 1,
    parameter RST_VAL  = 1'b0   // value held during reset (per bit)
)(
    input  logic             clk,
    input  logic             rst_n,
    input  logic [WIDTH-1:0] d,
    output logic [WIDTH-1:0] q
);

    logic [WIDTH-1:0] meta;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            meta <= {WIDTH{RST_VAL}};
            q    <= {WIDTH{RST_VAL}};
        end else begin
            meta <= d;
            q    <= meta;
        end
    end

endmodule
