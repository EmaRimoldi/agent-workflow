"""Official CLI for AgentOps Lab."""

from __future__ import annotations

import argparse


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        prog="agentops",
        description="Run AgentOps Lab experiments and analysis workflows.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["parallel", "single-long", "swarm", "merge"],
        help="Mode to run: parallel, single-long, swarm, or merge",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)

    args = parser.parse_args(argv)
    rest = args.args
    if args.command == "parallel":
        from agentops_lab.modes.parallel import main_parallel
        main_parallel(rest)
    elif args.command == "single-long":
        from agentops_lab.modes.single_long import main_single_long
        main_single_long(rest)
    elif args.command == "swarm":
        from agentops_lab.modes.swarm import main_swarm
        main_swarm(rest)
    elif args.command == "merge":
        from scripts.run_merge_phase import main as merge_main
        merge_main(rest)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
