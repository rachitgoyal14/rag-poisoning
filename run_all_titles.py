"""Run all demo titles end-to-end from the repository root.

This script executes the current Title 1-4 demo pipelines in order:
  1. Title 1 trials
  2. Title 1 analysis
  3. Title 2 trials
  4. Title 2 analysis
  5. Title 3 failure-mode tagging
  6. Title 4 defense evaluation

Run from the repo root with:
    python run_all_titles.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

COMMANDS = [
    (
        "Title 1 trials",
        ROOT / "demos" / "01-precision-matters" / "run_trials.py",
        ROOT / "demos" / "01-precision-matters",
    ),
    (
        "Title 1 analysis",
        ROOT / "demos" / "01-precision-matters" / "analyze_results.py",
        ROOT / "demos" / "01-precision-matters",
    ),
    (
        "Title 2 trials",
        ROOT / "demos" / "02-small-agents" / "run_trials_small_models.py",
        ROOT / "demos" / "02-small-agents",
    ),
    (
        "Title 2 analysis",
        ROOT / "demos" / "02-small-agents" / "analyze_small_models.py",
        ROOT / "demos" / "02-small-agents",
    ),
    (
        "Title 3 taxonomy",
        ROOT / "demos" / "03-taxonomy" / "tag_failure_modes.py",
        ROOT / "demos" / "03-taxonomy",
    ),
    (
        "Title 4 defense",
        ROOT / "demos" / "04-defense-quant" / "judge_defense.py",
        ROOT / "demos" / "04-defense-quant",
    ),
]


def run_command(name: str, script_path: Path, cwd: Path) -> None:
    if not script_path.exists():
        raise FileNotFoundError(f"Missing script for {name}: {script_path}")

    print(f"\n=== Running {name} ===")
    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(cwd),
        check=True,
    )


def main() -> None:
    for name, script_path, cwd in COMMANDS:
        run_command(name, script_path, cwd)
    print("\nAll title pipelines completed successfully.")


if __name__ == "__main__":
    main()
