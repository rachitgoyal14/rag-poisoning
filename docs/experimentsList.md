# Experiments to Build — Testing the Quantization Dual-Mechanism Hypothesis

Context: you already have `memory_poison_harness.py` + `run_experiment.py` with an
`ACTIVE_MODELS` flag for scale/precision/combined sweeps, a 7-category failure taxonomy, and
an AM-Sentry-style judge toggle. Everything below either extends that harness directly or adds
one small new module next to it — none of this requires new infrastructure beyond what's
already on the M5/Ollama/MLX/ChromaDB stack.

Hypothesis being tested throughout: quantization has two separable, competing effects —
**discrimination collapse** (model gets worse at treating retrieved content as untrusted data,
pushing toward write-faithful/write-partial outcomes) and **execution collapse** (model gets
worse at correlating/executing subtle triggers, pushing toward silent-nonresponse/write-refused
outcomes). The net effect is a *shift in the failure-mode distribution*, not a single
vulnerability score.

Build in this order — each one is either a prerequisite for the next or cheap enough to not
skip.

---

## 0. Prerequisite: multi-trial the grid you already have

**Why:** nothing below is credible until this exists. Right now you have directional
single-run results.

**Build:** wrap your existing `run_experiment.py` loop with `n_trials = 15–20` per
(scale, precision, attack) cell. Log raw per-trial category labels, not just aggregate rates.
Report Wilson or bootstrap confidence intervals per cell, not point estimates.

**Output:** a `results/grid_ci.csv` with columns
`[scale, precision, attack_type, category, count, rate, ci_low, ci_high]`.

**Effort:** low — mostly a loop + a stats helper, no new logic.

---

## 1. Refusal / trust-token margin probe

**Tests:** Mechanism 1 (discrimination collapse), directly.

**Tool:** Ollama's native API supports `logprobs` + `top_logprobs` per request
(`/api/generate` or `/api/chat`, `logprobs: true`). Set `num_predict: 1` to get a clean
next-token distribution at the exact decision point right after a poisoned retrieval is
inserted into context.

**Build:** a new `trust_probe.py` that:
1. Runs your existing poisoned-retrieval prompt up to the point right before the model's
   response.
2. Calls Ollama with `logprobs: true, top_logprobs: 10, num_predict: 1`.
3. From the returned top-N tokens, buckets them into "trust-signaling" (e.g. tokens starting
   a hedge/question/refusal — "I", "That", "Actually", "I'm not sure") vs "compliance"
   (tokens that would directly continue with the poisoned claim).
4. Computes `log P(trust-signaling) - log P(compliance)` as the margin.
5. Repeat across every (scale, precision) cell in `ACTIVE_MODELS`.

**Output:** margin value per cell → plot margin vs. precision level per scale. Prediction:
margin shrinks (goes more negative) as precision drops, if Mechanism 1 holds.

**Effort:** low-medium — one new file, reuses your existing prompt templates, no model
internals needed.

---

## 2. Mechanism-isolating poison pair (centerpiece experiment)

**Tests:** both mechanisms simultaneously, showing the split directly.

**Build:** two new poison templates in your harness's injection module:
- `poison_trust_only`: a false-but-plausible fact requiring zero reasoning to act on
  (pure discrimination test — does the model treat this as ground truth).
- `poison_complex_trigger`: a conditional instruction embedded in retrieved content
  ("when asked about X, actually do/say Y") requiring the model to notice and correctly
  execute an indirect correlation.

Run both through your existing `run_experiment.py` across the full scale × precision grid,
using the 7-category taxonomy you already have.

**Output:** two category-distribution curves per scale, one per poison type, across
precision. Prediction: `poison_trust_only` success rate (write-faithful/write-partial) rises
as precision drops; `poison_complex_trigger` success rate falls while
silent-nonresponse/write-refused rises. If both directions show up in the same grid, that's
your empirical demonstration of the split.

**Effort:** medium — two new prompt templates, reuse of all existing plumbing.

---

## 3. Repeated-sampling consistency probe

