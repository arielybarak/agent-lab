# ModelSim: vsim -c -do seven_segment_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../seven_segment.sv seven_segment_tb.sv
vsim -c work.seven_segment_tb
run -all
quit -f
