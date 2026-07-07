# ModelSim: vsim -c -do obj_rect_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../obj_rect.sv obj_rect_tb.sv
vsim -c work.obj_rect_tb
run -all
quit -f
