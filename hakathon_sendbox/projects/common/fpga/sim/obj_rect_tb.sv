// Self-checking test for obj_rect: inside/outside bounds + signed (off-screen).
`timescale 1ns/1ps

module obj_rect_tb;

    logic signed [11:0] px, py, tx, ty;
    logic               drawing;
    logic        [11:0] ox, oy;

    obj_rect #(.WIDTH(16), .HEIGHT(16)) dut (
        .pixel_x(px), .pixel_y(py), .topleft_x(tx), .topleft_y(ty),
        .drawing(drawing), .offset_x(ox), .offset_y(oy));

    int errors = 0;
    task automatic chk(input string name, input logic exp);
        #1;
        if (drawing !== exp) begin $error("%s: drawing=%b exp %b", name, drawing, exp); errors++; end
    endtask

    initial begin
        tx = 100; ty = 50;
        px = 100; py = 50;  chk("top-left corner", 1);
        if (ox !== 0 || oy !== 0) begin $error("corner offset %0d,%0d", ox, oy); errors++; end
        px = 115; py = 65;  chk("bottom-right inside", 1);
        if (ox !== 15 || oy !== 15) begin $error("br offset %0d,%0d", ox, oy); errors++; end
        px = 116; py = 50;  chk("just past right", 0);
        px =  99; py = 50;  chk("just left", 0);

        // signed: sprite partly off the left edge
        tx = -5; ty = 0;
        px =  0; py = 0;    chk("off-screen sprite, on-screen pixel", 1);
        if (ox !== 5) begin $error("signed offset %0d exp 5", ox); errors++; end
        px = 11; py = 0;    chk("past right of off-screen sprite", 0); // dx=16

        if (errors == 0) $display("OBJ_RECT: PASS");
        else             $display("OBJ_RECT: FAIL (%0d errors)", errors);
        $finish;
    end

endmodule
