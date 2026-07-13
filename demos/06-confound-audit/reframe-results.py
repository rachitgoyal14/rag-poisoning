# demos/title6_confound_audit/reframe_results.py
"""
reframe_results.py -- Title 6 demo: "Compression and Compromise:
Quantization as an Uncontrolled Confound in Agentic Memory-Poisoning
Benchmarks."

Per plan.md, Title 6 is explicitly NOT a new pipeline: "Demo: identical to
Title 1 -- same pipeline, same table, just narrate it as a 'confound audit'
instead of a 'vulnerability study'." This script does not run any new
trials, call Ollama, or touch Chroma. It only re-reads Title 1's already-
generated results and re-emits the identical numbers under confound-audit
framing (renamed columns + the DTA scope-limitations quote as the lead-in),
so the underlying evidence is provably the same as Title 1's -- only the
narrative changes.

ASSUMPTION FLAG: I don't have your actual demos/01-precision-matters/
analyze_results.py output filename, so this scans that results/ dir for
*.csv the same flexible way title3_taxonomy/tag_failure_modes.py scans
trial logs, and looks for a row per precision level with recognizable
column names (see FIELD_ALIASES). If your actual summary CSV uses
different column names, only FIELD_ALIASES needs editing.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Optional

TITLE6_DIR = Path(__file__).parent
RESULTS_DIR = TITLE6_DIR / "results"
TITLE1_RESULTS_DIR = TITLE6_DIR.parent / "01-precision-matters" / "results"

OUTPUT_TABLE = RESULTS_DIR / "confound_audit_table.csv"
OUTPUT_SUMMARY = RESULTS_DIR / "confound_audit_summary.md"

FIELD_ALIASES: dict[str, list[str]] = {
    "precision": ["precision", "quantization", "condition", "level"],
    "injection_success": [
        "injection_success", "injection_success_rate", "inject_success"
    ],
    "retrieval_rate": ["retrieval_rate", "retrieved", "retrieval_success_rate"],
    "trigger_success": [
        "trigger_success", "trigger_success_rate", "asr", "attack_success_rate"
    ],
}

# The line plan.md says to quote precisely, not paraphrase -- this is the
# actual scope-limitations text pulled from the DTA paper reference in
# plan.md, kept verbatim here since Title 6's whole framing hinges on
# quoting it exactly, not summarizing it.
DTA_SCOPE_LIMITATION_QUOTE = (
    'results "may differ from full-precision or API-served versions"'
)


def _find_title1_summary_csv() -> Optional[Path]:
    if not TITLE1_RESULTS_DIR.exists():
        return None
    candidates = sorted(TITLE1_RESULTS_DIR.rglob("*.csv"))
    return candidates[0] if candidates else None


def _normalize_row(raw: dict) -> dict:
    canonical = {}
    for canon, aliases in FIELD_ALIASES.items():
        for key in aliases:
            if key in raw and raw[key] not in (None, ""):
                canonical[canon] = raw[key]
                break
        canonical.setdefault(canon, "")
    return canonical


def load_title1_rows() -> list[dict]:
    path = _find_title1_summary_csv()
    if path is None:
        print(f"  [warn] no CSV found under {TITLE1_RESULTS_DIR}")
        return []
    print(f"  reading Title 1 results from {path}")
    with open(path, newline="") as f:
        raw_rows = list(csv.DictReader(f))
    return [_normalize_row(r) for r in raw_rows]


def write_confound_table(rows: list[dict]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_TABLE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Quantization level (uncontrolled confound in DTA)",
                "Injection Success",
                "Retrieval Rate",
                "Trigger Success (ASR)",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["precision"],
                    row["injection_success"],
                    row["retrieval_rate"],
                    row["trigger_success"],
                ]
            )
    print(f"  wrote {OUTPUT_TABLE}")


def write_confound_summary(rows: list[dict]) -> None:
    with open(OUTPUT_SUMMARY, "w") as f:
        f.write("# Title 6 -- Confound Audit Summary\n\n")
        f.write(
            "**Framing:** identical evidence to Title 1. Every number below "
            "is pulled directly from Title 1's own results/ directory -- "
            "nothing was re-run. Only the narrative changes: this is not "
            '"we found a vulnerability," it is "a benchmark\'s own footnote, '
            'turned into a research question."\n\n'
        )
        f.write(
            f"**Lead with this, quoted precisely (per plan.md, not "
            f"paraphrased):** DTA's own scope-limitations section states "
            f"its {DTA_SCOPE_LIMITATION_QUOTE} -- i.e. the paper's own "
            f"authors flag quantization as an open question rather than "
            f"answer it. Every existing local-model benchmark built on "
            f"Ollama defaults, DTA included, has silently fixed "
            f"quantization at whatever the default pull tag happens to be, "
            f"meaning published attack-success numbers may not generalize "
            f"across deployment configurations.\n\n"
        )
        if rows:
            f.write("| Quantization | Injection Success | Retrieval Rate | Trigger Success (ASR) |\n")
            f.write("|---|---|---|---|\n")
            for row in rows:
                f.write(
                    f"| {row['precision']} | {row['injection_success']} | "
                    f"{row['retrieval_rate']} | {row['trigger_success']} |\n"
                )
        else:
            f.write(
                "*(No Title 1 results found yet -- run Title 1's pipeline "
                "first, then re-run this script.)*\n"
            )
        f.write(
            "\n---\n\nSame reading list as Title 1: DTA (arXiv:2605.08442), "
            "Egashira et al. (arXiv:2405.18137), \"Widening the Gap\" "
            "(arXiv:2605.15152), AQUA-LLM (arXiv:2509.13514). Per plan.md, "
            "only the lead-in and framing order changes for this title.\n"
        )
    print(f"  wrote {OUTPUT_SUMMARY}")


def main() -> None:
    print("Reading Title 1's existing results (no new trials will be run)...")
    rows = load_title1_rows()
    write_confound_table(rows)
    write_confound_summary(rows)
    if not rows:
        print(
            "\nNo rows found -- if Title 1 has already been run, check "
            "FIELD_ALIASES against your actual summary CSV's column names."
        )


if __name__ == "__main__":
    main()