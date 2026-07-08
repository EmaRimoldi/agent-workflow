# Demo Walkthrough

This repository is easiest to read as an evidence trail, not as a UI demo.
The concrete task is AutoResearch: agents edit one CIFAR-10 training script,
run evaluations, and try to reduce validation loss.

## The Task

`autoresearch/` is the benchmark substrate used by the runtime:

- `autoresearch/train.py` is the file agents are allowed to edit.
- `autoresearch/prepare.py` owns data loading and evaluation.
- `val_bpb` is the reported validation-loss proxy; lower is better.
- Agent modes differ only in how search is coordinated: single long run,
  parallel independent runs, private/shared memory, swarm blackboard, or merge.

This gives the repo a concrete experimental question:

> Which agent workflow finds better `train.py` edits per unit of wall time,
> cost, and coordination overhead?

## Fastest Reading Path

1. Read the selected benchmark baseline:
   [`studies/baseline/README.md`](../studies/baseline/README.md).

   The current baseline was chosen after 161 controlled non-agentic evaluations.
   The selected starting model is "width 30, lower learning rate" (internal ID
   `width30_lr_low`), with `val_bpb = 0.841354` and future agent target
   `target_val_bpb = 0.824`.

2. Read the strongest agent-workflow finding:
   [`studies/agent_memory_ablation/README.md`](../studies/agent_memory_ablation/README.md).

   The most informative comparison is `T06` vs `T07`:

   | Trial | Meaning | Attempts | Best `val_bpb` | Mean `val_bpb` |
   |---|---|---:|---:|---:|
   | `T06` | exploratory search, no memory | 21 | 0.933 | 1.816 |
   | `T07` | exploratory search with shared memory | 41 | 0.914 | 1.049 |

   The interpretation is that exploration without routing correction behaves
   like a random walk, while shared memory reduces catastrophic repeats.

3. Read why the task had to be calibrated:
   [`studies/evaluator_calibration/results/evaluator_calibration_summary.md`](../studies/evaluator_calibration/results/evaluator_calibration_summary.md).

   This study made evaluation deterministic. Five consecutive baseline runs
   produced identical `val_bpb = 0.811222`, which means differences can be
   attributed to agent edits rather than training noise.

4. Read why compute allocation had to be controlled:
   [`studies/compute_allocation_calibration/README.md`](../studies/compute_allocation_calibration/README.md).

   This study shows why fixed-time parallel training can look worse simply
   because each worker completes fewer optimizer updates, and why fixed-step
   evaluation separates quality from latency.

## What To Look At Visually

The most useful result figures are:

- [`studies/figures/figure-01-study-map.png`](../studies/figures/figure-01-study-map.png)
- [`studies/baseline/results/figures/figure-04-recommended-baseline-detail.png`](../studies/baseline/results/figures/figure-04-recommended-baseline-detail.png)
- [`studies/agent_memory_ablation/results/figures/figure-01-trial-outcomes.png`](../studies/agent_memory_ablation/results/figures/figure-01-trial-outcomes.png)
- [`studies/agent_memory_ablation/results/figures/figure-02-memory-stabilization.png`](../studies/agent_memory_ablation/results/figures/figure-02-memory-stabilization.png)
- [`studies/evaluator_calibration/results/calibration__2x2-diversity-memory__superseded/figures/figure-01-main-comparison.png`](../studies/evaluator_calibration/results/calibration__2x2-diversity-memory__superseded/figures/figure-01-main-comparison.png)
- [`studies/compute_allocation_calibration/results/figures/figure-01-fixed-time-compute-loss.png`](../studies/compute_allocation_calibration/results/figures/figure-01-fixed-time-compute-loss.png)
- [`studies/compute_allocation_calibration/results/figures/figure-02-fixed-step-latency-cost.png`](../studies/compute_allocation_calibration/results/figures/figure-02-fixed-step-latency-cost.png)
- [`studies/swarm_baselines/results/figures/figure-01-validation-bpb-over-time.png`](../studies/swarm_baselines/results/figures/figure-01-validation-bpb-over-time.png)
- [`studies/swarm_baselines/results/figures/figure-04-swarm-memory-architecture.png`](../studies/swarm_baselines/results/figures/figure-04-swarm-memory-architecture.png)

## Runnable Surface

The current public CLI is:

```bash
uv run agentops --help
uv run agentops parallel --help
uv run agentops parallel-shared --help
uv run agentops single-long --help
uv run agentops single-memory --help
uv run agentops swarm --help
uv run agentops merge --help
uv run agentops certified-time --help
uv run agentops baseline-calibration --help
```

The repository does not include raw private run logs or local datasets. Curated
summaries and figures are checked in under `studies/`; new full runs write to
`runs/`.
