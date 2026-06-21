# ModelSim: vsim -c -do hex_display_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../hex_display.sv hex_display_tb.sv
vsim -c work.hex_display_tb
run -all
quit -f
