"""
run_trials.py -- runs N trials per precision level defined in config.py and
logs raw per-trial outcomes to results/trial_log.csv.

This is the file that actually spends Ollama inference time -- make sure
memory_store.py and attack_scenario.py both pass their standalone smoke
tests first (see the "how to run/test" note for each).

Usage:
    python run_trials.py
"""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from common.attack_scenario import load_scenario, run_single_trial


def run_all_trials() -> None:
    scenario = load_scenario(config.TRIGGER_TERMS_PATH)
    fieldnames = [
        "precision_label",
        "model_tag",
        "trial_index",
        config.METRIC_INJECTION_SUCCESS,
        config.METRIC_RETRIEVAL_RATE,
        config.METRIC_TRIGGER_SUCCESS,
        "planted_record_id",
        "agent_response",
        "control_response",
    ]

    with open(config.TRIAL_LOG_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for precision_label, model_tag in config.MODEL_TAGS.items():
            print(f"\n=== {precision_label} ({model_tag}) ===")
            for i in range(config.N_TRIALS_PER_PRECISION):
                start = time.time()
                result = run_single_trial(model_tag, scenario)
                elapsed = time.time() - start

                writer.writerow(
                    {
                        "precision_label": precision_label,
                        "model_tag": model_tag,
                        "trial_index": i,
                        config.METRIC_INJECTION_SUCCESS: result.injection_success,
                        config.METRIC_RETRIEVAL_RATE: result.retrieval_rate,
                        config.METRIC_TRIGGER_SUCCESS: result.trigger_success,
                        "planted_record_id": result.planted_record_id,
                        "agent_response": result.agent_response.replace("\n", " "),
                        "control_response": result.control_response.replace("\n", " "),
                    }
                )
                f.flush()

                print(
                    f"  trial {i + 1}/{config.N_TRIALS_PER_PRECISION} "
                    f"({elapsed:.1f}s) -- "
                    f"inj={result.injection_success} "
                    f"ret={result.retrieval_rate} "
                    f"trig={result.trigger_success}"
                )

    print(f"\nDone. Raw trial log written to {config.TRIAL_LOG_PATH}")


if __name__ == "__main__":
    run_all_trials()
