# ModelSim: vsim -c -do bcd_counter_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../bcd_counter.sv bcd_counter_tb.sv
vsim -c work.bcd_counter_tb
run -all
quit -f
