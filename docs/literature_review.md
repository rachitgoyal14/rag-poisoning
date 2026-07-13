# Literature Review & Novelty-Gap Analysis
### Persistent Memory Poisoning Demos — Titles 1, 2, 3, 4, 5, 6

**Prepared:** July 13, 2026
**Scope note (read first):** This review verified every paper cited in your two source files against live search (arXiv/ACM/ResearchGate), pulled real abstracts and, where possible, full text, and then ran targeted adversarial searches to try to find prior work that already does what each title claims. It is **not** the full 60+ query sweep the brief specifies (10 example queries × 6 titles). Given the scope, I prioritized (a) verifying every paper you already cite actually says what you think it says, and (b) chasing the highest-risk adversarial queries — anything combining "RAG/memory poisoning" with "quantization" or "small local models," since that's where your novelty claim is riskiest. Section 8 in each title and the final "Recommended Next Experiments" flag exactly which query families still need running before you present this as complete to Dr. Kashyap.

One correction to your source files up front: **"LM-SHIELD '26" is not a paper title** — it's the name of the workshop (*Workshop on Privacy in Large Language Models (LLM) and Natural Language Processing (NLP) 2026*). The paper itself is **Jaiswal, Pratap, Saraswati, Kasyap & Tripathy, "Analysis of LLMs Against Prompt Injection and Jailbreak Attacks"** (arXiv:2602.22242), published in the LM-SHIELD '26 proceedings. I've used the real title below and kept "LM-SHIELD '26" only as the venue name. I also confirmed "Aaditya Pratap" as a co-author, which matches your collaborator Aditya.

---

## Title 1 — "Does Precision Matter, Again?"

### 1. Our Research Question
Does GGUF quantization level (Q4_0 vs Q8_0 vs FP16) of a single local model (Llama 3.2 3B-Instruct) affect *downstream* memory-poisoning outcomes — specifically retrieval rate and delayed-trigger attack success — in a MINJA-style query-only memory injection scenario, holding the attack and model family fixed?

### 2. Our Observed Result
N=10 trials per precision level. Injection success is 100% at all three precisions (writing the record is trivial and precision-independent). Retrieval rate and trigger success (ASR) are ~0.90/0.90 at Q4_0, versus ~0.40–0.50/0.50 at Q8_0 and FP16 — roughly a 2x gap between the most-compressed variant and the other two, with Q8_0 and FP16 close to each other (evidence against a simple monotonic "more compression = more vulnerable" story; more consistent with a threshold somewhere between 4-bit and 8-bit). Single model family, single attack scenario/trigger phrase, N=10 — direction-validating, not statistically powered.

### 3. Closest Prior Literature

**Paper:** Defense effectiveness across architectural layers: a mechanistic evaluation of persistent memory attacks on stateful LLM agents (the "DTA" benchmark)
**Authors:** Jun Wen Leong
**Year / Venue:** 2026, preprint (under review)
**URL:** https://arxiv.org/abs/2605.08442

**What the paper studied:** Six defenses across four architectural layers (input, retrieval, action, memory) against delayed-trigger memory-poisoning attacks, on 9 open-source models, 5,040 runs total, N=40 per condition, with 108 pre-specified comparisons.
**Experimental scope:** 9 open-source models — the smallest being qwen3.5:9b — evaluated at a single, unspecified inference precision per model (not varied as an experimental axis). Seven defense conditions (no defense, Minimizer, Sanitizer, RAG Sanitizer, RAG LLM Judge, Prompt Hardening, Memory Sandbox).
**Relevant finding:** Five of six defenses fail to meaningfully reduce ASR; input-layer defenses never even see the payload because it arrives via RAG, not user input, and retrieval-layer defenses can't distinguish the compliance-framed payload from legitimate policy content.
**Where the paper stops:** Every model tested is 9B or larger, and each model is run at one fixed precision — quantization is never an independent variable. The paper's own text explicitly says results "may differ from full-precision or API-served versions," identifying exactly the open question Title 1 tests, but does not test it.
**Explicit author limitation/future work:** The "may differ from full-precision or API-served versions" line functions as a stated scope limitation, not a result — confirmed present in the abstract-adjacent framing of the released materials.

**Paper:** Fine-Tuning, Quantization, and LLMs: Navigating Unintended Outcomes (also indexed as "Increased LLM Vulnerabilities from Fine-tuning and Quantization")
**Authors:** Divyanshu Kumar, Anurakt Kumar, Sahil Agarwal, Prashanth Harshangi (Enkrypt AI)
**Year / Venue:** 2024, arXiv (v3 Sep 2024)
**URL:** https://arxiv.org/abs/2404.04392

**What the paper studied:** Impact of fine-tuning and quantization on *jailbreak* success rates (not memory/RAG poisoning) across Mistral, Llama, Qwen, and MosaicML foundation models and their variants.
**Experimental scope:** Direct jailbreak/prompt-based attacks on the model itself; quantization compared as a variable, but the object under attack is the model's alignment, not a retrieval/memory pipeline.
**Relevant finding:** Fine-tuning generally increases jailbreak success; <cite index="48-1">quantization has variable effects rather than a clean monotonic trend</cite> — directionally consistent with Title 1's "not a straight line" finding, but on a completely different attack surface.
**Where the paper stops:** No RAG, no memory store, no retrieval step at all — quantization's effect on *retrieval and trigger* behavior (the mechanism Title 1 isolates) is outside its scope by construction.
**Explicit author limitation/future work:** Not checked in full text this session; flagged for follow-up before citing further.

**Paper:** On Jailbreaking Quantized Language Models Through Fault Injection Attacks
**Authors:** (not fully captured this session — cite with caution pending author-list confirmation)
**Year / Venue:** 2025, arXiv
**URL:** https://arxiv.org/pdf/2507.03236

