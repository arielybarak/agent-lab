// echo_top -- minimal UART echo on the DE10-Lite.
// Receives a byte from the ESP32 (ARDUINO_IO[0]) and transmits it straight back
// (ARDUINO_IO[1]). Shows the last received byte on LEDR[7:0]. Reset = KEY[0].
// Built from the uart_rx + uart_tx bricks.

module echo_top (
    input         MAX10_CLK1_50,
    input  [9:0]  SW,
    input  [1:0]  KEY,
    output [9:0]  LEDR,
    output [7:0]  HEX0, HEX1, HEX2, HEX3, HEX4, HEX5,
    inout  [15:0] ARDUINO_IO
);

    wire clk   = MAX10_CLK1_50;
    wire rst_n = KEY[0];

    // Arduino header: IO0 = RX (input), IO1 = TX (output), rest high-Z
    wire rx_pin = ARDUINO_IO[0];
    wire tx_pin;
    assign ARDUINO_IO[0]    = 1'bz;
    assign ARDUINO_IO[1]    = tx_pin;
    assign ARDUINO_IO[15:2] = 14'bz;

    wire [7:0] rx_data;
    wire       rx_valid;
    wire       tx_busy;

    uart_rx #(.CLK_FREQ(50_000_000), .BAUD(9600)) u_rx (
        .clk(clk), .rst_n(rst_n), .rx(rx_pin),
        .rx_data(rx_data), .rx_valid(rx_valid));

    // echo each received byte back as soon as the line is free
    uart_tx #(.CLK_FREQ(50_000_000), .BAUD(9600)) u_tx (
        .clk(clk), .rst_n(rst_n), .tx_start(rx_valid), .tx_data(rx_data),
        .tx(tx_pin), .tx_busy(tx_busy));

    reg [7:0] last;
    always @(posedge clk or negedge rst_n)
        if (!rst_n) last <= 8'h00;
        else if (rx_valid) last <= rx_data;

    assign LEDR = {2'b00, last};
    assign {HEX5, HEX4, HEX3, HEX2, HEX1, HEX0} = {6{8'hFF}};

endmodule
