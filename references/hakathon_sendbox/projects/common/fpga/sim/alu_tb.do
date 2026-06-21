# ModelSim: vsim -c -do alu_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../alu.sv alu_tb.sv
vsim -c work.alu_tb
run -all
quit -f
