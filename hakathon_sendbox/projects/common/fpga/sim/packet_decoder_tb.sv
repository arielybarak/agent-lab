// Self-checking test for packet_decoder: a good frame decodes; a bad-CRC frame
// raises crc_err. CRC computed locally with the same poly as the DUT.
`timescale 1ns/1ps

module packet_decoder_tb;

    logic        clk = 0, rst_n = 0;
    logic [7:0]  byte_in = 0;
    logic        byte_valid = 0;
    logic [7:0]  cmd;
    logic [4:0]  len;
    logic [8*16-1:0] payload;
    logic        valid, crc_err;

    packet_decoder #(.MAXP(16)) dut (
        .clk(clk), .rst_n(rst_n), .byte_in(byte_in), .byte_valid(byte_valid),
        .cmd(cmd), .len(len), .payload(payload), .valid(valid), .crc_err(crc_err));

    always #10 clk = ~clk;

    function automatic logic [7:0] crc8_upd(input logic [7:0] crc, input logic [7:0] data);
        logic [7:0] c; c = crc ^ data;
        for (int i = 0; i < 8; i++) c = c[7] ? ((c << 1) ^ 8'h07) : (c << 1);
        return c;
    endfunction

    int   errors = 0;
    logic got_valid = 0, got_err = 0;
    always @(posedge clk) begin
        if (valid)   got_valid = 1;
        if (crc_err) got_err   = 1;
    end

    task automatic feed(input logic [7:0] b);
        @(negedge clk); byte_in = b; byte_valid = 1;
        @(negedge clk); byte_valid = 0;
    endtask

    logic [7:0] crc;
    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1;
        @(negedge clk);

        // good frame: cmd=0x12, payload {0x48,0x69}, len=2
        crc = 8'h00;
        crc = crc8_upd(crc, 8'd2);
        crc = crc8_upd(crc, 8'h12);
        crc = crc8_upd(crc, 8'h48);
        crc = crc8_upd(crc, 8'h69);
        feed(8'hAA); feed(8'd2); feed(8'h12); feed(8'h48); feed(8'h69); feed(crc);
        @(negedge clk);
        if (!got_valid)               begin $error("good frame not valid"); errors++; end
        if (cmd !== 8'h12)            begin $error("cmd=%02h exp 12", cmd); errors++; end
        if (payload[7:0]   !== 8'h48) begin $error("pay0=%02h exp 48", payload[7:0]); errors++; end
        if (payload[15:8]  !== 8'h69) begin $error("pay1=%02h exp 69", payload[15:8]); errors++; end

        // bad frame: same but wrong crc
        feed(8'hAA); feed(8'd1); feed(8'h34); feed(8'hAB); feed(8'h00); // 0x00 != real crc
        @(negedge clk);
        if (!got_err) begin $error("bad CRC not flagged"); errors++; end

        if (errors == 0) $display("PACKET_DECODER: PASS");
        else             $display("PACKET_DECODER: FAIL (%0d errors)", errors);
        $finish;
    end

    initial begin #3_000_000; $error("timeout"); $finish; end

endmodule
