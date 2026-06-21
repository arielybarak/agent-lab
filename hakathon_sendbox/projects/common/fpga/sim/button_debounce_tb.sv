// Self-checking test for button_debounce: bouncy edges produce exactly one
// clean press/release. Small DEBOUNCE_CYCLES so the sim is short.
`timescale 1ns/1ps

module button_debounce_tb;

    localparam DB = 4;   // tiny debounce window

    logic clk = 0, rst_n = 0;
    always #10 clk = ~clk;

    logic btn_n = 1'b1;   // active-low, idle high (not pressed)
    logic level, press, release_p;

    button_debounce #(.DEBOUNCE_CYCLES(DB)) dut (
        .clk(clk), .rst_n(rst_n), .btn_n(btn_n),
        .level(level), .press(press), .release_p(release_p));

    int press_cnt = 0, release_cnt = 0, errors = 0;
    always @(posedge clk) begin
        if (press)     press_cnt++;
        if (release_p) release_cnt++;
    end

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (4) @(negedge clk);

        // bouncy press: jitter then settle low (pressed)
        btn_n = 0; @(negedge clk); btn_n = 1; @(negedge clk);
        btn_n = 0; @(negedge clk); btn_n = 1; @(negedge clk);
        btn_n = 0;                              // settle pressed
        repeat (DB + 6) @(negedge clk);
        if (!level) begin $error("level not high after settle"); errors++; end

        // bouncy release: jitter then settle high (released)
        btn_n = 1; @(negedge clk); btn_n = 0; @(negedge clk);
        btn_n = 1;                              // settle released
        repeat (DB + 6) @(negedge clk);
        if (level) begin $error("level not low after release"); errors++; end

        if (press_cnt !== 1)   begin $error("press pulses = %0d (exp 1)", press_cnt); errors++; end
        if (release_cnt !== 1) begin $error("release pulses = %0d (exp 1)", release_cnt); errors++; end

        if (errors == 0) $display("BUTTON_DEBOUNCE: PASS");
        else             $display("BUTTON_DEBOUNCE: FAIL (%0d errors)", errors);
        $finish;
    end

endmodule
