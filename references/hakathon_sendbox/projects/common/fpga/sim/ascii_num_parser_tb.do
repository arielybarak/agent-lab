# ModelSim: vsim -c -do ascii_num_parser_tb.do
if {[file exists work]} { vdel -all }
vlib work
vlog -sv ../ascii_num_parser.sv ascii_num_parser_tb.sv
vsim -c work.ascii_num_parser_tb
run -all
quit -f
