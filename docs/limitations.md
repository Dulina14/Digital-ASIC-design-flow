# Limits of the current implementation evidence

## The 32-bit parameter experiment is not a functional validation

Both `tx_fsm.v` and `rx_fsm.v` declare `reg [2:0] data_bit_counter`. A three-bit counter cannot represent bit index 31. Changing `TX_WORD_LENGTH` and `RX_WORD_LENGTH` to 32 produces a synthesizable implementation, but does not establish correct transmission and reception of 32-bit words. Parameter-consistent counter widths and functional simulation would be required for that claim.

Reduced FSM area in the 32-bit result must therefore be interpreted cautiously: optimization can reflect unreachable behavior, not a superior functional implementation. The repository preserves the supplied RTL and does not claim that the counter issue has been fixed.

## Baud timing changes when the physical clock changes

The final experiment retains `CLOCK_IN_MHZ = 100` and the same baud-related counter constants while changing the constrained physical system clock to 50 MHz. In hardware clocked at 50 MHz, each counter interval takes approximately twice as long. This constraint-only experiment does not retain the original baud rate.

## Positive late-path slack is a limited timing conclusion

All ten reported late paths have positive slack in each supplied timing report. This supports the reported setup/late-path checks under those constraints. It does not establish hold closure, safe clock-domain crossing, all-corner signoff, or a clean electrical implementation. Reciprocal A↔B false paths explicitly remove cross-clock checks.

## Electrical violations remain

The baseline and 32-bit reports show maximum-transition violations. The final output-load experiment makes these much larger: the listed `rx_full` driver transition is about 7077 ps against a 280 ps limit. Lowering the clock frequency gives a larger timing budget but does not itself improve a loaded output's transition.

Only portions of the 32-bit and final design-rule reports were captured. Missing footer content cannot be used to infer complete maximum-capacitance or maximum-fanout results. The reported transition violation totals are costs, not failing-pin counts.

## Library setup does not demonstrate a complete MMMC analysis

The captured setup attempted to load both slow and fast libraries together and logged inconsistent nominal operating conditions and duplicate-cell deletion. Reports identify `PVT_0P9V_125C`. Listing two libraries does not prove separate multi-mode multi-corner analysis views or independent minimum/maximum delay verification.

## Captured outputs are incomplete and come from different timestamps

The mapped netlist text and power report are earlier 8-bit exports. They are preserved as earlier artifacts, not labeled as exact matches to the later corrected baseline reports. No final 32-bit mapped netlist or exported SDC was supplied as text. Clock, area, and design-rule evidence for the later experiments includes screenshots rather than complete text exports.

The preparation automation and Tcl constraint templates were newly reconstructed from captured commands and results. They have not been executed in Cadence during repository preparation. A fresh run may differ with tool settings, version, library access, or optimization history.

## Physical implementation and DFT remain future stages

No scan-chain implementation, ATPG coverage measurement, post-route extraction, physical verification, or GDSII export is claimed in the current results.
