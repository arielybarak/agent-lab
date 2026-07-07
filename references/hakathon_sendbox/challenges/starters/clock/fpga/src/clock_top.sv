// clock_top -- NTP clock display on the DE10-Lite.
// ESP32 streams "HH:MM:SS\n" over UART; we parse the 6 digits and show them on
// HEX5..HEX0 (HH MM SS). Built from uart_rx + ascii_num_parser + hex_display.
// Reset = SW[9] (active-low). Shows 00:00:00 until the first valid line.

module clock_top (
    input         MAX10_CLK1_50,
    input  [9:0]  SW,
    input  [1:0]  KEY,
    output [9:0]  LEDR,
    output [7:0]  HEX0, HEX1, HEX2, HEX3, HEX4, HEX5,
    inout  [15:0] ARDUINO_IO
);

    wire clk   = MAX10_CLK1_50;
    wire rst_n = SW[9];

    // Arduino header: IO0 = RX from ESP32, rest high-Z
    wire rx_pin = ARDUINO_IO[0];
    assign ARDUINO_IO[0]    = 1'bz;
    assign ARDUINO_IO[1]    = 1'bz;
    assign ARDUINO_IO[15:2] = 14'bz;
    assign LEDR = 10'b0;

    wire [7:0] rx_data;
    wire       rx_valid;
    uart_rx #(.CLK_FREQ(50_000_000), .BAUD(9600)) u_rx (
        .clk(clk), .rst_n(rst_n), .rx(rx_pin),
        .rx_data(rx_data), .rx_valid(rx_valid));

    // field0..field5 = first..last digit received = H tens, H ones, M tens, ...
    wire [23:0] fields;
    wire [2:0]  count;
    wire        valid;
    ascii_num_parser #(.FIELDS(6)) u_parse (
        .clk(clk), .rst_n(rst_n), .byte_in(rx_data), .byte_valid(rx_valid),
        .digits(fields), .count(count), .valid(valid));

    // latch on each valid line
    reg [23:0] shown;
    always @(posedge clk or negedge rst_n)
        if (!rst_n)      shown <= 24'h000000;
        else if (valid)  shown <= fields;

    // hex_display nibble i -> HEXi, so put field0 (H tens) in the top nibble:
    // value = {field0, field1, field2, field3, field4, field5}
    wire [23:0] value = {shown[3:0],   shown[7:4],   shown[11:8],
                         shown[15:12], shown[19:16], shown[23:20]};

    hex_display #(.LEADING_ZERO_BLANK(0)) u_disp (
        .value(value),
        .HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2),
        .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5));

endmodule
