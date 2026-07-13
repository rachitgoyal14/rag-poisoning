from pathlib import Path

# Embedding / vector store configuration reused across demos.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_PERSIST_DIR = "./results/chroma_db"
CHROMA_COLLECTION_NAME = "agent_memory"

# Shared scenario data path.
DATA_DIR = Path(__file__).parent / "data"
TRIGGER_TERMS_PATH = DATA_DIR / "trigger_terms.json"

# Shared metric names.
METRIC_INJECTION_SUCCESS = "injection_success"
METRIC_RETRIEVAL_RATE = "retrieval_rate"
METRIC_TRIGGER_SUCCESS = "trigger_success"
METRICS = [
    METRIC_INJECTION_SUCCESS,
    METRIC_RETRIEVAL_RATE,
    METRIC_TRIGGER_SUCCESS,
]
