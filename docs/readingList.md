# Reading List — Quantization × RAG/Memory Poisoning

Goal of this list: build the intuition Dr. Kasyap is asking for, in order. Each tier depends on
the one before it — read root cause first, then quantization-specific evidence, then the
attack/defense landscape. Don't jump straight to Tier 4 (attacks) or you'll be doing empirical
work again without the mechanism underneath it.

Check items off as you go.

---

## Tier 0 — Root cause (read this first, before anything quantization-specific)

- [ ] **Qi, Panda, Lyu, Ma, Roy, Beirami, Mittal, Henderson — "Safety Alignment Should Be Made
  More Than Just a Few Tokens Deep"** (ICLR 2025 Outstanding Paper) — arXiv:2406.05946
  **Why:** Safety alignment mostly reshapes the probability distribution over only the *first
  few output tokens* — it's a thin shortcut, not a deep distributed property of the network.
  This is why alignment is so cheap to knock out (fine-tuning, adversarial suffixes, prefilling,
  decoding-parameter changes). Once you've internalized this, "quantization erodes alignment"
  stops being a surprising empirical finding and becomes an obvious prediction. Read everything
  else through this lens.

---

## Tier 1 — Quantization breaking discrimination (Mechanism 1 evidence)

- [ ] **Kharinaev, Moskvoretskii, Shvetsov, Studenikina, Bykov, Burnaev — "Investigating the
  Impact of Quantization Methods on the Safety and Reliability of Large Language Models"**
  — arXiv:2502.15799
  **Why:** The paper that coined "alignment degradation" for quantization specifically —
  66 quantized model variants across 4 safety benchmarks, found both PTQ and QAT can degrade
  alignment. Your single most citable anchor for Mechanism 1.

- [ ] **"Alignment-Aware Quantization for LLM Safety" (CAQ)** — arXiv:2511.07842
  **Why:** Names the actual root cause — standard PTQ minimizes reconstruction error without
  accounting for behavioral alignment, so a model can keep low perplexity while safety
  degrades. Read for the mechanism section, not the fix (CAQ itself).

- [ ] **"The Joint Effect of Quantization and Sampling Temperature on LLM Safety Alignment: A
  Factorial Analysis"** — arXiv:2606.29581
  **Why:** Recent, and worth reading as a *methodology template* — they run a factorial design
  across quantization × temperature on safety outcomes. Structurally identical to what you're
  doing (scale × precision on poisoning outcomes). Steal their experimental design discipline.

- [ ] **"Preserving Fairness and Safety in Quantized LLMs Through Critical Weight Protection"**
  — arXiv:2601.12033
  **Why:** Good lit-review material — summarizes the genuinely mixed findings across PTQ vs
  QAT vs quantization method, so you don't overclaim a clean monotonic story to Dr. Kasyap.

---

## Tier 2 — Quantization breaking execution (Mechanism 2, pulling the opposite way)

- [ ] **Zhang et al. — "Imperceptible Content Poisoning in LLM-Powered Applications"**
  (ASE 2024)
  **Why:** Found quantization can cause LLMs to generate irrelevant responses, and that content
  poisoning specifically requires correlating a trigger with target content — a capability
  itself diminished by quantization. This is the paper that stops your story from being
  one-directional. Read right after Tier 1 so the tension between the two mechanisms is
  obvious before you design experiments around it.

---

## Tier 3 — The redundancy analogy (different lever, same intuition)

- [ ] **Peng, Wu, Chen — "Swallowing the Poison Pills: Insights from Vulnerability Disparity
  Among LLMs"** — arXiv:2502.18518
  **Why:** Argues disproportionate poisoning vulnerability may come from reduced parameter
  redundancy — pruned/distilled models need ~30% fewer poison samples for equivalent damage.
  This is about pruning/distillation, **not** quantization — read for the logic, not as a
  citation that already proves your point. Whether "fewer redundant weight paths" transfers
  from "weights removed" to "weights represented at lower precision" is an open question
  worth a paragraph in your own paper, not an assumption.

---

## Tier 4 — Attack foundations (so your baseline isn't reinventing wheels)

- [ ] **Zou, Geng, Wang, Jia — "PoisonedRAG: Knowledge Corruption Attacks to
  Retrieval-Augmented Generation of Large Language Models"** (USENIX Security 2025) —
  arXiv:2402.07867
  **Why:** The foundational knowledge-corruption attack on RAG — the starting point almost
  everything else cites.

