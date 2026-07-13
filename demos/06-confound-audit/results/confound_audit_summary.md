# Title 6 -- Confound Audit Summary

**Framing:** identical evidence to Title 1. Every number below is pulled directly from Title 1's own results/ directory -- nothing was re-run. Only the narrative changes: this is not "we found a vulnerability," it is "a benchmark's own footnote, turned into a research question."

**Lead with this, quoted precisely (per plan.md, not paraphrased):** DTA's own scope-limitations section states its results "may differ from full-precision or API-served versions" -- i.e. the paper's own authors flag quantization as an open question rather than answer it. Every existing local-model benchmark built on Ollama defaults, DTA included, has silently fixed quantization at whatever the default pull tag happens to be, meaning published attack-success numbers may not generalize across deployment configurations.

| Quantization | Injection Success | Retrieval Rate | Trigger Success (ASR) |
|---|---|---|---|
|  | 1.00 | 0.50 | 0.50 |

---

Same reading list as Title 1: DTA (arXiv:2605.08442), Egashira et al. (arXiv:2405.18137), "Widening the Gap" (arXiv:2605.15152), AQUA-LLM (arXiv:2509.13514). Per plan.md, only the lead-in and framing order changes for this title.
