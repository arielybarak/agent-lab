// Edge detector -- 1-cycle pulses on rising / falling edges of a synchronous
// signal. Feed it an already-synchronized signal (use sync_2ff first if the
// source is async). `either` pulses on any change.

module edge_detect (
    input  logic clk,
    input  logic rst_n,
    input  logic sig,
    output logic rising,
    output logic falling,
    output logic either
);

    logic sig_d;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) sig_d <= 1'b0;
        else        sig_d <= sig;
    end

    assign rising  =  sig & ~sig_d;
    assign falling = ~sig &  sig_d;
    assign either  =  sig ^  sig_d;

endmodule
