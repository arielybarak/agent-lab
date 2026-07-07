// frame_move -- bouncing 2-axis position generator for a sprite.
// Updates pos_x/pos_y by +/-STEP once per frame_tick (wire frame_start from
// vga_sync). Reverses direction at the X/Y bounds (wall bounce). Set the *_MAX
// bounds to (screen_size - sprite_size) so the sprite stays fully on-screen.
// Hold ena low to pause.

module frame_move #(
    parameter signed [11:0] X_MIN   = 0,
    parameter signed [11:0] X_MAX   = 624,   // 640 - 16
    parameter signed [11:0] Y_MIN   = 0,
    parameter signed [11:0] Y_MAX   = 464,   // 480 - 16
    parameter signed [11:0] START_X = 320,
    parameter signed [11:0] START_Y = 240,
    parameter signed [11:0] STEP    = 2
)(
    input  logic              clk,
    input  logic              rst_n,
    input  logic              frame_tick,
    input  logic              ena,
    output logic signed [11:0] pos_x,
    output logic signed [11:0] pos_y
);

    logic signed [11:0] vx, vy;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pos_x <= START_X;
            pos_y <= START_Y;
            vx    <= STEP;
            vy    <= STEP;
        end else if (frame_tick && ena) begin
            // X axis
            if (pos_x + vx <= X_MIN) begin pos_x <= X_MIN; vx <=  STEP; end
            else if (pos_x + vx >= X_MAX) begin pos_x <= X_MAX; vx <= -STEP; end
            else pos_x <= pos_x + vx;
            // Y axis
            if (pos_y + vy <= Y_MIN) begin pos_y <= Y_MIN; vy <=  STEP; end
            else if (pos_y + vy >= Y_MAX) begin pos_y <= Y_MAX; vy <= -STEP; end
            else pos_y <= pos_y + vy;
        end
    end

endmodule
