# Keeping one repository across the three stages

Use one repository and one folder per activity. The folder names retain the lab sequence for navigation, while the repository title describes the engineering work.

## Evidence convention

For each new experiment, record its date, tool version, RTL revision, parameter values, constraints, library corner, command sequence, and result filenames. Keep supplied/captured outputs separate from newly prepared scripts. A screenshot is useful visual evidence, but a text export makes numerical review easier.

Save results under experiment names, not ambiguous labels such as `final2`. For example:

```text
labs/lab02-dft-insertion/
  scripts/
  constraints/
  results/two-chains/after-scan-synthesis/
  results/two-chains/after-scan-connect/
  results/four-chains/
  evidence/
  netlists/
  report/

labs/lab03-physical-design/
  scripts/
  constraints/
  results/pre-placement/
  results/post-placement/
  results/pre-cts/
  results/post-cts/
  results/post-route/
  evidence/
  report/
```

Create these subfolders when they contain actual artifacts; the current planned folders intentionally contain only a README.

## Commit checkpoints

Good checkpoints include constraint corrections, a completed synthesis comparison, scan synthesis, scan stitching, a four-chain experiment, floorplan and power plan, placement analysis, CTS analysis, and routed verification. Each commit should describe a result that a reader can review.

Before a commit, check `git status` and `git diff --stat`, update the README, and confirm that references resolve to the saved evidence. Local EDA databases, credentials, and technology libraries are excluded by `.gitignore`. Selected report `.log` files may be archived as `.txt` or explicitly added with `git add -f`; do not force-add the complete runtime tree.

Keep analysis reproducible: report units, explain the slack calculation, distinguish estimated area from physical core/die area, and identify any unconstrained/excluded paths. Update a stage from “planned” to “completed” only when its results are captured and explained.
