# AgentOps Lab Architecture

AgentOps Lab treats `agentops_lab` as the public package surface while the
current tested runtime remains under `agentops_lab`. The public
architecture is split between stable interfaces, compatibility runtime,
evaluation tooling, and experiment evidence.

## Canonical Runtime Shape

```text
agentic CLI
  -> modes.parallel       -> agentops_lab.launcher.main_parallel
  -> modes.single_long    -> agentops_lab.launcher.main_single_long
  -> modes.merge          -> agentops_lab.merger.MergeOrchestrator
  -> modes.swarm          -> integrated blackboard surface and swarm runtime

agentops_lab.config
  -> AgentConfig, ExperimentConfig from agentops_lab.config

agentops_lab.orchestrator
  -> Orchestrator from agentops_lab.orchestrator

agentops_lab.communication
  -> SharedMemory blackboard
  -> coordinator helpers

agentops_lab.analysis
  -> H_prior / H_post diversity metrics

agentops_lab.instrumentation
  -> snapshotting
  -> reasoning traces
  -> certified time
```

## Configuration

There is one canonical config surface:

```python
from agentops_lab.config import AgentConfig, ExperimentConfig
```

During this public-release phase it re-exports the runtime dataclasses from
`agentops_lab.config`. This keeps existing behavior stable while
runtime ownership moves behind the canonical package surface.

## Orchestration

There is one canonical orchestrator surface:

```python
from agentops_lab.orchestrator import Orchestrator
```

It currently delegates to `agentops_lab.orchestrator.Orchestrator`.
The existing orchestrator owns process spawning, git worktree isolation, worker
integration, output collection, and report generation.

## Modes

| Mode | Module | Current integration status |
|---|---|---|
| `parallel` | `agentops_lab.modes.parallel` | Thin wrapper around the runtime launcher |
| `single_long` | `agentops_lab.modes.single_long` | Thin wrapper around the runtime launcher |
| `merge` | `agentops_lab.modes.merge` | Wrapper around `MergeOrchestrator`; CLI also preserves script behavior |
| `swarm` | `agentops_lab.modes.swarm` | Canonical blackboard creation plus `--run` delegation to the swarm runtime |

## Integrated Components

### Blackboard Communication

`src/agentops_lab/communication/blackboard.py` provides:

- append-only JSONL shared memory
- file locking via `fcntl`
- claim/dedup/release flow
- best-result sidecar
- context filtering for "other agents" reads

### Swarm Coordinator

`src/agentops_lab/communication/coordinator.py` imports the canonical
blackboard module and exposes local coordination helpers for shared-memory
agent workflows.

### Diversity Metrics

`src/agentops_lab/analysis/diversity.py` consolidates H_prior/H_post-style
analysis. Lightweight trajectory DTW is dependency-free; embedding and
weight-space metrics import heavy ML dependencies lazily.

### Instrumentation

`src/agentops_lab/instrumentation/` consolidates:

- snapshotting
- reasoning traces
- certified-time analysis

## Output And Reporting

The canonical reporting pipeline is still the runtime output stack under
`src/agentops_lab/outputs/` plus merge/report scripts and the swarm
reporter path. A future cleanup should move that ownership under
`agentops_lab.outputs` and leave compatibility imports behind.
