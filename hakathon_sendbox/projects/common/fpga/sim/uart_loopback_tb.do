# ModelSim: run with  vsim -c -do uart_loopback_tb.do   (from this sim/ folder)
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../uart_tx.sv ../uart_rx.sv uart_loopback_tb.sv
vsim -c work.uart_loopback_tb
run -all
quit -f
