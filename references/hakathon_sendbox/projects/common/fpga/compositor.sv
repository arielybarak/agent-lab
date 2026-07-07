// compositor -- priority mux for two sprite layers over a background.
// z-order: sprite 1 (front) > sprite 2 > background. A layer shows only where
// its `draw` is high. Output is 4-4-4 RGB; split into red/green/blue for the
// DE10-Lite DAC (each 4 bits). Extend with more layers as needed.

module compositor (
    input  logic [11:0] bg_rgb,
    input  logic [11:0] s1_rgb,
    input  logic        s1_draw,
    input  logic [11:0] s2_rgb,
    input  logic        s2_draw,
    output logic [11:0] rgb,
    output logic [3:0]  red,
    output logic [3:0]  green,
    output logic [3:0]  blue
);

    assign rgb = s1_draw ? s1_rgb :
                 s2_draw ? s2_rgb :
                           bg_rgb;

    assign red   = rgb[11:8];
    assign green = rgb[7:4];
    assign blue  = rgb[3:0];

endmodule
