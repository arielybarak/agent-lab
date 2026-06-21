// UART line receiver -- ASCII protocol helper.
// Wraps uart_rx and accumulates incoming bytes into a line buffer until a
// newline ('\n', 0x0A). On newline it pulses line_valid for 1 cycle with the
// buffered bytes in `line` and the byte count in `len`. '\r' (0x0D) is ignored
// so "HH:MM:SS\r\n" works. Lines longer than MAX_LEN are truncated.
//
// `line` is a flat bus: byte i occupies line[8*i +: 8].

module uart_line_rx #(
    parameter CLK_FREQ = 50_000_000,
    parameter BAUD     = 9600,
    parameter MAX_LEN  = 16
)(
    input  logic                     clk,
    input  logic                     rst_n,
    input  logic                     rx,                 // serial in (ARDUINO_IO[0])
    output logic [8*MAX_LEN-1:0]     line,               // received bytes, byte 0 = LSBs
    output logic [$clog2(MAX_LEN+1)-1:0] len,            // number of valid bytes
    output logic                     line_valid          // 1-cycle pulse on newline
);

    logic [7:0] rx_data;
    logic       rx_valid;

    uart_rx #(.CLK_FREQ(CLK_FREQ), .BAUD(BAUD)) u_rx (
        .clk(clk), .rst_n(rst_n), .rx(rx),
        .rx_data(rx_data), .rx_valid(rx_valid)
    );

    logic [$clog2(MAX_LEN+1)-1:0] count;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            line       <= '0;
            len        <= '0;
            count      <= '0;
            line_valid <= 1'b0;
        end else begin
            line_valid <= 1'b0;
            if (rx_valid) begin
                if (rx_data == 8'h0A) begin            // newline -> commit
                    len        <= count;
                    line_valid <= 1'b1;
                    count      <= '0;
                end else if (rx_data == 8'h0D) begin   // ignore CR
                    // no-op
                end else if (count < MAX_LEN) begin
                    line[8*count +: 8] <= rx_data;
                    count              <= count + 1;
                end
            end
        end
    end

endmodule
