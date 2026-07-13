# Title 2 — Small Agents, Same Sleepers?

Parameter-scale effects on delayed-trigger memory poisoning below the 8B
threshold. Extends the DTA benchmark's model roster downward — DTA's
smallest tested model is 9B; this demo runs the identical MINJA-style
attack against four models in the 1B–4B range instead.

## What's reused vs. new

Reused unchanged from `../common/`:
- `memory_store.py`
- `attack_scenario.py` (same bridging conversation, indication prompt,
  progressive shortening, and scoring logic)
- `data/trigger_terms.json` (identical scenario)

New in this folder:
- `config_small_models.py` — the small-model roster + trial count
- `run_trials_small_models.py` — sweeps *model* instead of *precision*
- `analyze_small_models.py` — summary table + chart keyed by model, not
  precision (Title 1's `analyze_results.py` is hardcoded around precision
  labels, so it couldn't be reused as-is)

## Setup

```bash
ollama pull llama3.2:1b
ollama pull qwen3:1.7b
ollama pull gemma3:1b
ollama pull phi3:3.8b
```

All four are pulled at their default (q4_0) quantization tag and held
constant across this sweep, so the only thing varying is the model —
matching DTA's own fixed-quantization setup. If a tag doesn't resolve,
check `ollama list` / the library page for the current exact tag name.

## Run order

1. Confirm `../common/memory_store.py` and
   `../common/attack_scenario.py` still pass their own standalone checks
   — this folder imports them directly rather than copying them, so if
   those break, this breaks too.
2. `python run_trials_small_models.py` — runs `N_TRIALS_PER_MODEL` (5)
   trials per model, logs to `results/trial_log.csv`.
3. `python analyze_small_models.py` — prints/saves
   `results/summary_table.csv` and `results/model_comparison.png`.

## Notes

- N=5 per model is direction-validation only, same caveat as Title 1 —
  say so out loud if you present this table.
- Frame this explicitly as "extending the DTA model roster downward," not
  as a standalone claim — keeps the novelty tight and citable.
- Small models can behave more erratically in the bridging conversation
  (more likely at 1B than 3–4B) — e.g. losing track of the "remember this"
  instruction, or refusing to summarize. That's not a bug in the harness;
  log it as-is and consider it a candidate entry for Title 3's failure-mode
  taxonomy rather than a trial to discard.
- Trial counts here are per-model, not per-precision, so this table isn't
  directly comparable to Title 1's — treat them as two separate slices of
  the same underlying attack, not one combined result.
