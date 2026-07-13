"""
Config for Title 2: "Small Agents, Same Sleepers? Parameter-Scale Effects
on Delayed-Trigger Memory Poisoning Below the 8B Threshold."

This config reuses shared common settings for the embedder, Chroma
collection name, and trigger-term path.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import common.config as common_config  # noqa: E402

# ---------------------------------------------------------------------------
# Small-model roster -- none of these are tested anywhere in the DTA
# benchmark, whose smallest model is 9B. Pull each at its default tag
# before running (that default is q4_0 on the Ollama library for all four).
# If a tag below doesn't resolve on your machine, check `ollama list` /
# the library page for the exact current tag name (e.g. Phi-3-mini is
# sometimes tagged `phi3:mini` instead of `phi3:3.8b`).
# ---------------------------------------------------------------------------
SMALL_MODEL_TAGS = {
    "Llama-3.2-1B": "llama3.2:1b",
    "Qwen3-1.7B": "qwen3:1.7b",
    "Gemma3-1B": "gemma3:1b",
    "Phi-3-3.8B": "phi3:3.8b",
}

N_TRIALS_PER_MODEL = 5  # smaller N than Title 1 -- direction-validation only

# ---------------------------------------------------------------------------
# Reused settings (same embedder, same Chroma collection shape, same
# scenario file -- imported from shared common config so nothing drifts
# out of sync between the demos)
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = common_config.EMBEDDING_MODEL
CHROMA_COLLECTION_NAME = common_config.CHROMA_COLLECTION_NAME
TRIGGER_TERMS_PATH = common_config.TRIGGER_TERMS_PATH
METRIC_INJECTION_SUCCESS = common_config.METRIC_INJECTION_SUCCESS
METRIC_RETRIEVAL_RATE = common_config.METRIC_RETRIEVAL_RATE
METRIC_TRIGGER_SUCCESS = common_config.METRIC_TRIGGER_SUCCESS
METRICS = common_config.METRICS

# ---------------------------------------------------------------------------
# New paths -- kept separate from Title 1's results/ so the two demos'
# trial data never mix
# ---------------------------------------------------------------------------
RESULTS_DIR = Path(__file__).parent / "results"
TRIAL_LOG_PATH = RESULTS_DIR / "trial_log.csv"
SUMMARY_TABLE_PATH = RESULTS_DIR / "summary_table.csv"
BAR_CHART_PATH = RESULTS_DIR / "model_comparison.png"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