- [ ] **Chen, Xiang, Xiao, Song, Li — "AgentPoison: Red-teaming LLM Agents via Poisoning
  Memory or Knowledge Bases"** (NeurIPS 2024) — arXiv:2407.12784
  **Why:** Closest prior "memory poisoning" framing to yours — backdoors an agent's long-term
  memory via optimized triggers. Also demonstrates that a defense based on isolating and
  aggregating individual retrievals fails once all retrieved instances are poisoned — useful
  context for why naive defenses aren't enough.

- [ ] **Zhang, Chen, Liu, Nie, Li, Liu, Fang — "Practical Poisoning Attacks against
  Retrieval-Augmented Generation" (CorruptRAG)** — arXiv:2504.03957
  **Why:** Single-poison-text attack — your most realistic attack baseline to reproduce first
  on your own harness.

---

## Tier 5 — Defenses worth knowing before designing your own

- [ ] **Zhang, Xin, Fang, Liu, Yi, Li, Liu — "Traceback of Poisoning Attacks to
  Retrieval-Augmented Generation" (RAGForensics)** (WWW '25) — arXiv:2504.21668
  **Why:** First traceback/forensics system for RAG poisoning — this is the "trace-back"
  instinct from the meeting; it already exists, cite it precisely.

- [ ] **Zhang, Xin, Chen et al. (incl. Fang) — "Who Taught the Lie? Responsibility
  Attribution for Poisoned Knowledge in Retrieval-Augmented Generation"** (IEEE S&P 2026) —
  arXiv:2509.13772
  **Why:** Direct follow-on to RAGForensics — read to see where that line of work is headed.

- [ ] **Tan, Luan, Luo, Sun, Chen, Dai — "RevPRAG: Revealing Poisoning Attacks in
  Retrieval-Augmented Generation through LLM Activation Analysis"** (EMNLP Findings 2025) —
  arXiv:2411.18948
  **Why:** Most mechanistically useful defense paper for you — detects poisoning via LLM
  activation patterns, 98% TPR / ~1% FPR. Gives you a ready-made separability metric you can
  re-run at each of your precision levels (see the experiments doc).

- [ ] **Tsai, Bagdasarian — "Context is Key for Agent Security" (Conseca)** (HotOS '25) —
  arXiv:2501.17070
  **Why:** Contextual-integrity-based, deterministic security policies for agents — structurally
  immune to prompt injection because it doesn't rely on the model judging itself. Your
  theoretical backbone for a defense that targets discrimination collapse specifically.

---

## Tier 6 — Reread your own anchors with this lens

- [ ] **Dr. Kasyap — LM-SHIELD '26** — arXiv:2602.22242
  Reread specifically checking whether reported "vulnerability" numbers show any split-direction
  signature (some categories up, some down) even though the paper didn't frame it that way.

- [ ] **Leong et al. — the ≥9B-parameter benchmark** — arXiv:2605.08442
  Same exercise — look for hints of the mechanism split in their reported numbers.

---

## Tier 7 — Closest competing/adjacent work (must-read before writing anything down)

- [ ] **Srivastava, He — "MemoryGraft: Persistent Compromise of LLM Agents via Poisoned
  Experience Retrieval"** — arXiv:2512.16962 (Dec 2025)
  **Why:** Closest existing paper to "persistent memory poisoning" as a headline. Read in full,
  not the abstract — you need a clean two-sentence distinction ready for the next meeting.

- [ ] **"Exploiting LLM Quantization"** — arXiv:2405.18137
  **Why:** Different threat model — attacker poisons a full-precision model so malice activates
  only once *someone else* quantizes it (supply-chain attack). Inverse of your question. Cite
  and distinguish, don't confuse the two in your related work.

- [ ] **LLMQuA — Practical Backdoor Injection on LLM Quantization** (ACM Web Conference 2026)
  **Why:** Same family as above — quantization as the backdoor *trigger*, not as a factor
  affecting susceptibility to inference-time content poisoning. Cite and distinguish.

---

## Suggested pace

Tier 0 + Tier 1 + Tier 2 in one sitting — that's the actual "why" argument, everything else is
support. Tier 7 before your next meeting with Dr. Kasyap, no exceptions. Tiers 3–6 can be spread
out alongside building the experiments.