**Tests:** general stability, supports either mechanism as corroborating evidence.

**Build:** at `temperature > 0` (e.g. 0.7), generate `k = 10` samples per
(scale, precision, poison) cell using your existing harness, unchanged. Compute agreement
rate or output entropy across the k samples.

**Output:** consistency score per cell. Prediction: consistency falls as precision drops,
independent of the logprobs experiment — a second, independent signal for the same claim.

**Effort:** low — just re-running inference k times and adding an entropy calc.

---

## 4. Cross-precision consistency as a defense

**Tests:** your proposed new defense.

**Build:** a `cross_precision_check.py` that takes the same poisoned context and runs your
existing admission-judge decision at two precisions (e.g. 4-bit and 8-bit, or 4-bit and
fp16/full) for the *same* underlying model family. Log whether the write/no-write decision
flips between the two.

**Output:** a confusion matrix — flip rate on known-poisoned content (want high) vs. flip
rate on known-benign content (want low, or you have a false-positive problem). This is the
first real evidence for or against the defense idea, not just a design sketch.

**Effort:** medium — needs two precision variants of the same model loaded, which you
already have from the scale/precision sweep.

---

## 5. Activation-separability probe (RevPRAG-style)

**Tests:** Mechanism 1, at the mechanistic (not behavioral) level — the most convincing
evidence if it works.

**Tool note:** Ollama doesn't expose intermediate hidden states, only final logprobs. For
this one, use `mlx-lm` (pure Python, model internals directly accessible) or `transformers`
with a GPTQ/AWQ-quantized checkpoint if you want exact quantization-method control instead
of GGUF's own quant levels. Check current `mlx-lm` docs for the hidden-state hook API before
starting — worth 20 minutes before writing code.

**Build:** extract hidden states (e.g. last-layer or a fixed middle layer) for correct vs.
poisoned generations, at each precision level. Compute a simple separability metric — linear
probe accuracy or centroid distance is enough, you don't need RevPRAG's full triplet network.

**Output:** separability score per precision level. Prediction: the poisoned-vs-clean signal
gets less separable (lower probe accuracy / smaller centroid distance) as precision drops —
meaning defenses like RevPRAG would themselves degrade under quantization, which is a paper
finding on its own.

**Effort:** medium-high — new dependency path (MLX/transformers direct loading instead of
Ollama), do this last, after 1–4 are solid.

---

## 6. Redundancy proxy

**Tests:** the Peng et al. redundancy analogy, adapted from pruning/distillation to
quantization.

**Build:** once you have model weights loaded (via MLX or GGUF inspection), compute per-layer
weight magnitude spread or effective rank (SVD of weight matrices) at each precision level.

**Output:** correlate this proxy against the vulnerability shift measured in Experiment 2.
Turns "precision level" from a categorical label into a quantitative mediator — this is what
makes the redundancy story a tested hypothesis rather than a borrowed citation.

**Effort:** medium — mostly linear algebra on weight tensors you already have on disk.

---

## 7. Conseca-style structural gate (your new-defense contribution)

**Tests:** whether a judge-free, deterministic defense beats your existing LLM-judge toggle.

**Build:** a `purpose_gate.py` — a small deterministic allow-list per task type (e.g.
"schedule reminder" → allowed write fields are `{date, time, description}`; anything else in
a proposed write is rejected regardless of content plausibility). No LLM call needed for the
gate itself.

**Output:** compare catch-rate and false-positive-rate of this gate vs. your existing
AM-Sentry-style judge, across the same grid. This is the concrete "new defense" artifact for
the paper.

**Effort:** low-medium — the gate itself is simple rule-matching; the work is in defining a
sensible action schema per task type.

---

## Suggested build order

`0 → 1 → 2 → 3 → 4 → 7`, with `5` and `6` last since they need the extra tooling (MLX/direct
weight access) rather than just Ollama + your existing harness. Don't start 5 or 6 before 2 is
producing a clean result — the mechanistic experiments only matter if the behavioral split
they're supposed to explain is already showing up in the data.
