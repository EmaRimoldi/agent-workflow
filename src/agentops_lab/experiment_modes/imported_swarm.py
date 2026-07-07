"""Imported agents-swarms mode: N agents with a shared JSONL blackboard."""

from __future__ import annotations

from pathlib import Path

from agentops_lab.config import ExperimentConfig
from agentops_lab.imported_swarms import IMPORTED_SWARM_MODE
from agentops_lab.imported_swarms.swarm_config import SwarmConfig
from agentops_lab.imported_swarms.swarm_orchestrator import (
    ImportedSwarmOrchestrator,
)
from agentops_lab.outputs.collector import collect_experiment
from agentops_lab.outputs.reporter import write_experiment_report


def run_imported_swarm_experiment(
    config: ExperimentConfig,
    experiment_dir: Path,
    repo_root: Path,
    system_prompt: str,
    first_message_template: str,
    swarm_config: SwarmConfig | None = None,
):
    """Run the imported swarm logic without replacing native 2x2 modes."""
    config.mode = IMPORTED_SWARM_MODE
    if swarm_config is None:
        swarm_config = SwarmConfig()
    assert len(config.agents) >= 1, (
        f"Imported swarm mode expects at least 1 agent, got {len(config.agents)}"
    )

    orchestrator = ImportedSwarmOrchestrator(
        config=config,
        repo_root=repo_root,
        swarm_config=swarm_config,
    )
    orchestrator.run_swarm(
        experiment_dir=experiment_dir,
        system_prompt=system_prompt,
        first_message_template=first_message_template,
    )

    agent_ids = [a.agent_id for a in config.agents]
    summary = collect_experiment(
        experiment_dir=experiment_dir,
        experiment_id=config.experiment_id,
        mode=IMPORTED_SWARM_MODE,
        agent_ids=agent_ids,
    )

    mode_dir = experiment_dir / f"mode_{IMPORTED_SWARM_MODE}"
    write_experiment_report(summary, mode_dir)
    return summary