**What the paper studied:** Gradient-guided bit-flip/fault-injection jailbreaks on Llama-3.2-3B, Phi-4-mini, and Llama-3-8B across FP16, FP8, INT8, and INT4.
**Experimental scope:** Weight-level fault injection, not black-box query-only memory poisoning.
**Relevant finding:** Found the **opposite direction** from Title 1 for their attack type — <cite index="108-1">attacks readily achieve above 80% success on FP16, while FP8 and INT8 models show success below 20% and 50% respectively</cite> within a fixed perturbation budget, i.e. lower precision was *more resistant* to their specific fault-injection mechanism.
**Where the paper stops:** Different threat model entirely (attacker controls bit-level weight perturbations, not black-box queries); the directional mismatch with Title 1 is worth noting explicitly rather than ignoring — it's evidence that "precision effect on attack success" is mechanism-specific and doesn't generalize across attack classes, which strengthens rather than weakens the case that Title 1 needs to be scoped precisely to *retrieval-mediated* memory poisoning.
**Explicit author limitation/future work:** Not checked.

**Paper:** Exploiting LLM Quantization / Widening the Gap: Exploiting LLM Quantization via Outlier Injection
**Authors:** Kazuki Egashira, Mark Vero, Robin Staab, Jingxuan He, Martin Vechev (2405.18137); Xiaohua Zhan, Kazuki Egashira, Robin Staab, Mark Vero, Martin Vechev (2605.15152)
**Year / Venue:** 2024 / 2026, arXiv
**URL:** https://arxiv.org/abs/2405.18137 · https://arxiv.org/abs/2605.15152

**What the paper studied:** A supply-chain attack where an adversary *releases* a model engineered so the full-precision weights look benign but the **quantized** version is malicious — the attacker controls the model, not the retrieval pipeline.
**Experimental scope:** GGUF k-quant, then (in the 2026 follow-up) AWQ/GPTQ/GGUF I-quants, via deliberate outlier injection into weights.
**Relevant finding:** Confirms quantization is a viable place to hide adversarial behavior, but via a completely different mechanism — weight-space engineering, not attack-success-rate variation of an existing black-box memory-injection attack.
**Where the paper stops:** No RAG, no agent memory, no query-only attacker — this line of work answers "can quantization hide a backdoor a model publisher planted," not "does quantization change how vulnerable an off-the-shelf model is to memory poisoning."
**Explicit author limitation/future work:** Not checked in full text.

### 4. Literature Comparison Matrix

| Paper | Persistent Memory | Query-Only Poisoning | Delayed Trigger | Small Local Models (1–4B) | Quantization Compared | Cross-Model Analysis | Failure Taxonomy | Defense × Precision |
|---|---|---|---|---|---|---|---|---|
| DTA (Leong, 2605.08442) | Yes | Yes | Yes | Not evaluated (smallest is 9B) | Not evaluated (fixed per model) | Yes (9 models) | Not reported | Not evaluated |
| Kumar et al. (2404.04392) | No | No (direct jailbreak) | No | Not evaluated | Yes | Yes | Not reported | Not evaluated |
| Fault-injection quant. jailbreak (2507.03236) | No | No | No | Yes (3B–8B) | Yes | Yes | Not reported | Not evaluated |
| Egashira et al. / Widening the Gap | No | No | No | Not the focus (backbone varies) | Yes (attack-conditioned) | Yes | Not reported | Not evaluated |
| **Title 1 (ours)** | **Yes** | **Yes (MINJA-style)** | **No (single-turn retrieval, not delayed)** | **No (3B only)** | **Yes** | **No (one model family)** | **Not reported** | **Not evaluated** |

### 5. Exact Research Gap
Existing literature has separately established that (a) memory-poisoning attacks on persistent-memory LLM agents work and that most defenses against them fail (DTA), and (b) quantization has a non-trivial, non-monotonic effect on model *jailbreak* susceptibility (Kumar et al.; fault-injection work). We found no evaluation that holds a memory-poisoning attack and model fixed and varies **only** inference precision to measure the effect on *retrieval and trigger* rates specifically — the DTA benchmark, which is closest, explicitly flags this as an open scope limitation rather than testing it. Title 1 extends DTA along exactly the axis DTA's own limitations paragraph names.

### 6. How Our Work Extends Prior Literature
**Closest prior work does:** Benchmarks memory-poisoning defenses across 9 models (≥9B) at one precision each (DTA), and separately shows quantization affects jailbreak ASR non-monotonically on the model itself (Kumar et al.).

**It does not evaluate:** Whether varying quantization on a *single* model, holding the memory-poisoning attack and architecture fixed, changes retrieval/trigger outcomes.

**Our experiment evaluates:** Retrieval rate and trigger ASR for Llama 3.2 3B-Instruct at Q4_0/Q8_0/FP16 under a MINJA-style query-only injection.

**Observed result:** Injection is precision-invariant (100% at all three); retrieval/trigger nearly doubles at Q4_0 versus Q8_0/FP16, with the two higher-precision variants close together (threshold-like, not linear).

**Why this matters:** If confirmed at scale, it means the *most commonly deployed* precision for local/edge agent deployments (4-bit) may be systematically more exposed to this attack class than benchmarks run at FP16/API precision would suggest — directly actionable for anyone citing DTA-style numbers to justify a security posture for a quantized local deployment.

### 7. Novelty Confidence
**MEDIUM.** No directly comparable experiment (same attack, same model, precision as the sole varied axis) was found. But the surrounding literature is dense enough — DTA on the memory-poisoning side, Kumar et al./fault-injection work on the quantization-and-safety side — that this reads as a natural, low-risk gap someone else could fill quickly, and a single-model/single-scenario N=10 study makes a MEDIUM rather than HIGH claim appropriate until replicated on a second model family. Closest competing paper: DTA (2605.08442), whose own limitations paragraph is the paper's strongest asset, but which does not run the experiment.

