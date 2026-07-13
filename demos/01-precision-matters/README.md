# Title 1 — Does Precision Matter, Again?

Quantization-dependent susceptibility to persistent memory poisoning in a
local LLM agent. Everything here runs entirely on your own machine against
your own local Ollama instance and a local Chroma store — no third-party
systems are involved.

## What this measures

Holding model family fixed (`llama3.2:3b-instruct`), does a MINJA-style
query-only memory injection behave differently across three quantization
levels (Q4_0 / Q8_0 / FP16)? Three metrics per trial, matching the field's
standard framing:

- **Injection Success** — was the malicious record actually written to the store
- **Retrieval Rate** — was it retrieved when the trigger query ran
- **Trigger Success** — did the agent's final output reflect the planted content

## Setup

```bash
pip install -r requirements.txt

ollama pull llama3.2:3b-instruct-q4_0
ollama pull llama3.2:3b-instruct-q8_0
ollama pull llama3.2:3b-instruct-fp16
```

Adjust `config.py` if you're using different tags or a different base model.

## Run order

1. `python ../common/memory_store.py` — smoke-tests Chroma + the embedder in isolation.
2. `python ../common/attack_scenario.py <model_tag>` — runs one full trial end-to-end
   against a single model tag, prints the three metrics and both agent
   responses so you can eyeball whether the scenario is behaving sensibly.
3. `python run_trials.py` — runs `N_TRIALS_PER_PRECISION` trials for each
   precision level in `config.py`, logs every trial to
   `results/trial_log.csv`.
4. `python analyze_results.py` — reads the trial log, prints and saves
   `results/summary_table.csv`, and saves
   `results/precision_comparison.png`.

## Notes

- `MemoryStore.reset()` is called between trials so trials don't leak into
  each other — each trial starts from an empty memory store.
- The attack scenario (`data/trigger_terms.json`) uses a fictional vendor
  on the reserved `.example` TLD, so nothing in the demo references a real,
  resolvable domain.
- Trial counts of 5–10 per condition are for direction validation only —
  say so explicitly if presenting this table anywhere; it isn't
  statistically powered.
