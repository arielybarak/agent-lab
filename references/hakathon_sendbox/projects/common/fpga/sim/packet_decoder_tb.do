# ModelSim: vsim -c -do packet_decoder_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../packet_decoder.sv packet_decoder_tb.sv
vsim -c work.packet_decoder_tb
run -all
quit -f
