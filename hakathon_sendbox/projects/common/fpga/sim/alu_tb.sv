// Self-checking test for the Hack alu: a few standard operations + flags.
`timescale 1ns/1ps

module alu_tb;

    logic [15:0] x, y, out;
    logic        zx, nx, zy, ny, f, no, zr, ng;

    alu dut (.x(x), .y(y), .zx(zx), .nx(nx), .zy(zy), .ny(ny), .f(f), .no(no),
             .out(out), .zr(zr), .ng(ng));

    int errors = 0;
    task automatic op(input logic [5:0] ctrl);
        {zx, nx, zy, ny, f, no} = ctrl; #1;
    endtask
    task automatic chk(input string n, input logic [15:0] exp);
        if (out !== exp) begin $error("%s: out=%0d exp %0d", n, $signed(out), $signed(exp)); errors++; end
    endtask

    initial begin
        x = 16'd7; y = 16'd5;

        op(6'b101010); chk("zero", 16'd0);
        if (!zr) begin $error("zr not set for 0"); errors++; end
        op(6'b001100); chk("x", 16'd7);
        op(6'b110000); chk("y", 16'd5);
        op(6'b000010); chk("x+y", 16'd12);
        op(6'b000000); chk("x&y", 16'd7 & 16'd5);
        op(6'b010011); chk("x-y", 16'd2);

        // negative result sets ng
        x = 16'd3; y = 16'd9; op(6'b010011); #1;  // x - y = -6
        if (!ng) begin $error("ng not set for negative"); errors++; end

        if (errors == 0) $display("ALU: PASS");
        else             $display("ALU: FAIL (%0d errors)", errors);
        $finish;
    end

endmodule
