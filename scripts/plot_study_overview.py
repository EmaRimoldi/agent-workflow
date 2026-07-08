"""Generate a simple visual map of the repository studies."""

from __future__ import annotations

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "studies" / "figures"

DARK = "#111827"
GRAY = "#64748b"
BLUE = "#2563eb"
GREEN = "#16a34a"
ORANGE = "#f97316"
PURPLE = "#7c3aed"
RED = "#dc2626"
SLATE = "#334155"
FILL = "#f8fafc"

STUDIES = [
    {
        "name": "Baseline",
        "folder": "baseline/",
        "role": "Choose the common starting train.py",
        "result": "161 controlled evaluations; selected val_bpb 0.841",
        "color": BLUE,
    },
    {
        "name": "Evaluator calibration",
        "folder": "evaluator_calibration/",
        "role": "Remove training noise",
        "result": "5 repeated baseline runs matched exactly",
        "color": GREEN,
    },
    {
        "name": "Compute allocation",
        "folder": "compute_allocation_calibration/",
        "role": "Separate quality from resource contention",
        "result": "Fixed-time parallel runs completed fewer updates",
        "color": ORANGE,
    },
    {
        "name": "Agent memory ablation",
        "folder": "agent_memory_ablation/",
        "role": "Test memory and exploration",
        "result": "T07 controlled exploratory failures better than T06",
        "color": PURPLE,
    },
    {
        "name": "Swarm baselines",
        "folder": "swarm_baselines/",
        "role": "Preserve blackboard coordination evidence",
        "result": "Historical swarm runs beat independent parallel baseline",
        "color": RED,
    },
    {
        "name": "Theory validation",
        "folder": "theory_validation/",
        "role": "Audit theorem, estimators, and protocol",
        "result": "Narrowed the claim and identified assumptions",
        "color": SLATE,
    },
]


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def add_box(ax: plt.Axes, x: float, y: float, item: dict) -> None:
    box = FancyBboxPatch(
        (x, y),
        2.62,
        1.34,
        boxstyle="round,pad=0.035,rounding_size=0.05",
        facecolor=FILL,
        edgecolor=item["color"],
        linewidth=1.5,
    )
    ax.add_patch(box)
    ax.text(x + 1.31, y + 1.16, item["name"], ha="center", va="top", fontsize=12, fontweight="bold", color=DARK)
    ax.text(x + 1.31, y + 0.86, item["folder"], ha="center", va="top", fontsize=9.5, color=item["color"])
    ax.text(x + 1.31, y + 0.61, wrap(item["role"], 31), ha="center", va="top", fontsize=9.5, color="#374151")
    ax.text(x + 1.31, y + 0.26, wrap(item["result"], 34), ha="center", va="top", fontsize=8.7, color=GRAY)


def arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=15,
            linewidth=1.4,
            color="#94a3b8",
            shrinkA=3,
            shrinkB=3,
        )
    )


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(13.8, 6.4), constrained_layout=True)
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.set_title("Study map: what each experiment contributes", fontsize=17, pad=14, color=DARK)

    positions = [(0.35, 3.1), (3.65, 3.1), (6.95, 3.1), (0.35, 0.95), (3.65, 0.95), (6.95, 0.95)]
    for item, (x, y) in zip(STUDIES, positions):
        add_box(ax, x, y, item)

    arrow(ax, (2.97, 3.77), (3.65, 3.77))
    arrow(ax, (6.27, 3.77), (6.95, 3.77))
    arrow(ax, (8.26, 3.1), (8.26, 2.29))
    arrow(ax, (6.95, 1.62), (6.27, 1.62))
    arrow(ax, (3.65, 1.62), (2.97, 1.62))

    ax.text(
        5.0,
        0.22,
        "Read left-to-right for methodology, then agent evidence, then historical swarm context and theory audit.",
        ha="center",
        fontsize=10.5,
        color=GRAY,
    )

    fig.savefig(FIGURES / "figure-01-study-map.png", dpi=260)
    fig.savefig(FIGURES / "figure-01-study-map.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
