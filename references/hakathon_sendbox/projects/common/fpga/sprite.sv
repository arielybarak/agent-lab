// sprite -- a solid-color rectangular sprite (the simplest "draw" unit).
// Give it the current pixel and the sprite's top-left position; it reports
// `drawing` and the sprite color. Move it by driving pos_x/pos_y from a
// register (e.g. frame_move or a joystick). For bitmaps, replace the constant
// COLOR with a ROM lookup using obj_rect's offset_x/offset_y (see vga skill).

module sprite #(
    parameter        WIDTH  = 16,
    parameter        HEIGHT = 16,
    parameter [11:0] COLOR  = 12'hF00   // 4-4-4 RGB
)(
    input  logic signed [11:0] pixel_x,
    input  logic signed [11:0] pixel_y,
    input  logic signed [11:0] pos_x,
    input  logic signed [11:0] pos_y,
    output logic               drawing,
    output logic        [11:0] rgb
);

    obj_rect #(.WIDTH(WIDTH), .HEIGHT(HEIGHT)) u_box (
        .pixel_x(pixel_x), .pixel_y(pixel_y),
        .topleft_x(pos_x), .topleft_y(pos_y),
        .drawing(drawing), .offset_x(), .offset_y());

    assign rgb = COLOR;

endmodule
