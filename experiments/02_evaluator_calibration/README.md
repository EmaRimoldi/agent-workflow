# Evaluator Calibration

**Status**: superseded design experiment
**Question**: can the evaluator be made deterministic enough that later agent
workflow comparisons measure agent edits rather than training noise?

## What Was Run

This experiment used fixed-step evaluation, repeated baseline checks, and early
memory/no-memory calibration reps. Its most important result is that five
unmodified baseline runs produced identical `val_bpb = 0.811222`.

## What It Contributed

The experiment established that deterministic evaluation was possible, but it also
found design problems: memory anchoring, run-count thresholds, task ceiling
effects, and training-time confounds. Those findings motivated the later
[`04_agent_memory_ablation/`](../04_agent_memory_ablation/) experiment.

## Read First

- [`results/evaluator_calibration_summary.md`](results/evaluator_calibration_summary.md)

## Caveat

This is not the current primary agentic result. It is methodological evidence
that explains why the later ablation was redesigned.
