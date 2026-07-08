# Agent Workflow

Agent Workflow is an open-source harness for designing and scoring Claude Code
agent workflows before you trust them with expensive work.

Define one agent or N agents, choose their models, roles, memory mode, and
CPU/GPU assignment, then run the same task through single-agent, parallel,
shared-memory, swarm, or merge workflows. The framework runs locally; live agent
capacity depends on your Claude Code subscription, provider quota, and available
compute.

![Agent Workflow experiment map](docs/assets/experiments/experiment-map.png)

## Why It Matters

AI-agent teams can now spawn more workers easily. The harder question is whether
more agents, shared memory, or coordination actually improves the result. Agent
Workflow measures that tradeoff with isolated workspaces, fixed evaluation
budgets, run logs, snapshots, and comparable metrics.

The built-in benchmark is `autoresearch/`: agents edit a CIFAR-10 `train.py`,
run evaluations, and try to reduce `val_bpb` validation loss. Lower is better.

## Build Your Own Agent Team

Use the compact CLI when every worker should be similar:

```bash
uv run agent-workflow parallel \
  --n-agents 4 \
  --model claude-haiku-4-5-20251001 \
  --cuda-devices 0,1,2,3 \
  --train-max-steps 1170 \
  --serialized-evaluator \
  --experiment-id four_agent_smoke
```

Use a roster config when agents should have different roles:

```yaml
agents:
  use_shared_memory: true
  roster:
    - id: explorer
      role: broad architecture and hyperparameter search
      model: claude-sonnet-4-6
      temperature: 1.2  # search-style directive; Claude CLI has no native temperature flag
      cuda_device: "0"
    - id: optimizer
      role: conservative refinement of the best known candidate
      model: claude-haiku-4-5-20251001
      temperature: 0.3  # lower values ask the agent to make smaller edits
      cuda_device: "1"
```

Run it with:

```bash
uv run agent-workflow parallel-shared --config configs/agent_roster_example.yaml
```

`N` is intentionally not hardcoded. You can test as many agents as your
subscription, provider rate limits, evaluator concurrency, and local CPU/GPU
resources can support.

## Current Signal

The strongest result so far is from the memory ablation experiment:

| Condition | Attempts | Best `val_bpb` | Mean `val_bpb` |
|---|---:|---:|---:|
| Exploratory search, no memory | 21 | 0.933 | 1.816 |
| Exploratory search, shared memory | 41 | 0.914 | 1.049 |

The narrow takeaway: shared memory did not solve the task, but it made
exploratory agents much less destructive on this benchmark.

## Evidence

| Evidence | What it proves | Start here |
|---|---|---|
| Baseline calibration | The starting task is neither trivial nor impossible. | [`experiments/01_baseline/`](experiments/01_baseline/) |
| Evaluation protocol | Fixed-step deterministic evaluation avoids hardware-dependent conclusions. | [`experiments/02_evaluation_protocol_calibration/`](experiments/02_evaluation_protocol_calibration/) |
| Memory ablation | Shared memory can stabilize exploratory agents in this substrate. | [`experiments/03_agent_memory_ablation/`](experiments/03_agent_memory_ablation/) |
| Swarm baseline | Historical blackboard runs are promising context for richer coordination. | [`experiments/04_swarm_baselines/`](experiments/04_swarm_baselines/) |

## Quick Demo

```bash
uv sync --dev
uv run agent-workflow doctor
PYTHONPATH=src python -m pytest tests -q
PYTHONPATH=src python -m agent_workflow.cli --help
```

For the shortest guided walkthrough, read [`docs/demo_script.md`](docs/demo_script.md).
For the full evidence path, read [`docs/demo_walkthrough.md`](docs/demo_walkthrough.md).

## CLI

```bash
uv run agent-workflow --help
uv run agent-workflow parallel --help
uv run agent-workflow parallel-shared --help
uv run agent-workflow single-long --help
uv run agent-workflow single-memory --help
uv run agent-workflow swarm --help
uv run agent-workflow merge --help
uv run agent-workflow certified-time --help
uv run agent-workflow baseline-calibration --help
uv run agent-workflow doctor
```

Live agent runs require Claude Code authentication and a clean workspace. See
[`docs/reproducibility.md`](docs/reproducibility.md).

## What Is Included

- A runnable `agent-workflow` CLI.
- Configurable agent rosters for custom roles, models, temperatures, and device
  assignment.
- Claude Code project instructions, sub-agent templates, and a preflight
  `doctor` command.
- The controlled `autoresearch/` benchmark task.
- Execution modes for single-agent, parallel, shared-memory, swarm, and merge
  workflows.
- Shared-memory/blackboard primitives, certified-time analysis, diversity
  metrics, snapshots, reasoning traces, and reporting utilities.
- Curated experiment summaries, tables, and figures.

## Limits

- This is not a general benchmark for all agent tasks.
- The current strongest evidence is one controlled memory-ablation comparison.
- Historical live-agent runs are not bit-for-bit reproducible because model
  services and agent decisions can change over time.

## More

- [`experiments/README.md`](experiments/README.md) - experiment map
- [`experiments/catalog.md`](experiments/catalog.md) - compact evidence catalog
- [`docs/reviewer_checklist.md`](docs/reviewer_checklist.md) - what is built, proven, and still open
- [`docs/reproducibility.md`](docs/reproducibility.md) - local and Claude Code setup
- [`docs/product/claude_code_orchestration.md`](docs/product/claude_code_orchestration.md) - product wedge and Claude Code orchestration setup
