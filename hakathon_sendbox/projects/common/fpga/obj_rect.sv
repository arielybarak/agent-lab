// obj_rect -- rectangle bounds checker for sprites / hit-testing.
// `drawing` is high when the current pixel is inside the WIDTH x HEIGHT box whose
// top-left corner is (topleft_x, topleft_y). Coordinates are SIGNED so a sprite
// can be partly off-screen (negative). offset_x/y give the pixel's position
// within the box (use it to index a bitmap).

module obj_rect #(
    parameter WIDTH  = 16,
    parameter HEIGHT = 16
)(
    input  logic signed [11:0] pixel_x,
    input  logic signed [11:0] pixel_y,
    input  logic signed [11:0] topleft_x,
    input  logic signed [11:0] topleft_y,
    output logic               drawing,
    output logic        [11:0] offset_x,
    output logic        [11:0] offset_y
);

    logic signed [12:0] dx, dy;

    assign dx       = pixel_x - topleft_x;
    assign dy       = pixel_y - topleft_y;
    assign drawing  = (dx >= 0) && (dx < WIDTH) && (dy >= 0) && (dy < HEIGHT);
    assign offset_x = dx[11:0];
    assign offset_y = dy[11:0];

endmodule
