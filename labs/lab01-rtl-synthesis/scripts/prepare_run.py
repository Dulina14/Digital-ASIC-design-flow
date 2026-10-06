#!/usr/bin/env python3
"""Prepare an isolated Genus workspace; does not run Cadence tools.

Reconstructed from captured commands. See the stage README for provenance,
assumed units, library setup differences, and functional limitations.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import sys

EXPERIMENTS = {
    "baseline8": {"word_length": 8, "physical_clock_mhz": 100, "load_pf": 0.2},
    "width32": {"word_length": 32, "physical_clock_mhz": 100, "load_pf": 0.2},
    "clock50_load52": {"word_length": 32, "physical_clock_mhz": 50, "load_pf": 5.2},
}
REQUIRED_LIBRARIES = (
    "timing/slow_vdd1v0_basicCells.lib",
    "lef/gsclib045_tech.lef",
    "lef/gsclib045_macro.lef",
    "lef/gsclib045_multibitsDFF.lef",
    "qrc/qx/gpdk045.tch",
)


def tcl_path(path):
    """Brace-quote literal paths; reject characters needing special Tcl handling."""
    value = path.resolve().as_posix()
    if any(char in value for char in "{}\n\r"):
        raise ValueError("Paths must not contain braces or line breaks.")
    return "{" + value + "}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", required=True, choices=EXPERIMENTS)
    parser.add_argument("--library-root", required=True, type=Path,
                        help="Authorized gsclib045 directory with timing, lef, qrc/qx.")
    parser.add_argument("--run-root", required=True, type=Path,
                        help="New directory to create; existing directories are refused.")
    args = parser.parse_args()
    stage = Path(__file__).resolve().parents[1]
    library_root = args.library_root.resolve()
    run_root = args.run_root.resolve()
    if run_root.exists():
        parser.error(f"Run directory already exists: {run_root}. Choose a fresh path.")
    missing = [name for name in REQUIRED_LIBRARIES if not (library_root / name).is_file()]
    if missing:
        parser.error("Missing required library files: " + ", ".join(missing))
    try:
        tcl_path(library_root)
    except ValueError as error:
        parser.error(str(error))

    config = EXPERIMENTS[args.experiment]
    # Prepare text before creating directories, so source errors leave no partial run.
    top = (stage / "rtl/uart_top.v").read_text(encoding="utf-8")
    for parameter in ("TX_WORD_LENGTH", "RX_WORD_LENGTH"):
        top, count = re.subn(
            rf"(parameter\s+{parameter}\s*=\s*)8\b",
            lambda match: match.group(1) + str(config["word_length"]), top,
        )
        if count != 1:
            parser.error(f"Expected exactly one captured {parameter} = 8 declaration.")

    setup = f"""# Reconstructed setup: slow corner only, not an MMMC configuration.
set_db init_lib_search_path [list {tcl_path(library_root / 'lef')} {tcl_path(library_root / 'timing')} {tcl_path(library_root / 'qrc/qx')}]
set_db library {{slow_vdd1v0_basicCells.lib}}
set_db lef_library {{gsclib045_tech.lef gsclib045_macro.lef gsclib045_multibitsDFF.lef}}
set_db qrc_tech_file gpdk045.tch
"""
    flow = """# Run from this run directory's work/ folder, in a fresh Genus session.
# Newly reconstructed flow; not locally executed in Genus.
source ../setup.tcl
read_hdl [glob ../input/rtl/*.v]
elaborate uart_top
check_design > ../log/check_design.log
uniquify uart_top
source ../input/constraints.tcl
synthesize -to_mapped -effort m
write -mapped > ../output/uart_top.v
write_sdc > ../output/uart_top.sdc
report_area > ../report/area.log
report_timing -nworst 10 > ../report/timing.log
report_port * > ../report/ports.log
report_power > ../report/power.log
# Also capture clocks, constraint lint, and design rules using this installation's
# report commands or GUI. Inspect units and PVT before comparing archived results.
"""
    run_root.mkdir(parents=True)
    for folder in ("work", "input", "log", "output", "report"):
        (run_root / folder).mkdir()
    shutil.copytree(stage / "rtl", run_root / "input/rtl")
    (run_root / "input/rtl/uart_top.v").write_text(top, encoding="utf-8", newline="\n")
    shutil.copy2(stage / f"constraints/{args.experiment}.tcl", run_root / "input/constraints.tcl")
    shutil.copy2(stage / "constraints/common.tcl", run_root / "input/common.tcl")
    (run_root / "setup.tcl").write_text(setup, encoding="utf-8", newline="\n")
    (run_root / "flow.tcl").write_text(flow, encoding="utf-8", newline="\n")
    metadata = {
        "experiment": args.experiment,
        "top_module": "uart_top",
        "tx_word_length": config["word_length"],
        "rx_word_length": config["word_length"],
        "tx_no_of_words": 1,
        "rx_no_of_words": 1,
        "rtl_clock_in_mhz": 100,
        "physical_clock_mhz": config["physical_clock_mhz"],
        "external_output_load_pf": config["load_pf"],
        "library_root": str(library_root),
        "timing_library": "slow_vdd1v0_basicCells.lib",
        "status": "Prepared only; Genus not executed by this script",
    }
    (run_root / "experiment.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {args.experiment}: {run_root}")
    print(f"Change directory to {run_root / 'work'}, launch genus, then source ../flow.tcl.")
    print("Inspect the RTL limitations, reported units, PVT, and constraints before drawing conclusions.")


if __name__ == "__main__":
    main()