### 8. Questions and Risks Before Claiming Novelty
- **Not yet checked:** whether the ~24 remaining example adversarial queries from the brief (e.g. "RAG poisoning" + model family, "retrieval poisoning" + INT4/INT8/FP16 as an exact phrase match) turn up something closer than what surfaced here. What was run supports the gap; it isn't exhaustive.
- Single model family (Llama 3.2 3B), single trigger phrase, N=10 — the "threshold not slope" claim needs a second model family before it's presentable as a finding rather than an anecdote.
- Scoring is automatic/heuristic, not human-verified (per your own cross-cutting caveats).
- The `summary_table.csv`/`trial_log.csv` overwrite issue (Section 0 of your final report) means these Title 1 numbers were *reconstructed*, not read directly off the original run — worth a sentence of methodological transparency if this goes to publication, even though your cross-check against `confound_audit_table.csv` is a reasonable mitigation.
- Egashira/Widening-the-Gap and the fault-injection paper are close enough in *keywords* ("quantization" + "attack success rate") that a reviewer may initially conflate them with your claim; the "Why this matters" and Section 6 framing above should make the mechanism distinction explicit in any write-up.

---

## Title 2 — "Small Agents, Same Sleepers?"

### 1. Our Research Question
Among small (~1–4B) locally-hosted LLMs, does memory-poisoning vulnerability scale with parameter count, or is it driven more by model family/training?

### 2. Our Observed Result
N=5 per model, one quantization point (Q4_0) each. Llama-3.2-1B: 100%/60% retrieval/trigger. Qwen3-1.7B: 40%/40%. Gemma3-1B: 20%/0%. Phi-3-3.8B: 40%/20%* (*confounded — 2 of 5 trials produced incoherent, off-topic output, likely a harness/template issue, not a security finding). The two 1B models sit at opposite extremes (most and least vulnerable of the four); parameter count alone does not predict vulnerability in this sample.

### 3. Closest Prior Literature

**Paper:** When Agents Remember Too Much: Memory Poisoning Attacks on Large Language Model Agents (introduces the "GhostWriter" attack)
**Authors:** George Torres, Sharad Shrestha, Satyajayant Misra
**Year / Venue:** 2026, arXiv (posted July 6, 2026 — one week before this review)
**URL:** https://arxiv.org/abs/2607.06595

