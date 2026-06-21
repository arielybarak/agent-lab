// alu -- the nand2tetris "Hack" ALU (16-bit), a self-contained combinational
// block. Six control bits select the function; zr/ng are status flags.
//   zx: zero x      nx: negate x
//   zy: zero y      ny: negate y
//   f : 1=add, 0=and
//   no: negate output
// Common ops (zx nx zy ny f no): 0=101010, x=001100, y=110000, x+y=000010,
//   x&y=000000, x-y=010011, y-x=000111.
// Useful on its own (a calculator/datapath challenge) or as the core of hack_cpu.

module alu (
    input  logic [15:0] x,
    input  logic [15:0] y,
    input  logic        zx, nx, zy, ny, f, no,
    output logic [15:0] out,
    output logic        zr,    // out == 0
    output logic        ng     // out < 0 (MSB set)
);

    logic [15:0] xp, yp, res;

    always_comb begin
        xp  = zx ? 16'h0000 : x;
        xp  = nx ? ~xp      : xp;
        yp  = zy ? 16'h0000 : y;
        yp  = ny ? ~yp      : yp;
        res = f  ? (xp + yp) : (xp & yp);
        res = no ? ~res      : res;
    end

    assign out = res;
    assign zr  = (res == 16'h0000);
    assign ng  = res[15];

endmodule
