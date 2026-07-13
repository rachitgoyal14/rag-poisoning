# Persistent Memory Poisoning in Agentic RAG — Title Candidates & Pre-Meeting Demo Plan

**Prepared for:** Meeting with Dr. Harsh Kasyap, ~July 14, 2026
**Direction locked in:** Persistent/cross-session agentic memory poisoning (the direction from the "Research Direction Proposal" doc), evaluated fully locally on quantized 1B–8B models.
**Scope of this document:** (1) a fresh literature check on every attack/benchmark referenced in the proposal, done tonight so numbers and gap claims are current; (2) six candidate paper titles, each grounded in a specific, still-open gap; (3) under each title, a concrete demo you can actually build before the meeting, with no code — just the pipeline, scenario, metrics, and table to fill in.

A note before the titles: the field around *general* agentic memory poisoning has gotten even more crowded since the original proposal was drafted — there is now a full survey paper on long-term memory security in LLM agents (arXiv:2604.16548) plus a wave of narrowly-scoped attacks (InjecMEM, MemMorph, Trojan Hippo, Superlocalmemory, DrunkAgent, Sleeper Memory Poisoning, Zombie Agents). That makes the *general* "we poisoned an agent's memory" claim essentially unpublishable on its own. The two lanes that survive scrutiny — **quantization as an untested variable**, and **sub-9B local models as an untested population** — are narrower than the original proposal assumed, but they are real, and tonight's search confirms exactly why.

---

## 1. Literature Landscape Check (verified tonight)

### 1.1 Core attacks — all confirmed, citations corrected/completed

| Work | Confirmed citation | What it actually does |
|---|---|---|
| MINJA | Dong et al., NeurIPS 2025, arXiv:2503.03704 | Query-only injection into agent memory banks via bridging steps + indication prompt + progressive shortening. >95% injection success rate reported. |
| AgentPoison | NeurIPS 2024 | Backdoors RAG/memory knowledge bases via an optimized trigger mapped to a malicious key-value pair; evaluated on driving/healthcare agents. |
| MemoryGraft | Srivastava & He, arXiv:2512.16962 (Dec 2025) | Trigger-free injection of fake "successful experiences" via benign-looking ingested artifacts (e.g. README files); exploits an agent's semantic-imitation heuristic; validated on MetaGPT's DataInterpreter with GPT-4o. |
| Sleeper Memory Poisoning | Pulipaka et al., arXiv:2605.15338 | "Hidden in Memory" — plant/persist/trigger sleeper-style attack on LLM agents. |
| Zombie Agents | Yang, He, Ji, Hooi & Dong, arXiv:2602.15654 (2026) | Self-reinforcing injections that give persistent control over self-evolving agents; two-phase infection → trigger model. |
| Delayed Trigger Attack (DTA) benchmark | Leong, arXiv:2605.08442 | The actual comprehensive defense benchmark the proposal refers to. |

### 1.2 What the DTA benchmark really covers (this matters a lot for your Gap 1 and Gap 2 claims)

I pulled the actual experimental design (paper + public repo). It is more informative than the proposal doc assumed:

- **9 models, all ≥ 9B parameters:** `qwen2.5:14b`, `qwen3.5:9b`, `qwen3:32b`, `qwen2.5:72b`, `qwen3.5:122b`, `qwq:32b`, `glm-4.7-flash:q8_0`, `gpt-oss:20b`, `gpt-oss-safeguard:120b`. Nothing below 9B is tested.
- **Quantization is fixed, not varied:** every Ollama model in the factorial runs at **q4_0 only**. The paper's own scope-limitations section says results "may differ from full-precision or API-served versions" — i.e., they flag this as an open question rather than answer it.
- **6 defenses + no-defense baseline, 5,040 runs total.** Six of seven conditions failed to meaningfully reduce attack success rate against delayed-trigger attacks.

This is good news for your framing: it independently confirms, in the most rigorous existing benchmark, that (a) quantization level is never treated as an independent variable, and (b) the entire small-model band (1B–8B) that your hardware constraint pushes you toward is genuinely untested. That's a sharper and more defensible version of "Gap 1" and "Gap 2" than the original proposal draft had, because now you have a specific paper and a specific model list to point to instead of a general claim.

### 1.3 Adjacent literature you must explicitly distinguish from (reviewers will ask)