**What the paper studied:** A two-phase (injection + activation) memory-poisoning attack against five agent architectures (A-Mem, Mem0, ExpeL, Letta, MemoryOS) with a personal-assistant email/calendar threat model, plus a proposed two-stage defense (AM-Sentry).
**Experimental scope:** Four LLM backbones — GPT-5.4-mini, DeepSeek-V4-Flash, Gemini-2.5-Flash (all via API), and <cite index="112-1">Llama 3.1 8B hosted locally via Ollama using Q4_K_M quantization</cite>. <cite index="112-2">Achieves roughly 98% injection and roughly 60% activation success on average across agents</cite> — strikingly close to your Title 2 injection numbers.
**Relevant finding:** This is the single closest paper found in this review to your local/small-model setup. It's from the same week as your run.
**Where the paper stops:** Only **one** local/quantized model (Llama 3.1 8B, above your 1–4B range) at a **single, fixed** quantization level — it does not compare across a family of small (1–4B) models, and quantization is not an independent variable at all (it's an implementation detail of running one of four backbones, not a studied axis). It also does not report a non-monotonic size-vs-vulnerability finding, because it doesn't vary size within a controlled sweep.
**Explicit author limitation/future work:** Not yet checked in the paper's Section 8 (Limitations & Future Work) — this is a priority follow-up, since a paper this closely adjacent, published this recently, is the single biggest risk to Title 2's novelty and its stated limitations may directly bound your claim.

**Paper:** Analysis of LLMs Against Prompt Injection and Jailbreak Attacks
**Authors:** Piyush Jaiswal, Aaditya Pratap, Shreyansh Saraswati, Harsh Kasyap, Somanath Tripathy
**Year / Venue:** LM-SHIELD '26 (Workshop on Privacy in LLM and NLP 2026); arXiv Feb 2026
**URL:** https://arxiv.org/abs/2602.22242

**What the paper studied:** Prompt-injection and jailbreak vulnerability (not memory/RAG poisoning) <cite index="32-1">using a large, manually curated dataset across multiple open-source LLMs, including Phi, Mistral, DeepSeek-R1, Llama 3.2, Qwen, and Gemma variants</cite>, with five inference-time defenses.
**Experimental scope:** Direct prompt attacks on the model, no retrieval or memory component; overlapping model families (Phi, Llama, Qwen, Gemma) but different task.
**Relevant finding:** <cite index="32-1">Significant behavioral variation across models, including refusal responses and complete silent non-responsiveness triggered by internal safety mechanisms</cite> — direct methodological ancestor for the idea that small models fail in qualitatively different, non-scalar ways, which supports (but doesn't itself demonstrate) Title 2's non-monotonic finding in the memory-poisoning setting.
**Where the paper stops:** No memory, no retrieval, no persistence across turns — this paper's model-family comparison is on jailbreak susceptibility, not memory-poisoning trigger success.
**Explicit author limitation/future work:** Not checked in full text this session.

**Paper:** Stochastic Monkeys at Play: Random Augmentations Cheaply Break LLM Safety Alignment
**Authors:** Jason Vega, Junsheng Huang, Gaokai Zhang, Hangoo Kang, Minjia Zhang, Gagandeep Singh
**Year / Venue:** 2024 (arXiv), NeurIPS-track workshop-adjacent
**URL:** https://arxiv.org/abs/2411.02785

**What the paper studied:** <cite index="33-1">How simple random augmentations to the input prompt affect safety alignment effectiveness across 17 different models, investigating augmentation type, model size, quantization, fine-tuning-based defenses, and decoding strategies</cite> — a jailbreak-style attack, not memory poisoning.
**Experimental scope:** 17 models spanning multiple sizes and quantization levels; the specific claim in your source doc ("§A.5, non-monotonic size-vs-safety") was **not independently confirmed** this session — flagged, not verified.
**Relevant finding:** If the §A.5 claim holds up on inspection, this would be a genuine methodological precedent for reporting non-monotonic size effects on safety, but in a jailbreak (not memory-poisoning) context.
**Where the paper stops:** Jailbreak attack surface, not memory/RAG.
**Explicit author limitation/future work:** Not checked — **do not cite the §A.5 claim as confirmed until someone reads that section directly.**

### 4. Literature Comparison Matrix

| Paper | Persistent Memory | Query-Only Poisoning | Delayed Trigger | Small Local Models (1–4B) | Quantization Compared | Cross-Model Family Analysis | Failure Taxonomy | Defense × Precision |
|---|---|---|---|---|---|---|---|---|
| GhostWriter (2607.06595) | Yes | Yes (indirect, via email/calendar tool inputs) | Not reported as "delayed"; activation on next benign query | Not evaluated (only Llama 3.1 8B local) | Not evaluated (single fixed quant) | Partial (4 backbones, mostly API) | Not reported (P1/P2 success only) | Not evaluated |
| LM-SHIELD '26 (2602.22242) | No | No | No | Yes (Phi, Llama 3.2, Qwen, Gemma variants) | Not reported | Yes | Yes (silent non-responsiveness) | Yes (5 inference-time defenses, no quant axis) |
| Stochastic Monkeys (2411.02785) | No | No | No | Partial (model size varied, exact range unconfirmed) | Yes | Yes | Not reported | Not evaluated |
| **Title 2 (ours)** | **Yes** | **Yes** | **No** | **Yes (1B–3.8B, four families)** | **No (fixed at Q4_0)** | **Yes (4 families)** | **No (separate title)** | **Not evaluated** |

### 5. Exact Research Gap
The closest paper, GhostWriter (one week old at time of writing), establishes that memory poisoning works against small local models via Ollama, but tests exactly one local model at one size and one quantization level rather than sweeping a family of 1–4B models. LM-SHIELD '26 sweeps small-model families for a *different* attack (jailbreak) and finds qualitatively distinct, non-scalar failure behavior; Title 2 asks whether that same "family matters more than size" pattern replicates for memory-poisoning trigger success specifically, and finds a similar non-monotonic result (two 1B models at opposite extremes).

### 6. How Our Work Extends Prior Literature
**Closest prior work does:** Demonstrates memory poisoning works on real agent architectures with one local 8B model (GhostWriter), and separately shows small-model jailbreak resistance is family-dependent, not size-dependent (LM-SHIELD '26).

**It does not evaluate:** A controlled sweep of multiple small (1–4B) local models, same attack, same quantization, isolating family/training as the driver of memory-poisoning vulnerability specifically.

**Our experiment evaluates:** Four ~1–4B models (Llama-3.2-1B, Qwen3-1.7B, Gemma3-1B, Phi-3-3.8B) at fixed Q4_0 under the same MINJA-style attack.

**Observed result:** Llama-3.2-1B most vulnerable (100%/60%), Gemma3-1B least (20%/0%) — two same-size models at opposite ends; Phi-3's row is confounded by a likely harness bug.

**Why this matters:** For anyone choosing a small local model for an agent deployment on vulnerability grounds, "bigger is safer" is not a reliable heuristic within this size band — family/alignment style appears to matter more, echoing (but not identical to) the LM-SHIELD '26 jailbreak finding in a different attack class.

### 7. Novelty Confidence
**MEDIUM**, trending toward **MEDIUM-LOW** pending the GhostWriter Section 8 limitations check. GhostWriter is close enough — same week, same general attack family, real local-Ollama-quantized-model deployment — that it is the single greatest risk to this title's novelty. It has not (per what was captured) run a *multi-model small-family sweep*, but a supervisor or reviewer will very likely ask "did you check GhostWriter's limitations section" and the honest answer right now is "not yet."

### 8. Questions and Risks Before Claiming Novelty
- **Highest-priority follow-up in this entire review:** read GhostWriter's Section 8 (Limitations & Future Work) in full — if they explicitly flag "we only tested one local quantized model; future work should sweep model families" as a limitation, that both validates and slightly undercuts your novelty claim (validates the gap exists; undercuts "we found it first," since they'd have named it).
- Confirm the Stochastic Monkeys §A.5 claim before using it as precedent.
- Phi-3's row needs the harness bug fixed and a re-run before it can be cited anywhere, including in a novelty argument (a broken row can't support "family matters more than size").
- N=5 per model is very small for a four-way comparison; the "opposite extremes" framing is suggestive, not statistically established.

---

## Title 3 — "Silent Sleepers" Failure-Mode Taxonomy

### 1. Our Research Question
When a memory-poisoning attack is attempted against small local LLM agents, what proportion of trials fall into each of a pre-specified set of outcome categories (clean negative, faithful write, retrieved-ignored, retrieved-partial, corrupted write, write refused, hallucinated memory)?

### 2. Our Observed Result
N=57 valid tagged trials (reconciled across Titles 1 and 2's raw data, correcting a data-provenance mismatch versus an earlier 35-trial partial file). Only 4 of 7 planned categories occurred: clean negative 49.1%, faithful write 35.1%, retrieved-ignored 8.8%, retrieved-partial 7.0%. Corrupted write, write refused, and hallucinated memory: 0% each. Scoring is automatic/heuristic (embedding similarity), not human-verified; `manual_tag` is empty for all 57 rows.

### 3. Closest Prior Literature

**Paper:** Analysis of LLMs Against Prompt Injection and Jailbreak Attacks
**Authors:** Jaiswal, Pratap, Saraswati, Kasyap, Tripathy
**Year / Venue:** LM-SHIELD '26; arXiv:2602.22242
**URL:** https://arxiv.org/abs/2602.22242

**What the paper studied:** Prompt injection/jailbreak vulnerability with a labeling scheme distinguishing vulnerable, non-vulnerable-with-refusal, and a distinct **silent non-responsiveness** category.
**Experimental scope:** Confirmed directly: <cite index="32-2">a response is classified as non-vulnerable if the model refuses, gives a safety warning, or redirects without disclosing restricted content; refusals followed by partial unsafe assistance are still labeled vulnerable; empty or silent responses triggered by internal safety gating are categorized separately as silent non-response and analyzed as a distinct failure mode</cite>. <cite index="32-2">This approach allows scalable and consistent annotation across thousands of responses approximating human evaluation quality</cite> — but note this is a claim of *approximation*, not verified human agreement, in the source paper itself.
**Relevant finding:** The "silent non-responsiveness" category is real and directly precedes your Title 3 taxonomy's framing, exactly as your source doc claims.
**Where the paper stops:** This taxonomy is for jailbreak/prompt-injection responses on the model directly — it has no analog to "written-but-never-retrieved," "retrieved-but-ignored," or "corrupted write," because there is no persistent memory store in that experimental setup. It's a genuine ancestor, not an overlapping taxonomy.
**Explicit author limitation/future work:** Not checked in full text this session.

**Paper:** RAS-Eval: A Comprehensive Benchmark for Security Evaluation of LLM Agents in Real-World Environments
**Authors:** Yuchuan Fu, Xiaohan Yuan, Dongxia Wang
**Year / Venue:** 2025, arXiv:2506.15253
**URL:** https://arxiv.org/abs/2506.15253

**What the paper studied:** A general LLM-agent security benchmark (80 test cases, 3,802 attack tasks across 11 CWE categories) with an atomic failure-pattern taxonomy.
**Experimental scope:** <cite index="44-1">Compound failures are recorded when multiple atomic modes co-occur; null execution can only appear alone; combining atomic patterns yields up to 32 different reasons for failure</cite>. This is a structural precedent for building a combinable, root-cause-oriented failure taxonomy, exactly as your source doc describes.
**Relevant finding:** <cite index="41-1">Scaling laws held for security capabilities in their benchmark, with larger models outperforming smaller counterparts</cite> — worth flagging as a point of tension with Title 2's non-monotonic finding, though RAS-Eval's models and attack types differ enough (general CWE-mapped tool-use attacks, not memory-poisoning specifically, and likely larger models overall) that this isn't a direct contradiction, just a nuance to address if a reviewer raises it.
**Where the paper stops:** General agent/tool-use security taxonomy, not a memory-write-lifecycle taxonomy — no categories analogous to "faithful write" or "clean negative" tied to a persistent memory store.
**Explicit author limitation/future work:** Not checked.

**Paper:** A Failure-Mode Benchmark for Polymorphic Sybil Poisoning in RAG
**Authors:** Donghyun Lee, Juntae Kim
**Year / Venue:** 2026, arXiv:2607.03739
**URL:** https://arxiv.org/pdf/2607.03739

**What the paper studied:** A four-category outcome partition for **retrieval** poisoning specifically — <cite index="119-1">gold, hijack, abstention, and drift</cite> — with an instance-level paired clean-to-poison transition matrix.
**Experimental scope:** Static-corpus RAG poisoning (Sybil/coordinated document injection), not persistent agent memory; reader-output classification, not memory-write classification.
**Relevant finding:** A close structural cousin — four mutually exclusive outcome categories for a poisoning attack — but the categories are about what the *reader/generator* does with poisoned retrieval, not whether a *write* to a persistent store succeeds, is retrieved, or is acted on. This is the closest failure-taxonomy paper found for a poisoning attack specifically (closer than RAS-Eval, which is general-purpose agent security).
**Where the paper stops:** No memory persistence, no write-time categories (corrupted write, write refused) — the taxonomy is entirely retrieval/generation-side.
**Explicit author limitation/future work:** Not checked.

### 4. Literature Comparison Matrix

| Paper | Persistent Memory | Query-Only Poisoning | Delayed Trigger | Small Local Models | Quantization Compared | Cross-Model Analysis | Failure Taxonomy (memory-write-lifecycle) | Defense × Precision |
|---|---|---|---|---|---|---|---|---|
| LM-SHIELD '26 (2602.22242) | No | No | No | Yes | Not reported | Yes | Partial (silent non-response, but no memory-write categories) | Not evaluated |
| RAS-Eval (2506.15253) | Not specific to memory | No | No | Not the focus | Not reported | Yes | Yes (32 combinable atomic patterns, general agent/tool-use) | Not evaluated |
| Sybil RAG failure-mode benchmark (2607.03739) | No (static corpus) | No | No | Not reported | Not reported | Not the focus | Yes (4-way reader-output partition) | Not evaluated |
| **Title 3 (ours)** | **Yes** | **Yes** | **No** | **Yes** | **Partial (spans Title 1's precision sweep)** | **Yes** | **Yes (7-category memory-write lifecycle, 4 observed)** | **Not evaluated** |

### 5. Exact Research Gap
Prior work has built failure taxonomies for jailbreak responses (LM-SHIELD '26, including a "silent non-responsiveness" category you directly inherit), for general agent/tool-use security (RAS-Eval's combinable atomic patterns), and for RAG reader-output classification under poisoning (the Sybil benchmark's gold/hijack/abstention/drift). We found no taxonomy organized around the **write-then-retrieve lifecycle of a persistent memory store** under a poisoning attack specifically (write success → retrieval → faithful reflection vs. ignored vs. partial vs. corrupted vs. refused vs. hallucinated). Title 3 is a genuine synthesis across two lineages (jailbreak-response taxonomies and agent-security taxonomies) applied to a memory-write axis that neither directly covers.

### 6. How Our Work Extends Prior Literature
**Closest prior work does:** Provides a "silent non-response" category for jailbreak outputs (LM-SHIELD '26) and a combinable atomic-failure structure for general agent security (RAS-Eval).

**It does not evaluate:** Outcomes organized around whether a *memory write* survives, is retrieved, and is faithfully versus partially versus not acted on.

**Our experiment evaluates:** A 7-category memory-write-lifecycle taxonomy, empirically populated from 57 trials.

**Observed result:** Only 4 of 7 categories occurred; corrupted write, write refused, and hallucinated memory were never observed in this run.

**Why this matters:** The absence of three planned categories is itself informative — it's an open question whether they're genuinely rare in this attack class or whether the current single-scenario, single-trigger-phrase design can't surface them, which is exactly the kind of question a taxonomy paper should raise rather than resolve prematurely.

### 7. Novelty Confidence
**MEDIUM.** The individual pieces (silent-response categorization, combinable atomic taxonomies, RAG-poisoning outcome partitions) all exist separately and are legitimately cited as ancestors. No paper found combines them into a memory-write-lifecycle taxonomy. The main risk to this claim isn't a missed competing paper so much as scope: at N=57 with automatic-only scoring and 3 of 7 categories unobserved, this currently reads as a preliminary category scaffold rather than a validated taxonomy, which affects how strongly the novelty claim can be stated even if it's directionally correct.

### 8. Questions and Risks Before Claiming Novelty
- Zero human-verified tags (`manual_tag` empty for all 57 rows) is the single biggest weakness for a taxonomy paper specifically — taxonomies live or die on inter-rater agreement, and there currently is none.
- Single attack scenario/trigger phrase (TravelWiz/Paris-Kyoto) — can't yet claim the taxonomy generalizes to other poisoning payloads.
- Recommend explicitly searching for taxonomy work from the memory-agent-security survey lineage (arXiv:2604.16548's citation list, e.g. its "Poison once, exploit forever" citation arXiv:2604.02623) before finalizing — that survey's Table 3 organizes threats by memory lifecycle phase (Write, Store, Retrieve, Execute, Share, Forget), which is conceptually adjacent enough to Title 3 that it should be checked directly rather than assumed distinct.

---

## Title 4 — "Forget Me Not" (Defense Under Quantization)

### 1. Our Research Question
Does a lightweight LLM-judge defense against memory-poisoning attacks perform differently at different inference precisions (Q4_0 vs FP16), and does its blocking behavior correlate with which attacks actually succeed?

### 2. Our Observed Result
N=5 per condition. ASR without defense: 0.80 (Q4_0), 0.40 (FP16). ASR with the judge defense: identical — 0.80 (Q4_0), 0.40 (FP16). Judge block rate: 20% at Q4_0, 60% at FP16 — the judge blocks *more* at FP16 but this doesn't translate into any ASR reduction at either precision; its blocking decisions don't correlate with which writes actually mattered.

### 3. Closest Prior Literature

**Paper:** DTA benchmark (Leong, 2026)
**URL:** https://arxiv.org/abs/2605.08442

**What the paper studied:** Six defenses (including an "RAG LLM Judge") against delayed-trigger memory-poisoning attacks across 9 models.
**Experimental scope:** As in Title 1's entry — 9 models ≥9B, fixed precision per model, no precision sweep.
**Relevant finding:** <cite index="5-1">Five of six defenses fail to meaningfully reduce ASR; retrieval-layer defenses like the RAG LLM Judge observe the payload but fail to detect it because the compliance-framed document is indistinguishable from legitimate policy content at the classifier's operating point</cite> — this is essentially the same failure mode Title 4 reproduces at small local scale, and the mechanism description (judge sees it, can't distinguish it from something legitimate) matches your own finding that block decisions don't correlate with actual attack success.
**Where the paper stops:** Never varies precision for the same model+defense pair — "does the *already-established* defense failure hold at different quantization levels" is untested.
**Explicit author limitation/future work:** Not checked in full text.

**Paper:** GhostWriter / AM-Sentry (Torres, Shrestha, Misra, 2026)
**URL:** https://arxiv.org/abs/2607.06595

**What the paper studied:** A two-stage LLM-judge-based defense (memory-saving policy + retrieval screen) against a memory-poisoning attack, with three policy strictness levels.
**Experimental scope:** Local model tested is Llama 3.1 8B at a single fixed Q4_K_M quantization — the defense evaluation does not vary precision, same limitation as DTA for this specific question.
**Relevant finding:** Not yet extracted whether AM-Sentry's effectiveness numbers show the same "blocking more doesn't reduce ASR" pattern Title 4 found — worth checking directly since if AM-Sentry's judge *does* reduce ASR while Title 4's simpler judge doesn't, that's a useful contrast for your write-up (single-field LLM-judge blocking vs. structured multi-field policy scoring may matter more than precision).
**Where the paper stops:** No precision sweep; defense architecture is more elaborate than Title 4's single-judge design, so a direct comparison needs care.
**Explicit author limitation/future work:** Not checked — same priority flag as under Title 2.

**Paper:** Memory Poisoning Attack and Defense on Memory Based LLM-Agents
**Authors:** (not fully captured — cite with author-list caveat)
**Year / Venue:** 2026, arXiv:2601.05504
**URL:** https://arxiv.org/abs/2601.05504

**What the paper studied:** Robustness of MINJA-style attacks and defenses under realistic conditions, <cite index="103-1">varying initial memory state, number of indication prompts, and retrieval parameters, on GPT-4o-mini, Gemini-2.0-Flash, and Llama-3.1-8B-Instruct using MIMIC-III clinical data</cite>.
**Experimental scope:** Explicitly investigates "effective defensive mechanisms" as a stated gap, per the abstract — but the varied dimensions are memory state / prompt count / retrieval parameters, not quantization; Llama-3.1-8B-Instruct's precision is not stated as varied.
**Relevant finding:** Another paper explicitly framing "defense robustness under realistic conditions" as an open gap — supports the general framing that defense evaluation for memory poisoning is immature, without directly overlapping on the precision axis.
**Where the paper stops:** No quantization axis found.
**Explicit author limitation/future work:** Not checked.

### 4. Literature Comparison Matrix

| Paper | Persistent Memory | Query-Only Poisoning | Delayed Trigger | Small Local Models | Quantization Compared | Cross-Model Analysis | Failure Taxonomy | Defense × Precision |
|---|---|---|---|---|---|---|---|---|
| DTA (2605.08442) | Yes | Yes | Yes | No | No | Yes | No | **No** (defense evaluated but not × precision) |
| GhostWriter / AM-Sentry (2607.06595) | Yes | Partial | Not reported as delayed | No (one 8B local model) | No (fixed Q4_K_M) | Partial | No | **No** |
| MINJA robustness/defense (2601.05504) | Yes | Yes | Not reported | No | No | Yes (3 models) | No | **No** |
| **Title 4 (ours)** | **Yes** | **Yes** | **Yes** | **Yes (3B)** | **Yes (2 levels)** | **No (1 model)** | **No** | **Yes** |

### 5. Exact Research Gap
Multiple papers establish that LLM-judge-style defenses against memory poisoning fail or under-perform (DTA's RAG LLM Judge; implicitly, the general immaturity flagged in the MINJA-defense-robustness paper), and at least one closely adjacent paper (GhostWriter/AM-Sentry) builds a more elaborate judge-based defense but fixes quantization rather than varying it. We found no evaluation that holds a single lightweight defense and model fixed and varies **only precision** to ask whether defense effectiveness (and specifically, whether blocking decisions correlate with actual attack outcomes) changes with quantization. This is the "defense × precision" cell that is empty across every comparable paper found.

### 6. How Our Work Extends Prior Literature
**Closest prior work does:** Shows LLM-judge defenses against memory poisoning generally fail because they can't distinguish poisoned-but-compliance-framed content from legitimate content (DTA), and builds more sophisticated multi-field judge defenses without a precision axis (AM-Sentry).

**It does not evaluate:** Whether that judge failure mode — or the judge's raw blocking behavior — changes as a function of the *defended model's* inference precision.

**Our experiment evaluates:** A single LLM-judge defense at Q4_0 vs. FP16, same model, same attack.

**Observed result:** Zero ASR reduction at either precision; the judge blocks 3x more often at FP16 (60% vs 20%) with no corresponding drop in ASR.

**Why this matters:** This is a stronger, more specific claim than "the defense doesn't work" — it says the judge's decisions are effectively decoupled from ground truth at *both* precisions, which is a sharper diagnostic than an aggregate ASR number and directly informs whether precision-aware defense tuning is worth pursuing (this pilot suggests: probably not, for this defense design).

### 7. Novelty Confidence
**MEDIUM-HIGH** for the narrow "defense × precision" cell specifically — this genuinely appears empty across every paper checked. Pulled down from HIGH because N=5 per condition is a very small base for any defense-effectiveness claim (your own report says this explicitly — "good enough for a meeting slide, not a paper claim yet"), and because the underlying *reason* the defense fails (judge can't distinguish poisoned from legitimate content) is already well-established by DTA, so the incremental contribution is narrower than it might first appear: not "defenses fail" (known) but "defenses fail *the same way* regardless of precision" (the new bit).

### 8. Questions and Risks Before Claiming Novelty
- Check AM-Sentry's actual effectiveness numbers directly — if their more elaborate defense *does* show meaningful ASR reduction, that changes the framing from "defenses fail" to "simple single-field judges fail, structured multi-field policies might not," which is a more precise and more defensible claim.
- N=5 per condition (20 trials total across the 2×2 design) is too small to support "zero measurable protection" as a strong claim; needs replication before a supervisor meeting positions this as settled.
- The blocked-write anecdote in your own report (one blocked write at Q4_0 wouldn't have triggered anyway) is a good qualitative observation but isn't yet a quantified "block decisions are uncorrelated with outcomes" statistic — computing an actual correlation/contingency table from the 20 trials would strengthen this considerably and is cheap to do with existing data.

---

## Title 5 — AGENT-SHIELD (Closing Roadmap, No Standalone Demo)

Per your source files, this is explicitly a positioning slide rather than a demo, so no independent research-question/result/novelty analysis applies. The three benchmark-design precedents you cite all check out:

- **Agent Security Bench (ASB):** Zhang, Huang, Mei, Yao, Wang, Zhan, Wang, Zhang. ICLR 2025. https://arxiv.org/abs/2410.02644 — <cite index="60-1">benchmarks 10 prompt injection attacks, a memory poisoning attack, a novel Plan-of-Thought backdoor attack, 4 mixed attacks, and 11 corresponding defenses across 13 LLM backbones, with the highest average attack success rate of 84.30%</cite>. Confirmed real; a genuine "formalize and benchmark broadly" precedent, though its memory-poisoning coverage is one attack among many, not a quantization/small-model-focused deep dive.
- **DTA:** as above, https://arxiv.org/abs/2605.08442.
- **A Survey on Long-Term Memory Security in LLM Agents:** Lin, Hao, Fu, Cui, Chen, Li, Li, Xiong. 2026. https://arxiv.org/abs/2604.16548 — <cite index="68-1">proposes a Memory Lifecycle Framework organizing attacks, defenses, and cross-phase dependencies along six lifecycle phases (Write, Store, Retrieve, Execute, Share & Propagate, Forget & Rollback) and four security objectives (Integrity, Confidentiality, Availability, Governance)</cite>. This is a genuinely useful structural map for positioning AGENT-SHIELD's four axes (quantization, model scale, failure taxonomy, defenses) within a broader lifecycle view — worth citing directly in the roadmap slide, and worth checking its Table 3 (VMG primitives / threat mapping) before finalizing, since it may already sketch a superset of what AGENT-SHIELD proposes to formalize.

---

## Title 6 — Confound Audit (Same Data as Title 1, Reframed)

Because Title 6 uses identical data to Title 1, its literature grounding is identical (see Title 1 above) — the difference is entirely narrative framing (reproducibility/methodology critique of DTA's own scope-limitations statement, rather than a new vulnerability claim). One addition specific to this framing:

**Paper:** A Survey on Long-Term Memory Security in LLM Agents
**URL:** https://arxiv.org/abs/2604.16548

This survey's related-work section cites <cite index="72-1">"Poison once, exploit forever: environment-injected memory poisoning attacks on web agents" (arXiv:2604.02623)</cite> and references the well-known **PoisonedRAG** line of work (Zou et al., knowledge corruption attacks to RAG, USENIX Security) as foundational RAG-poisoning citations. Neither was independently verified in full this session, but both are worth a direct check before finalizing Title 6, since PoisonedRAG in particular is a very widely cited foundational paper in this space and any methodology/reproducibility critique framing should position itself relative to it, not just to DTA.

**Novelty confidence for Title 6: MEDIUM**, same basis as Title 1 — the reframing doesn't change the underlying evidence base, only the narrative, so the confidence rating tracks Title 1's.

---

## Final Cross-Title Analysis

### A. Strongest Novelty Candidates (strongest → weakest)

1. **Title 4 (defense × precision)** — the narrowest, most specific empty cell found across every comparable paper checked. Weakness is entirely about sample size (N=5/condition), not about a competing paper.
2. **Title 1 / Title 6 (precision × retrieval/trigger)** — DTA's own limitations paragraph names this exact gap and doesn't fill it; strong textual evidence of an open question, tempered by a dense surrounding literature on quantization-and-safety generally (just not on *this* mechanism).
3. **Title 3 (failure taxonomy)** — genuine synthesis of two separate lineages (jailbreak-response taxonomies, agent-security taxonomies) onto a memory-write-lifecycle axis neither covers, but weakened by zero human-verified labels and 3 of 7 categories unobserved.
4. **Title 2 (small-model family sweep)** — was tracking MEDIUM until this review surfaced a one-week-old, extremely closely adjacent paper (GhostWriter) using the same general setup (Ollama, local quantized Llama, memory poisoning). Still likely differentiable on "systematic multi-model 1–4B sweep" grounds, but this is now the title most in need of a direct limitations-section check before anyone states a novelty claim out loud.

### B. Closest Competing Papers (biggest risk, by title)

- **Titles 1, 2, 4 (biggest single risk overall): GhostWriter** (arXiv:2607.06595) — same general local-Ollama-quantized-model memory-poisoning setup, published the week before this review, with its own LLM-judge-based defense. Its Section 8 (Limitations & Future Work) has not yet been read and is the highest-priority action item in this entire report.
- **Titles 1, 4, 6: DTA** (arXiv:2605.08442) — closest on defense-failure mechanism and the specific "may differ from full-precision or API-served versions" limitations line that Title 1/6 directly targets.
- **Title 2: LM-SHIELD '26** (arXiv:2602.22242) — closest on "small-model family, not size, drives vulnerability" framing, but for jailbreak rather than memory poisoning.
- **Title 3: the Sybil RAG failure-mode benchmark** (arXiv:2607.03739) and the memory-lifecycle survey's **Table 3** (arXiv:2604.16548) — both close enough on taxonomy structure to warrant a direct side-by-side check before finalizing category definitions.

### C. Recommended Research Positioning (per title, for a supervisor conversation)

- **Title 1/6:** "DTA's own scope-limitations paragraph flags that its results may not hold at full precision or API-served precision. We ran a small, direction-validating check (N=10/condition, one model family) and found the gap DTA names is real and roughly 2x — but it looks threshold-like rather than linear, which is itself a new observation worth a larger follow-up before we claim more."
- **Title 2:** "We find that within the 1–4B range, model family predicts memory-poisoning vulnerability better than parameter count. This week, an independent paper (GhostWriter) published a closely related local-model memory-poisoning study; we need to confirm our multi-model sweep design is differentiated from their single-model approach before presenting this as a gap, which we believe it is but haven't fully confirmed against their stated limitations."
- **Title 3:** "We propose a 7-category memory-write-lifecycle taxonomy synthesizing ideas from jailbreak-response categorization and general agent-security taxonomies, applied to a domain (persistent memory writes) neither directly covers. Our first pass is unverified by human raters and surfaced only 4 of 7 categories — positioned as a scaffold for a follow-up study, not a finished taxonomy."
- **Title 4:** "Existing work shows LLM-judge defenses fail against memory poisoning because they can't distinguish compliance-framed poison from legitimate content. We show, in a small pilot, that this failure is precision-invariant — the judge blocks more often at higher precision without blocking more effectively. This is a sharper, more specific claim than 'the defense doesn't work,' though it needs a larger N before it's presentation-ready."
- **Title 5:** Position as a roadmap slide only, explicitly citing ASB, DTA, and the memory-lifecycle survey as the benchmark-design lineage AGENT-SHIELD would sit within — not a novelty claim in itself.

### D. Recommended Next Experiments (minimum additions per title)

1. **Before anything else:** read GhostWriter's Limitations & Future Work section (arXiv:2607.06595, Section 8) in full. This affects Titles 1, 2, and 4 simultaneously and is the single highest-value next step.
2. **Title 1/6:** replicate the precision sweep on a second model family (e.g., Qwen or Phi) to test whether the "threshold not slope" pattern is Llama-specific.
3. **Title 2:** fix the Phi-3 harness bug and re-run those 5 trials; consider adding a second local family pair (e.g., two 3B-class models) to strengthen the "family over size" claim beyond two 1B models.
4. **Title 3:** get `manual_tag` filled in for at least the heuristic's self-flagged borderline cases; run a second attack scenario/trigger phrase to test whether the 4-of-7-categories pattern replicates.
5. **Title 4:** expand beyond N=5; compute an explicit correlation/contingency statistic between judge-block decisions and ground-truth attack success (cheap, uses existing data) rather than relying on the single anecdote currently in the report.
6. **All titles:** run the remaining adversarial query variants from the original brief that weren't covered this session — in particular exact-phrase searches like "retrieval poisoning" + "INT4 INT8 FP16" and "memory poisoning" + "failure taxonomy" run against ACL Anthology and USENIX Security directly (this review leaned on arXiv/general web search; venue-specific search wasn't separately run).
