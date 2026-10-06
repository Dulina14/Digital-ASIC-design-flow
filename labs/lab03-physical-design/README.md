# Stage 3 — Physical implementation

**Status: planned. No placed/routed design or GDSII result has been collected in this repository.**

This stage will use Cadence Innovus to implement the scan-inserted UART netlist. The planned inputs are the mapped scan netlist, timing constraints, scanDEF, timing/physical/parasitic libraries, analysis views, and stream mapping information supplied through the course environment.

## Planned sequence

1. Import the design and establish the intended analysis views and constraints.
2. Create the floorplan and document dimensions, utilization, and aspect ratio.
3. Add power rings and stripes, assign I/O positions and clock pin attributes, and save a pre-placement checkpoint.
4. Place standard cells with pre-place optimization; record gate count/area and placement screenshots.
5. Perform pre-CTS setup analysis and power special routing.
6. Run clock tree synthesis and capture the clock network/cell-count changes.
7. Reorder scan chains with awareness of the implemented clock tree.
8. Analyze post-CTS timing, including hold, and document any corrective optimization.
9. Route signals, use the intended on-chip-variation analysis mode, and collect post-route timing.
10. Add filler cells, verify geometry/connectivity, and export GDSII if the required checks are met.
11. Repeat placement without pre-place optimization from the saved checkpoint and compare outcomes.

## Evidence to collect

| Checkpoint | Save and explain |
| --- | --- |
| Floorplan/power plan | Core geometry, utilization, power rings/stripes, pin placement |
| Placement | Screenshots with nets hidden and clock nets visible; gate count/area |
| Placement comparison | Matched optimized/unoptimized measurements from the same saved checkpoint |
| Pre-CTS | Setup report and ideal-clock assumptions |
| Post-CTS | Clock network screenshots, inserted cells, skew/latency, hold report |
| Post-route | Timing analysis settings, relevant extraction assumptions, setup/hold results |
| Final verification | Geometry/connectivity reports and unresolved violations, if any |
| Export | GDSII generation result and its input/checkpoint provenance |

The discussion should explain why pre-CTS hold analysis has limited predictive value with an ideal clock network, why clock-tree implementation changes that analysis, why OCV is introduced, and how filler cells differ from metal fill. Do not treat a GDSII export alone as proof of complete production signoff.

Add actual scripts, checkpoint summaries, reports, screenshots, and exports as this stage is completed. See [the ongoing workflow](../../docs/workflow.md).
