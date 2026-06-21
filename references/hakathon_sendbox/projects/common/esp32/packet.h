// packet.h -- framed binary protocol, ESP32 side (matches packet_decoder.sv).
// Frame: [0xAA][len][cmd][payload(len)][crc8], crc8 = CRC-8 poly 0x07 init 0x00
// over { len, cmd, payload }. Use only when ASCII lines are too slow / you need
// binary payloads; otherwise prefer uart_fpga.h.
//
// Usage (send):
//   PacketIO pkt(fpga.raw());           // any Stream& (HardwareSerial)
//   uint8_t body[2] = {0x12, 0x34};
//   pkt.send(0x05, body, 2);
//
// Usage (receive): call pkt.poll() each loop; returns true once per good frame.
//   if (pkt.poll()) { uint8_t c = pkt.cmd(); const uint8_t* p = pkt.payload(); }
#pragma once
#include <Arduino.h>

class PacketIO {
public:
    static const uint8_t SYNC = 0xAA;
    static const uint8_t MAXP = 32;

    explicit PacketIO(Stream& io) : _io(io) {}

    static uint8_t crc8(const uint8_t* data, size_t n) {
        uint8_t c = 0x00;
        for (size_t i = 0; i < n; i++) {
            c ^= data[i];
            for (int b = 0; b < 8; b++)
                c = (c & 0x80) ? (uint8_t)((c << 1) ^ 0x07) : (uint8_t)(c << 1);
        }
        return c;
    }

    void send(uint8_t cmd, const uint8_t* payload, uint8_t len) {
        uint8_t hdr[2] = { len, cmd };
        uint8_t crc = crc8(hdr, 2);
        crc = crcContinue(crc, payload, len);
        _io.write(SYNC);
        _io.write(len);
        _io.write(cmd);
        if (len) _io.write(payload, len);
        _io.write(crc);
    }

    // Non-blocking receive. Returns true once when a CRC-valid frame arrives.
    bool poll() {
        while (_io.available()) {
            uint8_t b = (uint8_t)_io.read();
            switch (_st) {
                case S_SYNC: if (b == SYNC) { _crc = 0; _st = S_LEN; } break;
                case S_LEN:
                    if (b > MAXP) { _st = S_SYNC; }
                    else { _len = b; _crc = crc8(&b, 1); _idx = 0; _st = S_CMD; }
                    break;
                case S_CMD:
                    _cmd = b; _crc = step(_crc, b);
                    _st = (_len == 0) ? S_CRC : S_PAY;
                    break;
                case S_PAY:
                    _pay[_idx++] = b; _crc = step(_crc, b);
                    if (_idx == _len) _st = S_CRC;
                    break;
                case S_CRC:
                    _st = S_SYNC;
                    if (b == _crc) return true;   // good frame
                    break;
            }
        }
        return false;
    }

    uint8_t        cmd()     const { return _cmd; }
    uint8_t        len()     const { return _len; }
    const uint8_t* payload() const { return _pay; }

private:
    // incremental CRC helpers (same poly as crc8)
    static uint8_t step(uint8_t c, uint8_t data) {
        c ^= data;
        for (int b = 0; b < 8; b++)
            c = (c & 0x80) ? (uint8_t)((c << 1) ^ 0x07) : (uint8_t)(c << 1);
        return c;
    }
    static uint8_t crcContinue(uint8_t c, const uint8_t* data, uint8_t n) {
        for (uint8_t i = 0; i < n; i++) c = step(c, data[i]);
        return c;
    }

    enum St { S_SYNC, S_LEN, S_CMD, S_PAY, S_CRC };
    Stream& _io;
    St      _st  = S_SYNC;
    uint8_t _crc = 0, _len = 0, _cmd = 0, _idx = 0;
    uint8_t _pay[MAXP] = {0};
};
