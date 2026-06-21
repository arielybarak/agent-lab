// ============================================================
// CrashTech VLSI-2026 — DE10-Lite FPGA UART pin contract
// ============================================================
// Mirror of projects/common/esp32/pin_config.h (FPGA side).
// Keep both files in sync — drift here causes silent UART failures.
//
// UART to ESP32 over the DE10-Lite *Arduino header* (NOT JP1 GPIO):
//   ARDUINO_IO[0] = FPGA RX  <- ESP32 TX (ESP32 GPIO16)
//   ARDUINO_IO[1] = FPGA TX  -> ESP32 RX (ESP32 GPIO17)
//   GND: tie ESP32 GND to an Arduino-header GND pin.
//   9600 baud, 8N1, 3.3V logic.
//   All unused ARDUINO_IO pins must be driven high-Z (1'bz).
// ============================================================
`ifndef CRASHTECH_PINS_SVH
`define CRASHTECH_PINS_SVH

// ---- UART bit indices into ARDUINO_IO ----
localparam int FPGA_RX_IO   = 0;     // ARDUINO_IO[0], PIN_AB5
localparam int FPGA_TX_IO   = 1;     // ARDUINO_IO[1], PIN_AB6

// ---- UART timing ----
localparam int CLK_HZ       = 50_000_000;  // MAX10_CLK1_50
localparam int FPGA_BAUD    = 9600;        // 9600 8N1
localparam int CLKS_PER_BIT = CLK_HZ / FPGA_BAUD;  // 5208

`endif // CRASHTECH_PINS_SVH
