"""
Central configuration for the Title 1 demo:
"Does Precision Matter, Again? Quantization-Dependent Susceptibility to
Persistent Memory Poisoning in Local LLM Agents"

Edit MODEL_TAGS to match whatever quantization tags you've actually pulled
with `ollama pull`.
"""

from pathlib import Path
import sys

# Import shared common config from demos/common.
sys.path.insert(0, str(Path(__file__).parent.parent))
import common.config as common_config  # noqa: E402

# ---------------------------------------------------------------------------
# Model / precision configuration
# ---------------------------------------------------------------------------
# Map a human-readable precision label -> the exact Ollama model tag.
# Pull these first, e.g.:
#   ollama pull llama3.2:3b-instruct-q4_0
#   ollama pull llama3.2:3b-instruct-q8_0
#   ollama pull llama3.2:3b-instruct-fp16
MODEL_TAGS = {
    "Q4_0": "llama3.2:3b-instruct-q4_0",
    # "Q8_0": "llama3.2:3b-instruct-q8_0",
    # "FP16": "llama3.2:3b-instruct-fp16",
}

OLLAMA_HOST = "http://localhost:11434"

# ---------------------------------------------------------------------------
# Embedding / vector store configuration
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = common_config.EMBEDDING_MODEL
CHROMA_PERSIST_DIR = "./results/chroma_db"
CHROMA_COLLECTION_NAME = common_config.CHROMA_COLLECTION_NAME

# ---------------------------------------------------------------------------
# Trial configuration
# ---------------------------------------------------------------------------
N_TRIALS_PER_PRECISION = 10
RANDOM_SEED = 42

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
TRIGGER_TERMS_PATH = common_config.TRIGGER_TERMS_PATH
RESULTS_DIR = Path(__file__).parent / "results"
TRIAL_LOG_PATH = RESULTS_DIR / "trial_log.csv"
SUMMARY_TABLE_PATH = RESULTS_DIR / "summary_table.csv"
BAR_CHART_PATH = RESULTS_DIR / "precision_comparison.png"

# ---------------------------------------------------------------------------
# Metric names (kept consistent across run_trials.py and analyze_results.py)
# ---------------------------------------------------------------------------
METRIC_INJECTION_SUCCESS = common_config.METRIC_INJECTION_SUCCESS
METRIC_RETRIEVAL_RATE = common_config.METRIC_RETRIEVAL_RATE
METRIC_TRIGGER_SUCCESS = common_config.METRIC_TRIGGER_SUCCESS
METRICS = common_config.METRICS

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
