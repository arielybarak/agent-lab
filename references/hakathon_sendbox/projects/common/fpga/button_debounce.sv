// Button debouncer + synchronizer for the DE10-Lite KEYs (active-low).
// Synchronizes the async input, then requires it to stay stable for
// DEBOUNCE_CYCLES before accepting a change. Outputs:
//   level      - debounced, active-HIGH "pressed" level
//   press      - 1-cycle pulse on press   (release -> press edge)
//   release_p  - 1-cycle pulse on release
//
// DE10-Lite KEYs read 0 when pressed, so we invert internally.
// Default DEBOUNCE_CYCLES = 1_000_000 -> 20 ms at 50 MHz.

module button_debounce #(
    parameter DEBOUNCE_CYCLES = 1_000_000
)(
    input  logic clk,
    input  logic rst_n,
    input  logic btn_n,        // raw active-low button (e.g. KEY[0])
    output logic level,        // 1 = pressed (debounced)
    output logic press,        // 1-cycle pulse on press
    output logic release_p     // 1-cycle pulse on release
);

    // 2-flop synchronizer, then invert to active-high
    logic s1, s2;
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin s1 <= 1'b1; s2 <= 1'b1; end
        else        begin s1 <= btn_n; s2 <= s1; end
    end
    logic pressed_raw;
    assign pressed_raw = ~s2;

    localparam W = $clog2(DEBOUNCE_CYCLES);
    logic [W-1:0] cnt;
    logic         stable;      // current debounced level

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt       <= '0;
            stable    <= 1'b0;
            level     <= 1'b0;
            press     <= 1'b0;
            release_p <= 1'b0;
        end else begin
            press     <= 1'b0;
            release_p <= 1'b0;
            if (pressed_raw == stable) begin
                cnt <= '0;                       // no change, reset timer
            end else if (cnt == DEBOUNCE_CYCLES - 1) begin
                stable <= pressed_raw;           // accept the new level
                level  <= pressed_raw;
                cnt    <= '0;
                if (pressed_raw) press     <= 1'b1;
                else             release_p <= 1'b1;
            end else begin
                cnt <= cnt + 1;
            end
        end
    end

endmodule
