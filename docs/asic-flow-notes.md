# ASIC synthesis: explanations and worked examples

## Inputs to synthesis

Verilog RTL specifies behavior and structure. Timing libraries (`.lib`) characterize cell delay, transition, setup/hold requirements, and power. LEF provides physical cell/layer information. The parasitic technology (`.tch` in this setup) supports interconnect estimation. Timing constraints define the environment in which the design must operate.

A clock constraint does not generate an oscillator or rewrite the sampling logic. An input delay models when an external device supplies data relative to the clock. An output delay reserves time for external receiving logic. A pin load models external capacitance, influencing output delay and slew.

## Read, elaborate, check, and uniquify

`read_hdl` reads the source. `elaborate uart_top` resolves hierarchy, applies parameters, and connects signals. The top-level word lengths take effect here, which is why changing them requires fresh elaboration. `check_design` reports structural problems such as unresolved references or undriven signals; it is not a replacement for functional simulation. `uniquify uart_top` gives instances separate subdesign representations for independent optimization.

## Optimize and map

The captured flow used `synthesize -to_mapped -effort m`. Genus translates RTL into generic logic, optimizes it, and maps it to library cells. The log reports this as an older command and names `syn_generic`, `syn_map`, and `syn_opt` as alternatives. The repository's reconstructed flow keeps the command used in the captured experiment rather than silently substituting a different flow.

The mapped Verilog expresses the implementation using standard-cell instances. Exported SDC transfers constraints to downstream tools. Area, timing, port, and power reports are different views of this implementation and its environment.

## Clocks and resets

The system clocks are `clk_a` and `clk_b`; each drives one transceiver. Sequential logic uses rising edges. The RTL checks `if (reset)` inside `always @(posedge clk)`, making these resets synchronous and active high. A reset port without input delay remains a constraint-lint finding even when the reset network is marked don't-touch.

The `sampling_tick_generator` produces pulses consumed as enable conditions in clocked blocks. A slower enable pulse is not a derived clock when it does not drive the sequential clock pins.

## Frequency, duty cycle, and phase

Frequency is the reciprocal of period. A 10 ns period is 100 MHz; a 20 ns period is 50 MHz. Duty cycle is high time divided by period. Edges `{0 8}` at 20 ns mean an 8 ns high interval, hence 40% duty cycle.

For clock B, edges `{10 18}` move both edges 10 ns later. Phase offset is `360 × 10 / 20 = 180°`. Simply inverting a 40% clock would produce 60% high time, so inversion is not the waveform used here.

The setup uncertainty is 0.5 ns. Reported clock network/source latencies are zero in these synthesis reports. CTS and implemented clock delays will be a later stage.

## The output collection correction

The captured initial constraint command for B selected `rx_full_a`. This left the intended B flag out of its correct output-delay collection and applied a B-clock output delay to an A-side signal. The corrected collection selects `rx_full_b`.

Edit the constraints source, then reload the corrected constraints and regenerate synthesis/reports. A fresh Genus session is the cleanest way to avoid stale constraints. Editing only constraints does not require an RTL change. Editing top-level parameters requires rereading and elaborating the design before synthesis.

## External I/O budgets

The recorded design uses 6 ns input delays and 6 ns output delays, with A-side signals assigned to clock A and B-side signals to clock B. The external output load begins at 0.2 pF. Adding 5 pF produces 5.2 pF, or 5200 fF, before the estimated internal net capacitance is added.

No external driving-cell or input-transition model was specified for several data/control inputs. The lint reports reflect this: the baseline shows 22 inputs without driver/transition definitions, and the wider case shows 70. The reset-delay entries overlap with the reset inputs in that count, so the total lint entry count is not a count of unique ports.

## Baseline input-to-register timing

The worst captured baseline path begins at `rx_data_rd_enable_in_b` and ends at an RX-buffer full-counter register. All quantities below are in ns:

```text
Required time = capture edge − uncertainty − setup requirement
              = 10.000 − 0.500 − 0.168 = 9.332
Arrival time  = external input delay + internal data path
              = 6.000 + 0.793 = 6.793
Slack         = required − arrival = 2.539
```

## 32-bit input-to-register timing

```text
Required time = 10.000 − 0.500 − 0.091 = 9.409
Arrival time  = 6.000 + 1.378 = 7.378
Slack         = 9.409 − 7.378 = 2.031
```

The internal data path grows by 0.585 ns while the setup requirement falls by 0.077 ns. Their combined effect is 0.508 ns less slack. The reported path includes a larger fanout and additional logic; the changed parameter affects more than the input/output bus declaration.

## Final register-to-output timing

The worst final path launches in B at 10 ns and is checked against the next B edge at 30 ns:

```text
Required time = capture edge − output delay − uncertainty
              = 30.000 − 6.000 − 0.500 = 23.500
Arrival time  = launch edge + internal data path
              = 10.000 + 4.636 = 14.636
Slack         = 23.500 − 14.636 = 8.864
```

The equivalent A path launches at 0 ns and captures at 20 ns; its slack is also 8.864 ns. The phase offset changes absolute edge timestamps without changing the same-clock full-cycle budget.

The output `CLKBUFX20` arc contributes 4.070 ns of delay and has 7.077 ns transition at approximately 5201.6 fF load. The external 5200 fF plus the estimated net contribution explains that load value. Although the late path is met, its transition violates the 280 ps limit by approximately 6797 ps.

## Area comparison

Cell count is the number of mapped instances; it is not a transistor count. Cell area is the sum of the library cell footprints. Net area is an interconnect-related estimate. Neither reported total area nor cell area directly specifies final die dimensions.

```text
8 → 32-bit cell count increase = (1130 − 772) / 772 × 100 = 46.37%
8 → 32-bit cell area increase  = (4010.292 − 2220.948) / 2220.948 × 100 = 80.57%
8 → 32-bit total area increase = (5413.762 − 3167.441) / 3167.441 × 100 = 70.92%
Final cell area reduction vs 32-bit/100 MHz = 5.07%
Final total area reduction vs 32-bit/100 MHz = 3.78%
```

The output-load and clock changes allow a different mapped implementation even without another RTL edit. The modest area reduction does not mean the increased load improves electrical behavior.

## Power and its assumptions

The earlier 8-bit report gives leakage 60.819 nW, dynamic power 172490.052 nW, and total 172550.870 nW, approximately 172.551 µW. It predates the corrected baseline report set. There is no matched 32-bit/final power evidence, and switching-activity provenance was not supplied, so a comparative power claim would be unsupported.

## Timing exceptions and signoff boundaries

The reciprocal `set_false_path` commands remove paths between the A and B clocks from timing checks. They are analysis exceptions, not circuitry or proof of safe CDC. Likewise, loading slow and fast libraries into one setup is not the same as creating separate MMMC views. Library warnings and the actual reported PVT must be reviewed before drawing a signoff conclusion.

The next stages add scan circuitry and real placement/interconnect. Those stages can change area, clock loading, delay, and congestion; they need their own before/after measurements.
