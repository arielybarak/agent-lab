# ModelSim: vsim -c -do bin2bcd_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../bin2bcd.sv bin2bcd_tb.sv
vsim -c work.bin2bcd_tb
run -all
quit -f
