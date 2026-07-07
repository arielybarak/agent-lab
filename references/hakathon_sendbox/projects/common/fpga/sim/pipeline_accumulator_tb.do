# ModelSim: vsim -c -do pipeline_accumulator_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../pipeline_accumulator.sv pipeline_accumulator_tb.sv
vsim -c work.pipeline_accumulator_tb
run -all
quit -f
