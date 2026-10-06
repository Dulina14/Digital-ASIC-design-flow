# Stage 1 — RTL synthesis and constraint experiments

**Status: experiments completed; report prepared.** Tool: Cadence Genus 18.10-p003_1. Reference design: dual cross-connected UART. Reported operating condition: `PVT_0P9V_125C`; interconnect mode: global; area mode: physical library.

## Read this stage in order

1. Inspect [`rtl/uart_top.v`](rtl/uart_top.v) and [`rtl/uart_transceiver.v`](rtl/uart_transceiver.v) to understand hierarchy and serial connections.
2. Read the [ASIC flow notes](../../docs/asic-flow-notes.md) and the [constraints guide](constraints/README.md).
3. Inspect the [8-bit evidence](evidence/baseline8/), then compare [32-bit evidence](evidence/width32/) and [clock/load evidence](evidence/clock50-load52/).
4. Review the [summary CSV](results/experiment-summary.csv), [limitations](../../docs/limitations.md), and [final PDF report](report/220511N_Lab1_RTL_Synthesis_Report.pdf).

## Captured execution sequence

The supplied console transcripts record library setup, `read_hdl`, `elaborate uart_top`, `check_design`, `uniquify uart_top`, constraint sourcing, `synthesize -to_mapped -effort m`, netlist/SDC export, reports, and GUI launch. These transcripts describe the earlier initial run and include the original B-output typo; the corrected results are saved separately.

| Step | Purpose | Captured/new material |
| --- | --- | --- |
| Technology setup | Timing, physical dimensions, interconnect estimation | [Library console](evidence/console/library-setup.txt) |
| Read and elaborate | Apply parameters and resolve hierarchy | [Synthesis console](evidence/console/initial-synthesis.txt) |
| Check and uniquify | Inspect structural issues and separate instance subdesigns | Initial synthesis console; complete check log not supplied |
| Apply constraints | Set clocks, I/O budgets, loads, and exceptions | [Reconstructed templates](constraints/) |
| Map and export | Create library-cell netlist and downstream constraints | [Earlier 8-bit export](netlists/uart_top_8bit_earlier.v), [export screenshot](evidence/design/export-and-reports.png) |
| Inspect reports | Explain area, late-path timing, lint, power, and design rules | Evidence directories and final report |

## Experiment definitions

| ID | RTL top-level defaults used | Constraints |
| --- | --- | --- |
| `baseline8` | TX/RX word length 8, one word per buffer, clock parameter 100 | 10 ns clocks, `{0 5}` waveforms, 0.2 pF load |
| `width32` | TX/RX word length 32; other top parameters retained | Same 100 MHz constraints |
| `clock50_load52` | Same 32-bit RTL as previous experiment | 20 ns clocks, A `{0 8}`, B `{10 18}`, 5.2 pF load |

All cases retain 0.5 ns setup uncertainty, 6 ns data/control input delays, 6 ns output delays, and reciprocal A/B false paths. The constraints intentionally preserve the captured missing reset delays and input driver/slew definitions for comparison.

## Evidence index

| Directory/file | Meaning and provenance |
| --- | --- |
| `rtl/*.v` | Nine source modules extracted without behavior changes from `code.txt`; defaults remain 8 bits |
| `evidence/source/code.txt` | Exact original combined RTL snapshot |
| `evidence/console/` | Initial setup/synthesis transcripts, with account workspace paths replaced |
| `evidence/baseline8/area.txt` | Corrected 8-bit area capture |
| `evidence/baseline8/clocks.txt` | 100 MHz clocks and 83 registers per clock |
| `evidence/baseline8/constraints-lint.txt` | Supplied `constraints.txt`; this is report output, not Tcl |
| `evidence/baseline8/timing.txt` | Ten late paths; worst slack 2539 ps |
| `evidence/baseline8/design-rules.txt` | Transition violations; complete supplied baseline text |
| `evidence/baseline8/ports.txt` | Supplied port report |
| `evidence/baseline8/power-earlier.txt` | Earlier 8-bit estimate, not a matched latest power comparison |
| `evidence/width32/` | Area, clocks, lint, and design-rule screenshots; text timing capture |
| `evidence/clock50-load52/` | Step 9 area/clock/lint/design-rule screenshots and text timing capture |
| `evidence/design/` | Schematics and export/report console screenshot |
| `netlists/uart_top_8bit_earlier.v` | Earlier mapped 8-bit export from `uart_top.txt`; not the final 32-bit netlist |
| `results/experiment-summary.csv` | Transcribed/calculated experiment comparison, with evidence references |
| `results/timing-paths.json` | Ten captured slack values per experiment, parsed from supplied reports |
| `evidence/manifest.json` | Source filename, treatment, and SHA-256 for copied evidence |
| `report/` | Final PDF and editable Word report |

Report headers use the remote machine's time labels. The timeline is preserved as captured rather than converted to local Sri Lankan time. Not all artifacts originate from the same run timestamp.

## Recreate a run on the Cadence machine

Required technology directory structure:

```text
/path/to/gsclib045/
  timing/slow_vdd1v0_basicCells.lib
  lef/gsclib045_tech.lef
  lef/gsclib045_macro.lef
  lef/gsclib045_multibitsDFF.lef
  qrc/qx/gpdk045.tch
```

The reconstructed flow uses **only the slow timing library** to avoid the duplicate-cell deletion seen when both corners were loaded together. This is a deliberate preparation choice; it does not recreate the original warning-producing library command byte for byte, and does not set up MMMC signoff.

From the repository root:

```sh
python3 labs/lab01-rtl-synthesis/scripts/prepare_run.py \
  --experiment width32 \
  --library-root /path/to/gsclib045 \
  --run-root work/width32
cd work/width32/work
genus
source ../flow.tcl
```

`source ../flow.tcl` belongs at the **Genus prompt**, not the Unix prompt. Use a fresh Genus session per experiment. The script refuses to replace an existing run directory. It prints the prepared path and leaves a record of the experiment parameters.

The generated flow writes a mapped netlist, SDC, design check, and area/timing/port/power reports. Capture clock, constraint-lint, and design-rule reports through the available Genus reporting commands/GUI in your installation, then archive the relevant outputs. Inspect the generated setup and reported units/PVT before comparing numerical results.

### What to rerun after changes

- **Top-level parameter edit:** reread RTL and elaborate again, then check, uniquify, constrain, synthesize, and report.
- **Constraint-only edit:** apply the revised constraints and resynthesize/report. A fresh session that repeats the full flow avoids duplicate or stale constraints and is the prepared script's approach.
- **Report-only request:** report the existing mapped design if the intended constraints and implementation are already loaded.

### Validation performed during repository preparation

The RTL split was checked against the original nine module bodies; timing summaries were parsed from the supplied text; summary values were reconciled with the completed report; repository links and file inventory were checked. The preparation script was exercised in a temporary workspace using placeholder library filenames to validate file generation. No synthesis, simulation, or proprietary timing analysis was run locally.

## Main conclusions

The 32-bit case is larger and has less late-path margin than the baseline. The slower-clock case gains late-path margin but has much worse output transitions under the larger load. Neither the positive slacks nor the parameter-only change establish a fully verified design. Counter-width, baud-timing, exception, library, and evidence boundaries are detailed in [limitations](../../docs/limitations.md).
