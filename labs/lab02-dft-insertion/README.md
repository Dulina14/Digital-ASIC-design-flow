# Stage 2 — DFT and scan insertion

**Status: planned. No DFT execution results have been collected in this repository.**

This stage will use Cadence Genus to insert muxed scan into the dual UART design. The coursework handout describes scan synthesis, scan-chain definition and stitching, DFT checks, and exports for downstream physical implementation and ATPG tooling.

## Planned sequence

1. Establish and record the functional baseline, parameters, constraints, library setup, and inherited RTL limitations.
2. Read and elaborate the RTL, uniquify instances, and apply constraints.
3. Set muxed scan style and DFT naming prefix; define an active-high shared scan enable.
4. Check DFT rules before scan synthesis.
5. Run generic synthesis and technology mapping; export the scan-synthesized netlist and area, timing, port, and power reports.
6. Define dedicated scan chains for the two clock regions, preview them, and stitch the scan cells.
7. Perform incremental optimization and recheck DFT rules.
8. Export the stitched netlist, SDC, scanDEF, scan setup/chain reports, and ATPG input files.
9. Repeat with two scan chains per transceiver and dedicated scan I/O; compare overhead and chain structure.

## Evidence to collect

| Checkpoint | Save and explain |
| --- | --- |
| Before scan synthesis | Functional baseline area and port count |
| After scan synthesis | Netlist, area, timing, power, ports, DFT rule result |
| After stitching | Netlist, SDC, scanDEF, chain report, DFT rules, updated area/ports |
| Four-chain experiment | Chain lengths, dedicated scan I/O, shared enable, area/port comparison |
| Scan-cell comparison | Matching netlist excerpts showing SI connections before and after stitching |
| Pad-limited discussion | A reasoned proposal for reducing dedicated scan pins with added test logic |

Do not equate scannable-cell replacement with a connected scan chain. Do not report achieved fault coverage from ATPG input export alone; running ATPG is outside the described exercise and would need separate evidence.

When results are available, add `scripts/`, `constraints/`, `results/`, `evidence/`, `netlists/`, and `report/` folders with actual artifacts. Update this README and the root progress table. See [the ongoing workflow](../../docs/workflow.md).
