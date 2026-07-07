// Self-checking loopback: uart_tx -> uart_rx. Sends several bytes and checks
// each comes back intact. Uses a tiny baud divisor (10 clks/bit) for fast sim.
`timescale 1ns/1ps

module uart_loopback_tb;

    localparam CLK_FREQ = 100_000;
    localparam BAUD     = 10_000;   // CLKS_PER_BIT = 10

    logic clk = 0, rst_n = 0;
    always #10 clk = ~clk;          // 50 MHz-ish period (20 ns)

    logic       tx_start, tx_busy, serial;
    logic [7:0] tx_data;
    logic [7:0] rx_data;
    logic       rx_valid;

    uart_tx #(.CLK_FREQ(CLK_FREQ), .BAUD(BAUD)) dut_tx (
        .clk(clk), .rst_n(rst_n), .tx_start(tx_start), .tx_data(tx_data),
        .tx(serial), .tx_busy(tx_busy));

    uart_rx #(.CLK_FREQ(CLK_FREQ), .BAUD(BAUD)) dut_rx (
        .clk(clk), .rst_n(rst_n), .rx(serial),
        .rx_data(rx_data), .rx_valid(rx_valid));

    int errors = 0;

    task automatic send_check(input logic [7:0] b);
        @(negedge clk);
        tx_data  = b;
        tx_start = 1;
        @(negedge clk);
        tx_start = 0;
        // wait for received byte
        @(posedge rx_valid);
        @(negedge clk);
        if (rx_data !== b) begin
            $error("loopback mismatch: sent %02h got %02h", b, rx_data);
            errors++;
        end else
            $display("  ok: %02h ('%c')", b, b);
        // ensure TX finished before next byte
        wait (!tx_busy);
    endtask

    initial begin
        tx_start = 0; tx_data = 0;
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (4) @(negedge clk);

        send_check(8'h41);   // 'A'
        send_check(8'h0A);   // newline
        send_check(8'h39);   // '9'
        send_check(8'h00);
        send_check(8'hFF);

        if (errors == 0) $display("UART LOOPBACK: PASS");
        else             $display("UART LOOPBACK: FAIL (%0d errors)", errors);
        $finish;
    end

    initial begin
        #5_000_000;
        $error("timeout"); $finish;
    end

endmodule
