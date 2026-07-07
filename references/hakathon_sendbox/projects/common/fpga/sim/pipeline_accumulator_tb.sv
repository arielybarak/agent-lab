// Self-checking test for pipeline_accumulator: sum 4 values -> 100.
`timescale 1ns/1ps

module pipeline_accumulator_tb;

    logic        clk = 0, rst_n = 0, start = 0, in_valid = 0;
    logic [4:0]  num_inputs = 0;
    logic [31:0] data_in = 0, data_out;
    logic        done, busy;

    pipeline_accumulator #(.WIDTH(32), .MAXN(16)) dut (
        .clk(clk), .rst_n(rst_n), .start(start), .num_inputs(num_inputs),
        .data_in(data_in), .in_valid(in_valid), .data_out(data_out),
        .done(done), .busy(busy));

    always #10 clk = ~clk;

    int  errors = 0;
    logic got_done = 0;
    always @(posedge clk) if (done) got_done = 1;

    task automatic feed(input logic [31:0] v);
        @(negedge clk); data_in = v; in_valid = 1;
        @(negedge clk); in_valid = 0;
    endtask

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1;
        @(negedge clk);

        num_inputs = 4; start = 1; @(negedge clk); start = 0;
        feed(32'd10); feed(32'd20); feed(32'd30); feed(32'd40);
        @(negedge clk);

        if (!got_done)              begin $error("no done pulse"); errors++; end
        if (data_out !== 32'd100)   begin $error("sum=%0d exp 100", data_out); errors++; end

        if (errors == 0) $display("PIPELINE_ACCUMULATOR: PASS");
        else             $display("PIPELINE_ACCUMULATOR: FAIL (%0d errors)", errors);
        $finish;
    end

    initial begin #2_000_000; $error("timeout"); $finish; end

endmodule
