# ModelSim: vsim -c -do compositor_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../compositor.sv compositor_tb.sv
vsim -c work.compositor_tb
run -all
quit -f
