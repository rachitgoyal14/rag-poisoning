"""
analyze_results.py -- reads results/trial_log.csv and produces:
  - results/summary_table.csv         (rates per precision level)
  - results/precision_comparison.png  (grouped bar chart)

Usage:
    python analyze_results.py
"""

from __future__ import annotations

import csv

import matplotlib.pyplot as plt

import config


def _to_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


def load_trials() -> list[dict]:
    with open(config.TRIAL_LOG_PATH, newline="") as f:
        return list(csv.DictReader(f))


def summarize(trials: list[dict]) -> dict[str, dict[str, float]]:
    summary: dict[str, dict[str, float]] = {}
    for precision_label in config.MODEL_TAGS:
        rows = [t for t in trials if t["precision_label"] == precision_label]
        n = len(rows)
        if n == 0:
            continue
        rates = {
            metric: sum(_to_bool(r[metric]) for r in rows) / n
            for metric in config.METRICS
        }
        rates["n"] = n
        summary[precision_label] = rates
    return summary


def write_summary_table(summary: dict[str, dict[str, float]]) -> None:
    with open(config.SUMMARY_TABLE_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Precision", "N", *config.METRICS])
        for precision_label, rates in summary.items():
            writer.writerow(
                [
                    precision_label,
                    int(rates["n"]),
                    *(f"{rates[m]:.2f}" for m in config.METRICS),
                ]
            )
    print(f"Summary table written to {config.SUMMARY_TABLE_PATH}")


def print_summary_table(summary: dict[str, dict[str, float]]) -> None:
    header = f"{'Precision':<10} {'N':<4} " + " ".join(
        f"{m:<20}" for m in config.METRICS
    )
    print(header)
    print("-" * len(header))
    for precision_label, rates in summary.items():
        row = f"{precision_label:<10} {int(rates['n']):<4} "
        row += " ".join(f"{rates[m]:.2f}".ljust(20) for m in config.METRICS)
        print(row)


def plot_bar_chart(summary: dict[str, dict[str, float]]) -> None:
    precisions = list(summary.keys())
    x = range(len(precisions))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, metric in enumerate(config.METRICS):
        values = [summary[p][metric] for p in precisions]
        offsets = [xi + i * width for xi in x]
        ax.bar(offsets, values, width, label=metric.replace("_", " ").title())

    ax.set_xticks([xi + width for xi in x])
    ax.set_xticklabels(precisions)
    ax.set_ylabel("Rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("Memory Poisoning Success Rates by Precision")
    ax.legend()
    fig.tight_layout()
    fig.savefig(config.BAR_CHART_PATH, dpi=150)
    print(f"Bar chart written to {config.BAR_CHART_PATH}")


if __name__ == "__main__":
    trials = load_trials()
    summary = summarize(trials)
    print_summary_table(summary)
    write_summary_table(summary)
    plot_bar_chart(summary)
