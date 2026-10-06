# Reconstructed constraint templates

These files are newly prepared source templates based on the captured `source constraints.tcl` transcript and later clock/load reports. They are not claimed to be the original files exported from the university machine. In particular, the supplied `constraints.txt` contains timing-lint results rather than Tcl source.

`baseline8.tcl` and `width32.tcl` create 10 ns, 50% duty clocks. `clock50_load52.tcl` creates 20 ns clocks with 40% duty cycle and a 10 ns offset for B. Each sources `common.tcl`, which sets the external budgets and corrected port collections.

`common.tcl` intentionally retains 6 ns I/O delays, 0.5 ns uncertainty, clock/reset don't-touch networks, maximum input fanout 20, output fanout load 2, and reciprocal A/B false paths. It corrects the B collection to include `rx_full_b`. Reset delay and input transition/driver models remain unspecified, matching the study's lint findings. Adding models without external interface requirements would invent assumptions.

The observed environment uses ns for time and pF for `set_load`; reports display ps and fF. Check the loaded library/tool units when using another environment. The final load is the original 0.2 pF plus 5 pF, hence 5.2 pF.

The new files have not been executed in Genus during repository preparation. Use them as a reviewable starting point, inspect the emitted SDC and clock/port reports, and verify each collection in the target installation. False paths preserve the lab experiment; they are not proof of safe clock-domain crossing.
