# Reconstructed baseline8 scenario; inspect constraints/README.md.
create_clock -name clk_a -period 10 [get_ports clk_a] -waveform {0 5}
create_clock -name clk_b -period 10 [get_ports clk_b] -waveform {0 5}
set external_output_load_pf 0.2
source [file join [file dirname [info script]] common.tcl]
