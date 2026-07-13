"""
memory_store.py -- thin wrapper around a local ChromaDB collection used as
the agent's long-term memory store.

This module is shared by multiple demos and does not depend on title-specific
config. Title-specific code passes the desired persist directory, collection
name, and embedding model when it creates the store.
"""

from __future__ import annotations

import uuid
from typing import Any, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class MemoryStore:
    """A minimal wrapper around a persistent Chroma collection, used as the
    stand-in for an agentic RAG system's long-term memory.
    """

    def __init__(
        self,
        persist_dir: str = "./results/chroma_db",
        collection_name: str = "agent_memory",
        embedding_model: str = "all-MiniLM-L6-v2",
        reset: bool = False,
    ):
        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        if reset:
            try:
                self._client.delete_collection(collection_name)
            except Exception:
                pass
        self._collection = self._client.get_or_create_collection(collection_name)
        self._embedder = SentenceTransformer(embedding_model)

    def write(self, text: str, metadata: Optional[dict[str, Any]] = None) -> str:
        """Write a single memory record. Returns the record's id."""
        record_id = str(uuid.uuid4())
        embedding = self._embedder.encode([text])[0].tolist()
        self._collection.add(
            ids=[record_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}],
        )
        return record_id

    def query(self, text: str, n_results: int = 3) -> dict[str, Any]:
        """Query memory for the n most similar records to `text`."""
        embedding = self._embedder.encode([text])[0].tolist()
        return self._collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )

    def contains_record(self, record_id: str) -> bool:
        """Verify a specific record id is actually present in the store --
        used to score Injection Success independent of retrieval.
        """
        result = self._collection.get(ids=[record_id])
        return len(result.get("ids", [])) > 0

    def get_record_text(self, record_id: str) -> Optional[str]:
        result = self._collection.get(ids=[record_id])
        docs = result.get("documents", [])
        return docs[0] if docs else None

    def count(self) -> int:
        return self._collection.count()

    def reset(self) -> None:
        """Wipe all records -- call between trials so trials don't leak
        into each other.
        """
        all_ids = self._collection.get().get("ids", [])
        if all_ids:
            self._collection.delete(ids=all_ids)


if __name__ == "__main__":
    print("Sanity-checking MemoryStore...")
    store = MemoryStore(persist_dir="./results/chroma_db_smoketest", reset=True)

    rid = store.write(
        "Test record: user prefers window seats on flights.",
        metadata={"source": "smoketest"},
    )
    print(f"Wrote record {rid}. Store count = {store.count()}")

    assert store.contains_record(rid), "FAIL: record not found after write"
    print("contains_record: OK")

    results = store.query("What kind of seat does the user like?", n_results=1)
    print("query() results:", results["documents"])

    store.reset()
    assert store.count() == 0, "FAIL: reset() did not clear the store"
    print("reset: OK")

    print("All smoke tests passed.")
