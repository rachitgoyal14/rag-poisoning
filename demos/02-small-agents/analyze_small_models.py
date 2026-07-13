"""
analyze_small_models.py -- Title 2 analysis: reads results/trial_log.csv
(written by run_trials_small_models.py) and produces a summary table +
grouped bar chart, one row per model instead of per precision level.

This is a genuinely new file, not a reused one -- title1_precision_matters/
analyze_results.py is hardcoded around config.MODEL_TAGS' precision labels,
so it can't be pointed at Title 2's model-labeled log without changes.

Usage:
    python analyze_small_models.py
"""
from __future__ import annotations

import csv

import matplotlib.pyplot as plt

import config_small_models as config


def _to_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


def load_trials() -> list[dict]:
    with open(config.TRIAL_LOG_PATH, newline="") as f:
        return list(csv.DictReader(f))


def summarize(trials: list[dict]) -> dict[str, dict[str, float]]:
    summary: dict[str, dict[str, float]] = {}
    for model_label in config.SMALL_MODEL_TAGS:
        rows = [t for t in trials if t["model_label"] == model_label]
        n = len(rows)
        if n == 0:
            continue
        rates = {
            metric: sum(_to_bool(r[metric]) for r in rows) / n
            for metric in config.METRICS
        }
        rates["n"] = n
        summary[model_label] = rates
    return summary


def write_summary_table(summary: dict[str, dict[str, float]]) -> None:
    with open(config.SUMMARY_TABLE_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Model", "N", *config.METRICS])
        for model_label, rates in summary.items():
            writer.writerow(
                [
                    model_label,
                    int(rates["n"]),
                    *(f"{rates[m]:.2f}" for m in config.METRICS),
                ]
            )
    print(f"Summary table written to {config.SUMMARY_TABLE_PATH}")


def print_summary_table(summary: dict[str, dict[str, float]]) -> None:
    header = f"{'Model':<16} {'N':<4} " + " ".join(
        f"{m:<20}" for m in config.METRICS
    )
    print(header)
    print("-" * len(header))
    for model_label, rates in summary.items():
        row = f"{model_label:<16} {int(rates['n']):<4} "
        row += " ".join(f"{rates[m]:.2f}".ljust(20) for m in config.METRICS)
        print(row)


def plot_bar_chart(summary: dict[str, dict[str, float]]) -> None:
    models = list(summary.keys())
    x = range(len(models))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, metric in enumerate(config.METRICS):
        values = [summary[m][metric] for m in models]
        offsets = [xi + i * width for xi in x]
        ax.bar(offsets, values, width, label=metric.replace("_", " ").title())

    ax.set_xticks([xi + width for xi in x])
    ax.set_xticklabels(models, rotation=15)
    ax.set_ylabel("Rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("Memory Poisoning Success Rates by Model (q4_0 fixed)")
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
