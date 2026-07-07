# ModelSim: vsim -c -do button_debounce_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../button_debounce.sv button_debounce_tb.sv
vsim -c work.button_debounce_tb
run -all
quit -f
