# Kickoff Prompt for Implementing the Demos

**How to use this:** Start a new Claude chat, attach `plan.md` as context, then paste the prompt below as your first message. It forces the new chat to propose a plan and provide all necessary files for the requested title at once, reusing the shared codebase.

---

## Folder structure (current repository state)

```
project-root/
├── docs/                                   # planning and kickoff prompts
│   ├── plan.md                             # main research direction & demo plan document
│   └── kickoff-prompt.md                   # this file
│
├── demos/
│   ├── requirements.txt                    # shared python package dependencies
│   │
│   ├── common/                             # SHARED PIPELINE (implemented)
│   │   ├── __init__.py
│   │   ├── config.py                       # shared embedding model & Chroma settings
│   │   ├── memory_store.py                 # local ChromaDB + sentence-transformers wrapper
│   │   ├── attack_scenario.py              # MINJA-style query-only injection scenario, scoring & single-trial runner
│   │   └── data/
│   │       └── trigger_terms.json          # conversation and trigger term configuration
│   │
│   ├── 01-precision-matters/               # Title 1: Quantization-dependent sweep (implemented)
│   │   ├── README.md
│   │   ├── config.py                       # overrides or specifies base model precision levels (Q4_0, Q8_0, FP16)
│   │   ├── run_trials.py                   # precision trial loop running N trials per condition
│   │   ├── analyze_results.py              # analyzes log, outputs summary CSV and precision comparison plot
│   │   └── results/                        # trial logs, summary tables, and plots
│   │
│   ├── 02-small-agents/                    # Title 2: Small model parameter sweep (implemented)
│   │   ├── README.md
│   │   ├── config_small_models.py          # small-model roster (1B-4B range)
│   │   ├── run_trials_small_models.py      # trial runner iterating over the small model roster
│   │   ├── analyze_small_models.py         # analysis scripts generating model comparison results
│   │   └── results/                        # trial logs, summary tables, and plots
│   │
│   ├── title3_taxonomy/                    # Title 3 (NOT YET BUILT): Failure-mode taxonomy
│   │   └── tag_failure_modes.py            # script to analyze and tag trial logs into failure categories
│   │
│   └── title4_defense_quant/               # Title 4 (NOT YET BUILT): Defense effectiveness under quantization
│       └── judge_defense.py                # LLM-judge defense code/sandbox evaluation
```

---

## The prompt (copy everything in the box below into the new chat)

```
You are helping me implement the demos described in the attached document (plan.md). This is academic AI-security research: I'm a research intern building a local, sandboxed red-teaming harness that poisons the memory of my own local LLM agent — running entirely on my own machine, no third-party systems involved — to reproduce and extend methodology from published papers cited in the doc (MINJA, MemoryGraft, the DTA benchmark, etc.), ahead of a research meeting with my faculty advisor.

ENVIRONMENT
- MacBook Pro, Apple M5, 24GB unified memory, macOS
- Python 3.11
- Ollama for local model serving (models pulled as quantization tags, e.g. llama3.2:3b-instruct-q4_0, q8_0, fp16, etc.)
- ChromaDB as the local vector store
- sentence-transformers for embeddings

WHAT HAS ALREADY BEEN DONE
We have implemented a shared foundation and the first two title sweeps in the repository:
1. `demos/common/` (Shared Code):
   - `config.py`: Shared constants for embedding model ("all-MiniLM-L6-v2"), Chroma collection name, results path, and metrics.
   - `memory_store.py`: Simple ChromaDB persistent client wrapper with write/query/reset/contains operations.
   - `attack_scenario.py`: Implements a MINJA-style query-only injection scenario, simulating a bridging conversation + indication prompt + progressive shortening to write the agent's own memory summary to Chroma, followed by a benign trigger query to measure injection success, retrieval rate, and trigger success.
   - `data/trigger_terms.json`: JSON file with the conversation turns, trigger query, and target payload.
2. `demos/01-precision-matters/` (Title 1: Precision Sweep):
   - Compares the `llama3.2:3b-instruct` model across Q4_0, Q8_0, and FP16.
   - `config.py` (defines model tag mapping), `run_trials.py` (trial runner), and `analyze_results.py` (saves summary CSV and bar charts).
3. `demos/02-small-agents/` (Title 2: Small Model Sweep):
   - Compares 1B-4B parameter models (llama3.2:1b, qwen3:1.7b, gemma3:1b, phi3:3.8b) at q4_0 quantization.
   - `config_small_models.py` (specifies model tags), `run_trials_small_models.py` (runs trials), and `analyze_small_models.py` (saves comparison results).

HOW THIS CONVERSATION SHOULD WORK
When I ask you to build a specific Title's demo (e.g., Title 3 or Title 4 from the plan.md document), you must output all necessary files for that title at once in your very first reply:
1. First, outline a brief file-by-file plan showing what files you are creating, what they do, and how they reuse or import the existing shared code from `demos/common/` or existing trial results (e.g., Title 3 should reuse and tag the trial logs generated by Title 1 and Title 2).
2. Immediately follow the plan with the complete, runnable code for ALL of those files in the same response. Each file must be in its own markdown block clearly labeled with its relative target file path (e.g. `demos/title3_taxonomy/tag_failure_modes.py`). Do not use placeholders or truncate files — provide everything ready to run.
3. At the end of the response, write a brief guide on the run order, how to run/test the files, and what expected outputs to check.
4. Keep responses lean: no restating this prompt or plan.md back to me, no long conversational preambles. Just the plan, the complete files, and the run/test guide.
```

---

### Why it's structured this way

- **All files at once** saves time and turns, giving you a complete, runnable demo in a single response, while keeping the output grounded by requiring a brief plan first.
- **Reusing common/ and existing results** prevents the model from rebuilding the shared pipeline or attack logic from scratch. It forces Title 3 to build on top of generated trial logs, and Title 4 to build on top of the common MemoryStore and attack scenario logic.
- **Pinning the metrics/scenario to the document** stops the new instance from quietly redesigning the experiment (e.g., picking different trial counts or different metrics than what's already specified in `plan.md`).