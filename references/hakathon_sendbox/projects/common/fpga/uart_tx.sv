// UART Transmitter -- 8N1, parametric baud.
// Pulse tx_start for 1 cycle with tx_data valid; module sends start + 8 data
// (LSB first) + stop. tx_busy stays high until the byte is fully shifted out.
// Hold tx_start low while busy. Idle line is high.

module uart_tx #(
    parameter CLK_FREQ = 50_000_000,
    parameter BAUD     = 9600
)(
    input  logic       clk,
    input  logic       rst_n,
    input  logic       tx_start,   // 1-cycle pulse to begin a byte
    input  logic [7:0] tx_data,    // byte to send (sampled when not busy)
    output logic       tx,         // serial output (drive ARDUINO_IO[1])
    output logic       tx_busy     // high while transmitting
);

    localparam CLKS_PER_BIT = CLK_FREQ / BAUD;   // 5208 @ 50 MHz / 9600

    typedef enum logic [1:0] { IDLE, START, DATA, STOP } state_t;
    state_t state;

    logic [15:0] clk_cnt;
    logic [2:0]  bit_idx;
    logic [7:0]  shift_reg;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state     <= IDLE;
            clk_cnt   <= 0;
            bit_idx   <= 0;
            shift_reg <= 0;
            tx        <= 1'b1;   // idle high
            tx_busy   <= 1'b0;
        end else begin
            case (state)
                IDLE: begin
                    tx      <= 1'b1;
                    clk_cnt <= 0;
                    bit_idx <= 0;
                    if (tx_start) begin
                        shift_reg <= tx_data;
                        tx_busy   <= 1'b1;
                        tx        <= 1'b0;   // start bit
                        state     <= START;
                    end else begin
                        tx_busy <= 1'b0;
                    end
                end

                START: begin
                    if (clk_cnt == CLKS_PER_BIT - 1) begin
                        clk_cnt <= 0;
                        tx      <= shift_reg[0];  // first data bit (LSB)
                        state   <= DATA;
                    end else clk_cnt <= clk_cnt + 1;
                end

                DATA: begin
                    if (clk_cnt == CLKS_PER_BIT - 1) begin
                        clk_cnt <= 0;
                        if (bit_idx == 7) begin
                            tx    <= 1'b1;   // stop bit
                            state <= STOP;
                        end else begin
                            bit_idx <= bit_idx + 1;
                            tx      <= shift_reg[bit_idx + 1];
                        end
                    end else clk_cnt <= clk_cnt + 1;
                end

                STOP: begin
                    if (clk_cnt == CLKS_PER_BIT - 1) begin
                        clk_cnt <= 0;
                        tx_busy <= 1'b0;
                        state   <= IDLE;
                    end else clk_cnt <= clk_cnt + 1;
                end
            endcase
        end
    end

endmodule
