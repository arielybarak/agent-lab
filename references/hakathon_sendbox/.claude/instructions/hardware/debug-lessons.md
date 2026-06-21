# Hardware Debug Lessons — CrashTech VLSI 2026

Accumulated from live debugging sessions (extracted from a teammate's fork). Future agents:
**read this before touching hardware** — especially the 7-step protocol at the bottom.

> Host note for this repo: FPGA recompile/program runs from **Windows PowerShell** (as shown in
> lesson 6); `pio` commands (monitor/upload) run from **WSL** after `usbipd attach --wsl`
> (see `SETUP_QUICKSTART.md`). The procedures below are otherwise host-agnostic.

---

## ESP32

### 1. `pin_config.h` absent from repo
`projects/common/esp32/pin_config.h` is not committed (or was missing). All ESP32 projects depend on it.
Recreate from `.copilot/skills/esp32-firmware/SKILL.md` BKM section if absent.
Canonical values: TX=16, RX=17, OLED SDA=21, SCL=22, LED1=23, LED2=2, LED3=15, Buzzer=19, SW1=4, SW2=0, Servo=18, ADC=34, Baud=9600.

### 2. GPIO0 boot strap — boot loop symptom
`PIN_SW_2 = GPIO0` is the ESP32 boot select strap.
**Holding GPIO0 LOW at power-on → ROM enters download mode → app never runs → boot loop.**
Symptom: serial shows garbage bytes (ROM at 74880 baud mis-decoded at 115200) then repeated `rst:ets Jul 29 2019 12:21:46`.
Fix: release SW2, press EN button. Do not hold SW2 during power-on or upload.

### 3. Silkscreen TXD/RXD ≠ UART2
ESP32 DevKit V1 silkscreen `TXD`/`RXD` labels = **GPIO1/GPIO3** (USB-serial debug, 115200 baud).
FPGA UART uses **HardwareSerial(2)** on **GPIO16 (TX) / GPIO17 (RX)**.
Wiring to silkscreen pins: FPGA sees 115200 garbage → HEX1 never updates. ESP sees nothing from FPGA.
Fix: count pins physically. GPIO16 = 7th pin from USB end on right side of 38-pin DevKit.

### 4. `pio device monitor` resets ESP32 on close
CP2102 USB-serial controls ESP32 EN/GPIO0 via RTS/DTR.
Monitor disconnect pulses RTS → ESP32 resets. Looks like freeze/crash.
Fix — add to `platformio.ini`:
```ini
monitor_rts = 0
monitor_dtr = 0
```
Already applied in `demos/alive_test/esp32/platformio.ini`.

### 5. UART2 loopback test procedure
To verify GPIO16/17 are correct physical pins and UART2 works:
1. Bridge GPIO16 ↔ GPIO17 with short wire (disconnect from FPGA first).
2. Run `pio device monitor`.
3. Expect `[FPGA RAW]` lines echoing ESP's own countdown.
No echo = wrong physical pins or broken wire.

---

## FPGA (DE10-Lite / MAX 10)

### 6. Prebuilt `.sof` may be stale
`output_files/alive_test.sof` committed to repo may predate `.sv` changes.
**Always recompile before debugging IO issues:**
```powershell
cd demos\alive_test\fpga
& "C:\intelFPGA_lite\17.1\quartus\bin64\quartus_sh.exe" --flow compile alive_test
```
Stale bitstream symptom: HEX0 counts (timer logic fine) but IO pins don't respond.

### 7. FPGA loopback test procedure
To verify FPGA TX/RX IO work independently of cross-board wiring:
1. Bridge ARDUINO_IO[0] ↔ ARDUINO_IO[1] on DE10-Lite Arduino header (adjacent pins).
2. Power cycle or reprogram FPGA.
3. HEX1 should mirror HEX0 within ~2 seconds.
No mirror = FPGA TX not driving IO1 or RX not reading IO0. Recompile `.sof`.

### 8. Warning 13035 — harmless tri-state buffer insertion
```
Warning (13035): Inserted always-enabled tri-state buffer between "ARDUINO_IO[1]" and its non-tri-state driver.
```
Caused by driving `inout` port with non-tristate signal. Output still correctly driven. Ignore.

---

## Cross-Board Wiring

### 9. Correct pinout
| ESP32 GPIO | Direction | FPGA Arduino Header | FPGA Pin |
|------------|-----------|---------------------|----------|
| GPIO16     | → TX      | IO[0]               | PIN_AB5  |
| GPIO17     | ← RX      | IO[1]               | PIN_AB6  |
| GND        | —         | GND                 | —        |

### 10. Both directions dead = check GND first
Most common cause of both FPGA→ESP and ESP→FPGA failing simultaneously: missing or loose common ground.
Verify GND wire continuity between ESP GND and FPGA Arduino header GND pin before anything else.

### 11. Debug signal map (alive_test)
| Observable | Meaning |
|------------|---------|
| HEX0 counting 0→9 | FPGA clock + timer OK |
| HEX1 showing digit | FPGA received byte from ESP |
| LEDR[9] toggling | Raw ESP TX line active on FPGA IO[0] |
| LEDR[8] toggling | FPGA UART RX decoded valid byte |
| `[FPGA RAW]` in ESP serial | ESP received byte from FPGA |
| `ESP32->FPGA:` in ESP serial | ESP UART2 TX firing |

---

## Debug Protocol — Both Directions Dead

Run in order, stop when you find the break:

1. **HEX0 counting?** No → FPGA bitstream bad or in reset (KEY[0] held). Recompile + reprogram.
2. **FPGA loopback** (IO0↔IO1 bridge) → HEX1 mirrors HEX0? No → recompile `.sof` (lesson 6).
3. **ESP serial alive?** (`pio device monitor` shows banner) No → boot loop (lesson 2) or wrong COM port.
4. **`ESP32->FPGA:` lines appear?** No → UART2 not initialized.
5. **ESP loopback** (GPIO16↔GPIO17 bridge) → `[FPGA RAW]` appears? No → wrong physical pins (lesson 3).
6. **LEDR[9] toggling with wires connected?** No → loose wire on FPGA IO[0] or GND missing (lesson 10).
7. If all pass but still no link → swap TX/RX wires (may be crossed).

---

## Adding Lessons

Append new `### N. Title` sections to this file after each debug session.
Update the pointer in `CLAUDE.md` if a new category is added.
