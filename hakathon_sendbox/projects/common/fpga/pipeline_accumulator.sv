// pipeline_accumulator -- sum a stream of N values with a single adder (the
// constrained-datapath pattern from the board-and-build skill).
// Protocol: pulse `start` with `num_inputs` (1..MAX) set. Then present each
// value on `data_in` and pulse `in_valid` once per value. After the Nth value,
// `done` pulses for 1 cycle and `data_out` holds the sum.

module pipeline_accumulator #(
    parameter WIDTH = 32,
    parameter MAXN  = 16
)(
    input  logic                    clk,
    input  logic                    rst_n,
    input  logic                    start,
    input  logic [$clog2(MAXN+1)-1:0] num_inputs,
    input  logic [WIDTH-1:0]        data_in,
    input  logic                    in_valid,
    output logic [WIDTH-1:0]        data_out,
    output logic                    done,
    output logic                    busy
);

    typedef enum logic [1:0] { IDLE, ACC, FINISH } state_t;
    state_t state;

    logic [$clog2(MAXN+1)-1:0] remaining;
    logic [WIDTH-1:0]          acc;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state     <= IDLE;
            acc       <= '0;
            remaining <= '0;
            data_out  <= '0;
            done      <= 1'b0;
            busy      <= 1'b0;
        end else begin
            done <= 1'b0;
            case (state)
                IDLE: begin
                    busy <= 1'b0;
                    if (start && num_inputs != 0) begin
                        acc       <= '0;
                        remaining <= num_inputs;
                        busy      <= 1'b1;
                        state     <= ACC;
                    end
                end
                ACC: begin
                    if (in_valid) begin
                        acc       <= acc + data_in;     // the single shared adder
                        remaining <= remaining - 1;
                        if (remaining == 1) state <= FINISH;
                    end
                end
                FINISH: begin
                    data_out <= acc;
                    done     <= 1'b1;
                    busy     <= 1'b0;
                    state    <= IDLE;
                end
            endcase
        end
    end

endmodule
