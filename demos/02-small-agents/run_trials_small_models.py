"""
run_trials_small_models.py -- Title 2 demo driver.

Reuses, unchanged, from ../common/:
  - memory_store.py         (MemoryStore)
  - attack_scenario.py      (load_scenario, run_single_trial, and the whole
                              MINJA-style bridging/indication-prompt/
                              progressive-shortening logic)
  - data/trigger_terms.json (identical scenario -- same attack, same
                              trigger term, same fictional .example vendor)

New here: instead of sweeping *precision* at a fixed model (Title 1), this
sweeps *model* at a fixed precision (q4_0), across four small models that
sit below the DTA benchmark's 9B floor.

Each call to run_single_trial() creates its own fresh MemoryStore
internally (reset=True), so trials never leak into each other regardless
of which folder's config.py it happens to resolve paths from.

Usage:
    python run_trials_small_models.py
"""
from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import config_small_models as config
from common.attack_scenario import load_scenario, run_single_trial


def run_all_trials() -> None:
    scenario = load_scenario(config.TRIGGER_TERMS_PATH)
    fieldnames = [
        "model_label",
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

        for model_label, model_tag in config.SMALL_MODEL_TAGS.items():
            print(f"\n=== {model_label} ({model_tag}) ===")
            for i in range(config.N_TRIALS_PER_MODEL):
                start = time.time()
                result = run_single_trial(model_tag, scenario)
                elapsed = time.time() - start

                writer.writerow(
                    {
                        "model_label": model_label,
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
                    f"  trial {i + 1}/{config.N_TRIALS_PER_MODEL} "
                    f"({elapsed:.1f}s) -- "
                    f"inj={result.injection_success} "
                    f"ret={result.retrieval_rate} "
                    f"trig={result.trigger_success}"
                )

    print(f"\nDone. Raw trial log written to {config.TRIAL_LOG_PATH}")


if __name__ == "__main__":
    run_all_trials()
