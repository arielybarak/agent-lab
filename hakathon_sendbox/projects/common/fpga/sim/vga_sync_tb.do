# ModelSim: vsim -c -do vga_sync_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../vga_sync.sv vga_sync_tb.sv
vsim -c work.vga_sync_tb
run -all
quit -f
