# Reconstructed clock50_load52 scenario; inspect constraints/README.md.
create_clock -name clk_a -period 20 [get_ports clk_a] -waveform {0 8}
create_clock -name clk_b -period 20 [get_ports clk_b] -waveform {10 18}
set external_output_load_pf 5.2
source [file join [file dirname [info script]] common.tcl]
