// periphery_control -- turn raw 12-bit ADC joystick axes into direction flags.
// Pure combinational thresholding (no IP). Feed it the joystick X/Y channel
// values coming out of the ADC (see adc.README.md for the analog_input FSM +
// Qsys ADC IP that produces them). A centered stick sits near mid-scale (2048);
// past LOW_TH / HIGH_TH we assert the direction.
//
// `wheel` is passed through for use as an analog position (e.g. paddle X).

module periphery_control #(
    parameter [11:0] LOW_TH  = 12'd1365,   // ~1/3 of 4095
    parameter [11:0] HIGH_TH = 12'd2730    // ~2/3 of 4095
)(
    input  logic [11:0] joy_x,
    input  logic [11:0] joy_y,
    input  logic [11:0] wheel_in,
    output logic        left,
    output logic        right,
    output logic        up,
    output logic        down,
    output logic [11:0] wheel
);

    assign left  = (joy_x < LOW_TH);
    assign right = (joy_x > HIGH_TH);
    assign up    = (joy_y < LOW_TH);
    assign down  = (joy_y > HIGH_TH);
    assign wheel = wheel_in;

endmodule