Quantization-and-safety is **not** a novel intersection in general — it's well studied for single-turn jailbreak/adversarial-prompt attacks:

- Kumar et al. (2024) — fine-tuning + quantization reduce jailbreak resilience (cited repeatedly as the seminal result here).
- Egashira et al., "Exploiting LLM Quantization," arXiv:2405.18137 — an attacker-crafted full-precision model that behaves benignly until quantized (a *quantization-conditioned* attack, i.e. the attacker controls the base weights — different threat model from yours).
- "Widening the Gap: Exploiting LLM Quantization via Outlier Injection," arXiv:2605.15152 (May 2026) — a newer, stronger version of the same quantization-conditioned attack family (AWQ/GPTQ/GGUF).
- HarmLevelBench (arXiv:2411.06835), AQUA-LLM (arXiv:2509.13514), "Stochastic Monkeys" (arXiv:2411.02785), and a Llama3-8B-specific quantization-jailbreak study all measure how *quantization level* changes *jailbreak/adversarial-prompt* success — none touch persistent memory.

**Your novelty argument, stated precisely:** quantization's effect on *single-turn adversarial-prompt* vulnerability is established; quantization's effect on *persistent, cross-session memory-poisoning* vulnerability is not — and the one benchmark large enough to have settled it (DTA) explicitly fixed quantization as a constant rather than a variable. That sentence is worth putting in the email to Dr. Kasyap almost verbatim.

---

## 2. Candidate Titles + What to Demo Tonight

Each title below is buildable on the M5 MacBook (Ollama + a lightweight memory layer + Chroma + sentence-transformers). Demos are ordered by how directly they map to tomorrow's meeting decision, not by how "impressive" they are — a rough, honest 10-trial table beats a broken ambitious pipeline.

---

### Title 1 (recommended primary) — *"Does Precision Matter, Again? Quantization-Dependent Susceptibility to Persistent Memory Poisoning in Local LLM Agents"*

**Maps to:** Direction 1 in the proposal, sharpened with tonight's DTA finding.
**Research question:** Holding the model family fixed, does injection / retrieval / trigger success change as the same model moves across quantization levels?

**Demo to build tonight:**
1. Pick **one** small model available in multiple Ollama quantization tags — e.g. `llama3.2:3b-instruct` (pull `q4_0`, `q8_0`, and the `fp16`/unquantized tag) or `qwen3:4b`. Confirm all three pull and run within your 24GB budget (a 3–4B model at fp16 is ~6–8GB, comfortable).
2. Stand up a minimal memory-augmented agent: mem0 (fastest) or a hand-rolled Chroma collection + sentence-transformers embedder, wired to the Ollama model as the reasoning backend.
3. Implement **one** MINJA-style query-only injection scenario: a benign-looking multi-turn conversation that plants a malicious "record" in memory (reuse MINJA's bridging-step idea — connect a benign query to a target victim term through intermediate steps), then a later, unrelated benign query containing the trigger term.
4. Run **N = 8–10 trials per precision level** (small N is fine for a direction-validation demo — say so explicitly at the meeting).
5. Log three numbers per trial, matching the field's standard metrics: **Injection Success** (was the malicious record actually written to the store), **Retrieval Rate** (was it retrieved when the trigger query ran), **Trigger Success** (did the agent's final output reflect the malicious content).
6. Produce one table + one bar chart (precision on x-axis, the three rates on y-axis).

**Table to bring:**

| Precision | Injection Success (n/10) | Retrieval Rate (n/10) | Trigger Success (n/10) |
|---|---|---|---|
| Q4_0 | | | |
| Q8_0 | | | |
| FP16 | | | |

**Why this is the strongest opener:** it's the cheapest possible experiment that directly answers the question the whole roadmap is staged around, and even a null result ("no difference across precision") is a publishable, honest finding you can say out loud tomorrow.

