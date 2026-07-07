# analog_input — joystick/potentiometer ADC (Qsys IP, not a plain .sv)

The DE10-Lite ADC is read through an Avalon-MM IP generated in **Platform Designer
(Qsys)**, so `analog_input.sv` is an FSM wrapped around generated IP rather than a
standalone module. The pure-logic part — turning channel values into direction
flags — is already provided as `periphery_control.sv`.

## Generate the ADC IP (once)

1. Quartus → **Tools → Platform Designer (Qsys)**.
2. Add **Modular ADC core** (or **ADC**). Configure for the channels your add-on
   board uses (the kit add-on uses up to 6 channels: joystick X/Y, buttons, wheel).
3. Set **sequencer** to read those channels in order; clock the core from a PLL
   (the ADC needs its own clock, often 10 MHz — the IP wizard states the rate).
4. Generate; add the produced `.qip` to your `.qsf`.

## Wire it up

Write a small `analog_input.sv` FSM that walks the sequencer over the Avalon-MM
interface and latches each channel into a register (`ch0..ch5`), respecting
`adc_wait_request`. Then:

```systemverilog
periphery_control u_pc (
    .joy_x(ch_x), .joy_y(ch_y), .wheel_in(ch_wheel),
    .left(left), .right(right), .up(up), .down(down), .wheel(wheel));
```

Full FSM + exact channel mapping + Qsys steps: see the
`de10lite-addon-peripherals` skill ("ADC FSM (analog_input.sv)", "Clean Periphery
Control Wrapper", "Qsys ADC IP Setup").
