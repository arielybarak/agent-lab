// packet_decoder -- framed binary protocol (optional alternative to ASCII).
// Frame: [0xAA][len][cmd][payload(len bytes)][crc8]
//   crc8 = CRC-8 (poly 0x07, init 0x00) over { len, cmd, payload }.
// Feed the byte stream from uart_rx (byte_in + byte_valid). On a complete,
// CRC-valid frame, pulses `valid` with cmd, len, and payload (flat bus, byte 0
// in the low bits). `crc_err` pulses on a bad checksum. Matches packet.h on the
// ESP32 side.

module packet_decoder #(
    parameter MAXP = 16     // max payload bytes
)(
    input  logic                 clk,
    input  logic                 rst_n,
    input  logic [7:0]           byte_in,
    input  logic                 byte_valid,
    output logic [7:0]           cmd,
    output logic [$clog2(MAXP+1)-1:0] len,
    output logic [8*MAXP-1:0]    payload,
    output logic                 valid,
    output logic                 crc_err
);

    function automatic logic [7:0] crc8_upd(input logic [7:0] crc, input logic [7:0] data);
        logic [7:0] c;
        c = crc ^ data;
        for (int i = 0; i < 8; i++)
            c = c[7] ? ((c << 1) ^ 8'h07) : (c << 1);
        return c;
    endfunction

    typedef enum logic [2:0] { SYNC, LEN, CMD, PAY, CRC } state_t;
    state_t state;

    logic [7:0]                    crc_acc;
    logic [7:0]                    len_r;
    logic [$clog2(MAXP+1)-1:0]     idx;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state   <= SYNC;
            crc_acc <= 8'h00;
            len_r   <= 8'h00;
            idx     <= '0;
            cmd     <= 8'h00;
            len     <= '0;
            payload <= '0;
            valid   <= 1'b0;
            crc_err <= 1'b0;
        end else begin
            valid   <= 1'b0;
            crc_err <= 1'b0;
            if (byte_valid) begin
                case (state)
                    SYNC: if (byte_in == 8'hAA) begin
                        crc_acc <= 8'h00;
                        state   <= LEN;
                    end
                    LEN: begin
                        if (byte_in > MAXP) begin
                            state <= SYNC;            // too long, drop
                        end else begin
                            len_r   <= byte_in;
                            len     <= byte_in[$clog2(MAXP+1)-1:0];
                            crc_acc <= crc8_upd(crc_acc, byte_in);
                            idx     <= '0;
                            state   <= CMD;
                        end
                    end
                    CMD: begin
                        cmd     <= byte_in;
                        crc_acc <= crc8_upd(crc_acc, byte_in);
                        state   <= (len_r == 0) ? CRC : PAY;
                    end
                    PAY: begin
                        payload[8*idx +: 8] <= byte_in;
                        crc_acc <= crc8_upd(crc_acc, byte_in);
                        if (idx == len_r - 1) state <= CRC;
                        idx <= idx + 1;
                    end
                    CRC: begin
                        if (byte_in == crc_acc) valid   <= 1'b1;
                        else                    crc_err <= 1'b1;
                        state <= SYNC;
                    end
                endcase
            end
        end
    end

endmodule