**Supporting reading (bring these to the meeting):**
- Leong, J. W. "Defense Effectiveness Across Architectural Layers…" (DTA benchmark), arXiv:2605.08442 — this is your smoking gun. Read the model list and the "may differ from full-precision or API-served versions" scope-limitations line yourself so you can quote it precisely.
- Dong et al., "A Practical Memory Injection Attack against LLM Agents" (MINJA), arXiv:2503.03704 — the attack design your demo adapts (bridging steps, indication prompt, progressive shortening). Read this closely, not just the abstract.
- Kumar et al. (2024) — the seminal result that fine-tuning and quantization reduce jailbreak resilience; the paper you're extending into a new attack class. (Cited in full in HarmLevelBench, arXiv:2411.06835, and AQUA-LLM, arXiv:2509.13514, if you can't locate the original directly.)
- Egashira et al., "Exploiting LLM Quantization," arXiv:2405.18137, and "Widening the Gap: Exploiting LLM Quantization via Outlier Injection," arXiv:2605.15152 — read these to pre-empt the "isn't this just quantization-conditioned attacks?" question. The answer is no (there the attacker controls the base weights; in your setting they don't), but you should be able to say that in one sentence without hesitating.
- AQUA-LLM, arXiv:2509.13514 — closest existing paper to your Q4/Q8/FP16 comparison framing; useful as a template for how to present the trade-off table.

---

### Title 2 — *"Small Agents, Same Sleepers? Parameter-Scale Effects on Delayed-Trigger Memory Poisoning Below the 8B Threshold"*

**Maps to:** Direction 3.
**Research question:** DTA's smallest tested model is 9B. Does the same delayed-trigger attack behave differently once you drop into the 1B–8B band nobody has benchmarked?

**Demo to build tonight (secondary, if Title 1's demo finishes with time to spare):**
1. Reuse the exact pipeline and attack scenario from Title 1.
2. Instead of varying precision, hold quantization constant (pick one, e.g. q4_0 to stay comparable to DTA) and vary the **model**: 3–4 small models across families — e.g. `llama3.2:1b`, `qwen3:1.7b`, `gemma3:1b`, `phi3:3.8b`.
3. Run a smaller trial count per model (N = 5 is enough for a direction-validation slide) and log the same three metrics.
4. Produce a simple grouped bar chart: model on x-axis, the three rates on y-axis.

**Table to bring:**

| Model | Params | Injection Success | Retrieval Rate | Trigger Success |
|---|---|---|---|---|
| Llama 3.2 | 1B | | | |
| Qwen3 | 1.7B | | | |
| Gemma 3 | 1B | | | |
| Phi-3 | 3.8B | | | |

**Framing note:** pitch this explicitly as "extending the DTA model roster downward," not as a standalone claim — that keeps the novelty tight and citable.

**Supporting reading (bring these to the meeting):**
- LM-SHIELD '26, arXiv:2602.22242 — Dr. Kasyap's own precedent for benchmarking small open models on jailbreak robustness. Read this first; it's the direct methodological ancestor of this title, and he'll expect you to have it cold.
- Leong (DTA), arXiv:2605.08442 — again, for the exact model floor (9B) you're pushing below.
- "Small but Dangerous: Evaluating and Mitigating Jailbreak Vulnerabilities in Small Language Models" (Springer, 2026) — directly parallel work in the jailbreak (not memory-poisoning) space; good for framing language and related-work positioning.
- Howe et al. (2024) and Ren et al. (2024) on model size vs. jailbreak safety — summarized well in "Stochastic Monkeys at Play," arXiv:2411.02785 (§A.5) if you can't find the originals. The finding is "larger tends to be safer but non-monotonically" — useful context since your own small-N demo may come back mixed rather than clean.
- "Systematic Scaling Analysis of Jailbreak Attacks in Large Language Models," arXiv:2603.11149 — a recent, clean example of presenting a model-scale result; useful as a formatting template even though its attack type differs from yours.

---

### Title 3 — *"Silent Sleepers: A Failure-Mode Taxonomy for Persistent Memory Poisoning in Small, Local LLM Agents"*

**Maps to:** Direction 5 — and directly mirrors the "silent non-responsiveness" framing from LM-SHIELD, which is the strongest continuity argument you can make to Dr. Kasyap.
**Research question:** Instead of binary success/fail, how do small local agents actually fail when you try to poison their memory?

**Demo to build tonight (cheapest add-on, high narrative payoff):**
1. No new infrastructure needed — this reuses the trial logs from Title 1's demo.
2. Hand-tag each of the ~24–30 trials into a small taxonomy instead of just pass/fail. A reasonable starting set, adapted from what MINJA/DTA/MemoryGraft implicitly distinguish but never name as categories:
   - Memory written faithfully (clean injection)
   - Memory written but corrupted/truncated
   - Memory write silently dropped (no error, no record — the "silent non-responsiveness" analogue)
   - Write refused (agent flags or declines)
   - Retrieved but ignored at generation time
   - Retrieved and reflected only partially
   - Hallucinated memory (content not actually present in the store, but the model claims it)
3. Produce one small frequency table + one sentence per category with a real example transcript snippet from tonight's trials.

**Table to bring:**

| Failure mode | Count (of ~30 trials) | Example |
|---|---|---|
| Faithful write | | |
| Corrupted write | | |
| Silent drop | | |
| Write refused | | |
| Retrieved, ignored | | |
| Retrieved, partial | | |
| Hallucinated | | |

**Why this matters for tomorrow:** this is the piece that most closely matches Dr. Kasyap's established style (empirical + taxonomy, per LM-SHIELD), and it costs you almost nothing extra since it's just re-analysis of Title 1's logs.

**Supporting reading (bring these to the meeting):**
- LM-SHIELD '26, arXiv:2602.22242 — non-negotiable read. This is the paper you're explicitly extending "silent non-responsiveness" from into the memory-poisoning setting; know its exact taxonomy before the meeting.
- RAS-Eval, arXiv:2506.15253 — a hierarchical failure-mode taxonomy for agent security (six atomic failure modes plus compound manifestations). The closest existing methodological template for what you'd build tonight.
- Microsoft, "Taxonomy of Failure Mode in Agentic AI Systems" (whitepaper) and its June 2026 update "Updating the Taxonomy of Failure Modes in Agentic AI Systems" (Microsoft Security Blog) — Microsoft's taxonomy includes an actual memory-poisoning case study on an email assistant. Read this before the meeting; it's the most directly comparable existing taxonomy, and you'll want a clear answer for how yours differs (yours: empirical/per-model/quantitative; theirs: qualitative/red-team-derived).
- "Navigating the Risks: A Survey of Security, Privacy, and Ethics Threats in LLM-Based Agents," arXiv:2411.09523 — a source-based (input/model/combined) taxonomy of agent threats; a useful contrast to the outcome-based taxonomy you're proposing.
- Aegis, arXiv:2508.19504 — not a security paper, but a clean example of turning failure analysis (six failure modes from real agent traces) into a structured contribution; good as a "how to write this section" model.

---

### Title 4 — *"Forget Me Not, Even Compressed: Do Memory-Sanitization Defenses Degrade Under Quantization in Local LLM Agents?"*

**Maps to:** Direction 4.
**Research question:** DTA showed 6 of 7 defenses fail against delayed-trigger attacks at a single fixed quantization level. Does the one defense that *does* work hold up if the model doing the defending is itself quantized differently?

**Demo to build tonight:** mark this as **stretch / partial only** — it's a real next step, not a one-night build.
1. If time remains after Title 1: add a single lightweight defense on top of the same pipeline — e.g. an "LLM-judge" pass where the small model itself is asked to flag a candidate memory write as suspicious before it's committed.
2. Run it at just two precision levels (Q4_0 vs FP16) with a handful of trials (N = 5).
3. Present this at the meeting explicitly as "in progress / proof-of-concept," not a finished comparison — overclaiming a rushed defense result is the one thing to avoid here.

**Table to bring (partial, marked as preliminary):**

| Precision | ASR without defense | ASR with judge defense |
|---|---|---|
| Q4_0 | | |
| FP16 | | |

**Supporting reading (bring these to the meeting):**
- Leong (DTA), arXiv:2605.08442 — the "6 of 7 defenses fail" result you're building on. Read the actual defense implementations (Minimizer, Sanitizer, RAG Sanitizer, RAG LLM Judge, Prompt Hardening, Memory Sandbox) since your one-night demo defense is a simplified version of one of these.
- "Memory Poisoning Attack and Defense on Memory Based LLM-Agents," arXiv:2601.05504 — EHR-agent-specific defense evaluation; a useful second data point on which defenses hold up outside DTA's setting.
- "Fine-Tuning, Quantization, and LLMs: Navigating Unintended Outcomes," arXiv:2404.04392 — directly evaluates guardrail effectiveness under quantization, for jailbreaks rather than memory poisoning. The closest existing precedent for "does a defense degrade under compression," and the paper to cite as your direct predecessor.
- AQUA-LLM, arXiv:2509.13514 — again useful here, applying the accuracy/quantization/robustness trade-off framing to a defense mechanism rather than the base attack.

---

### Title 5 — *"AGENT-SHIELD: Benchmarking Persistent Memory Poisoning Across Model Scale, Quantization, and Defenses in Fully Local Agentic RAG"*

**Maps to:** Direction 2 — the eventual combined paper, not a one-night target.
**No standalone demo tonight.** Instead, bring a single roadmap slide/diagram showing how tonight's Title 1 pipeline is the minimal slice that the full AGENT-SHIELD factorial (models × quantization × attacks × defenses) scales up from — this is the "long-term destination" framing to close the meeting with, once Direction 1 is validated as the entry point.

**Supporting reading (bring these to the meeting):**
- LM-SHIELD '26, arXiv:2602.22242 — the direct template for scope, dataset-release philosophy, and taxonomy style this paper would follow.
- Agent Security Bench (ASB), arXiv:2410.02644 — the benchmark-design precedent (27 attack/defense combinations × 13 backbones × 7 metrics) for how to structure a large factorial agent-security benchmark.
- Leong (DTA), arXiv:2605.08442 — the immediate predecessor benchmark AGENT-SHIELD would extend, by adding quantization level and sub-9B models as new factorial dimensions.
- "A Survey on Long-Term Memory Security in LLM Agents," arXiv:2604.16548 — read this in full before committing to AGENT-SHIELD's scope. It's the most current map of the whole landscape and will show you exactly which attack/defense combinations other papers have already "claimed."

---

### Title 6 (alternate framing of Title 1, worth having in your back pocket) — *"Compression and Compromise: Quantization as an Uncontrolled Confound in Agentic Memory-Poisoning Benchmarks"*

**Maps to:** same underlying experiment as Title 1, different rhetorical framing.
**Positioning:** rather than "we found a new vulnerability," this frames the contribution as a **methodological critique** — every existing local-model benchmark (DTA, and by extension anything built on Ollama defaults) has silently fixed quantization at whatever the default pull tag happens to be, meaning published attack-success numbers may not generalize across deployment configurations. This is a different kind of publishable contribution (methodology/reproducibility) than a vulnerability paper, and it's worth floating to Dr. Kasyap as an alternative angle on the identical Title 1 demo, in case he prefers that framing.

**Demo:** identical to Title 1 — same pipeline, same table, just narrate it as a "confound audit" instead of a "vulnerability study" if you use this framing.

**Supporting reading (bring these to the meeting):**
- Same core set as Title 1 — DTA (arXiv:2605.08442), Egashira et al. (arXiv:2405.18137), "Widening the Gap" (arXiv:2605.15152), AQUA-LLM (arXiv:2509.13514). The demo is identical, so the reading list is identical; only the order you lead with changes.
- For this framing, open with DTA's own scope-limitations paragraph — the "may differ from full-precision or API-served versions" line — as your primary evidence. The whole pitch is "a benchmark's own footnote, turned into a research question," so that sentence needs to be quoted precisely, not paraphrased from memory.
- Optional: skim one general reference on uncontrolled variables / hidden confounds in ML benchmark reporting if you want extra methodological backing — not essential, since DTA's own text already carries the argument.

---

## 3. Recommendation for Tomorrow

1. **Lead with Title 1's demo.** It's the cheapest, most directly answers the roadmap's Phase 1 question, and a null result is still a result.
2. **Bring Title 3's taxonomy table as a five-minute add-on.** It costs almost nothing beyond Title 1 and is the piece most likely to resonate with Dr. Kasyap given LM-SHIELD's style.
3. **Mention Title 2 and Title 6 as framing options**, not finished work — useful for the "which title should we commit to" discussion.
4. **Show Title 4 only if it actually runs.** Don't force it; a broken defense demo is worse than no defense demo.
5. **Use Title 5 as the closing slide** — it's the destination, not tonight's output, and it answers his "Overall Positioning" discussion point directly.

## 4. Honest Caveats to State Out Loud at the Meeting

- Tonight's trial counts (N = 5–10 per condition) are for direction validation only — not statistically powered, and you should say so before he asks.
- Single model family, single attack scenario, single trigger design — the real study needs the full 1B–8B roster and ideally more than one attack type (MINJA-style query-only vs. MemoryGraft-style ingestion-based).
- The taxonomy in Title 3 is a first draft from ~24–30 trials — treat it as a seed list to refine once Aditya's literature sweep on failure-mode language across the newer papers (InjecMEM, Trojan Hippo, DrunkAgent) is done, since some of those may already name categories worth reusing or citing against.

## 5. Reference List (verified tonight, with arXiv IDs)

- Dong, S. et al. "A Practical Memory Injection Attack against LLM Agents" (MINJA). NeurIPS 2025. arXiv:2503.03704.
- Chen, A. et al. "AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases." NeurIPS 2024.
- Srivastava, S. S. & He, H. "MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval." arXiv:2512.16962 (Dec 2025).
- Pulipaka, S. et al. "Hidden in Memory: Sleeper Memory Poisoning in LLM Agents." arXiv:2605.15338.
- Yang, X., He, Y., Ji, S., Hooi, B. & Dong, J. S. "Zombie Agents: Persistent Control of Self-Evolving LLM Agents via Self-Reinforcing Injections." arXiv:2602.15654 (2026).
- Leong, J. W. "Defense Effectiveness Across Architectural Layers: A Mechanistic Evaluation of Persistent Memory Attacks on Stateful LLM Agents" (Delayed Trigger Attack benchmark). arXiv:2605.08442.
- Zhang, H. et al. "Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-Based Agents." ICLR 2025. arXiv:2410.02644.
- OWASP GenAI Security Project. "Top 10 for Agentic Applications 2026" — ASI06: Memory & Context Poisoning. Published Dec 9, 2025.
- Kumar, A. et al. (2024) — fine-tuning and quantization effects on jailbreak vulnerability (as cited in multiple 2025–26 surveys).
- Egashira, K. et al. "Exploiting LLM Quantization." arXiv:2405.18137.
- "Widening the Gap: Exploiting LLM Quantization via Outlier Injection." arXiv:2605.15152 (May 2026).
- "HarmLevelBench: Evaluating Harm-Level Compliance and the Impact of Quantization on Model Alignment." arXiv:2411.06835.
- "AQUA-LLM: Evaluating Accuracy, Quantization, and Adversarial Robustness Trade-offs in LLMs for Cybersecurity QA." arXiv:2509.13514.
- "Stochastic Monkeys at Play: Random Augmentations Cheaply Break LLM Safety Alignment." arXiv:2411.02785.
- Comprehensive survey: "A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses, and Governance Across the Memory Lifecycle." arXiv:2604.16548 — useful for Aditya's sweep; also evidence of how saturated the general space now is.
- LM-SHIELD '26 (Dr. Kasyap's prior work). arXiv:2602.22242.
- "Memory Poisoning Attack and Defense on Memory Based LLM-Agents." arXiv:2601.05504 — EHR-agent defense evaluation (Title 4 reading).
- "Fine-Tuning, Quantization, and LLMs: Navigating Unintended Outcomes." arXiv:2404.04392 — guardrail effectiveness under quantization (Title 4 reading).
- "Small but Dangerous: Evaluating and Mitigating Jailbreak Vulnerabilities in Small Language Models." Springer, 2026 (Title 2 reading).
- Howe et al. (2024) and Ren et al. (2024) on model size vs. jailbreak safety, as summarized in "Stochastic Monkeys at Play," arXiv:2411.02785, §A.5 (Title 2 reading).
- "Systematic Scaling Analysis of Jailbreak Attacks in Large Language Models." arXiv:2603.11149 (Title 2 reading).
- RAS-Eval: "A Comprehensive Benchmark for Security Evaluation of LLM Agents in Real-World Environments." arXiv:2506.15253 — hierarchical failure-mode taxonomy (Title 3 reading).
- Microsoft. "Taxonomy of Failure Mode in Agentic AI Systems" (whitepaper) and "Updating the Taxonomy of Failure Modes in Agentic AI Systems: What a Year of Red Teaming Taught Us" (Microsoft Security Blog, June 2026) — includes a memory-poisoning case study (Title 3 reading).
- "Navigating the Risks: A Survey of Security, Privacy, and Ethics Threats in LLM-Based Agents." arXiv:2411.09523 (Title 3 reading).
- Aegis: "Taxonomy and Optimizations for Overcoming Agent-Environment Failures in LLM Agents." arXiv:2508.19504 (Title 3 reading, structural template).
