# Quick Start (per session)

Paths use this repo's `challenges/<name>/` layout. Adapt `<name>`/`<project>` per challenge.

## FPGA (DE10-Lite) — re-program every power-on

Compile (WSL or Windows):
```bash
just fpga-build challenges/<name>/fpga <project>
```

Program — **from Windows PowerShell** (Quartus `.exe` can't use WSL paths):
```powershell
cd <repo>\challenges\<name>\fpga
& "C:\intelFPGA_lite\17.1\quartus\bin64\quartus_pgm.exe" -c "USB-Blaster [USB-0]" -m JTAG -o "P;output_files\<project>.sof"
```

## ESP32 (PlatformIO) — firmware persists; reflash after code changes

Build (WSL):
```bash
just esp32-build challenges/<name>/esp32
```

Upload each session, after connecting ESP32 USB:

1. **Windows PowerShell (Admin)** — attach USB to WSL:
   ```powershell
   usbipd attach --wsl --busid 1-1     # run `usbipd list` to find the CP210x busid
   ```
2. **WSL** — load driver + permissions:
   ```bash
   sudo modprobe cp210x
   sudo chmod 666 /dev/ttyUSB0
   ```
3. **WSL** — upload + monitor:
   ```bash
   just esp32-flash   challenges/<name>/esp32 /dev/ttyUSB0
   just esp32-monitor /dev/ttyUSB0 115200
   ```

> If `pio` isn't on PATH, use `~/.platformio/penv/bin/pio` (PlatformIO's bundled CLI).

## Wiring (UART, Arduino header — NOT JP1)

| ESP32 | Direction | FPGA Arduino Header |
|-------|-----------|---------------------|
| GPIO16 | → | ARDUINO_IO[0] (PIN_AB5) |
| GPIO17 | ← | ARDUINO_IO[1] (PIN_AB6) |
| GND | — | GND |

9600 baud, 8N1, 3.3V. Unused `ARDUINO_IO` pins → high-Z (`1'bz`).
