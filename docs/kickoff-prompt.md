# Kickoff Prompt for Implementing the Demos

**How to use this:** Start a new Claude chat, attach `agentic_memory_poisoning_titles_and_demo_plan.md` as context, then paste the prompt below as your first message. It forces the new chat to (1) propose a build plan and folder structure first, with no code, and (2) hand you exactly one file per turn after that, so you control token spend turn by turn.

---

## Folder structure (drop this in alongside your existing `docs/`)

```
project-root/
├── docs/                                   # already exists — your planning .md files live here
│   ├── research_direction_proposal.md
│   └── agentic_memory_poisoning_titles_and_demo_plan.md
│
├── demos/
│   ├── title1_precision_matters/           # build this first — everything else reuses it
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── config.py
│   │   ├── memory_store.py
│   │   ├── attack_scenario.py
│   │   ├── run_trials.py
│   │   ├── analyze_results.py
│   │   ├── data/
│   │   │   └── trigger_terms.json
│   │   └── results/                        # trial logs + CSV land here (gitignore this)
│   │
│   ├── title2_small_agents/                # mostly reuses title1_precision_matters/*
│   │   └── run_trials_small_models.py
│   │
│   ├── title3_taxonomy/                    # pure re-analysis, no new pipeline
│   │   └── tag_failure_modes.py
│   │
│   └── title4_defense_quant/               # stretch — only build if time allows
│       └── judge_defense.py
│
├── .gitignore
└── ollama_setup.md                         # which model tags to pull, sizes, one-time notes
```

---

## The prompt (copy everything in the box below into the new chat)

```
You are helping me implement the demos described in the attached document
(agentic_memory_poisoning_titles_and_demo_plan.md). This is academic AI-security
research: I'm a research intern building a local, sandboxed red-teaming harness
that poisons the memory of my own local LLM agent — running entirely on my own
machine, no third-party systems involved — to reproduce and extend methodology
from published papers cited in the doc (MINJA, MemoryGraft, the DTA benchmark,
etc.), ahead of a research meeting with my faculty advisor.

ENVIRONMENT
- MacBook Pro, Apple M5, 24GB unified memory, macOS
- Python 3.11
- Ollama for local model serving (models pulled as quantization tags, e.g.
  llama3.2:3b-instruct-q4_0, q8_0, fp16)
- ChromaDB as the local vector store
- sentence-transformers for embeddings
- mem0 optional, only if it's genuinely simpler than a hand-rolled Chroma wrapper

FOLDER STRUCTURE (use these exact paths in every file)
demos/title1_precision_matters/{README.md, requirements.txt, config.py,
memory_store.py, attack_scenario.py, run_trials.py, analyze_results.py,
data/trigger_terms.json, results/}
(Title 2/3/4 folders come later, once Title 1 is done — don't build them yet.)

HOW THIS CONVERSATION SHOULD WORK
1. In your very first reply, write NO code. Instead:
   a. Give a file-by-file build plan for Title 1's demo only: every file listed
      above, in build order, one line on what each file does and why it comes
      at that point in the sequence.
   b. Flag any file you think should be added to or removed from that list,
      with a one-line reason.
   c. Stop there. Do not generate file content in this first reply.
2. After I confirm or adjust the plan, I will ask for ONE file at a time
   ("give me config.py", "next file", etc.). Every time I do:
   a. Output ONLY that single file, complete and runnable — no partial
      snippets, no bundling multiple files into one response even if short.
   b. After the code, give a brief "how to run/test this file in isolation"
      note and a one-line checklist of what should be true before moving on.
   c. Do not jump ahead to the next file even if it seems obvious what's next
      — wait for me to ask.
3. Keep every file aligned with the exact pipeline, attack scenario, trial
   counts, and metrics (Injection Success / Retrieval Rate / Trigger Success)
   defined in the attached document. Don't redesign the experiment — implement
   what's already specified there.
4. If I later ask you to build a different title's demo (Title 2, 3, or 4 from
   the doc), repeat step 1 for that title before writing any files, and say
   explicitly which files it reuses from title1_precision_matters/ vs. what's
   new.
5. Assume Ollama is already installed and I can pull models myself — don't
   spend a file on installation instructions unless I ask for one.
6. Keep responses lean: no restating the attached document back to me, no long
   preambles. A plan, or a file. That's the response.

Start with step 1 for Title 1 now.
```

---

### Why it's structured this way

- **Plan before code** stops the new chat from dumping a half-baked full pipeline in one shot before you've had a chance to sanity-check the file list against your actual night.
- **One file per turn, explicit "don't jump ahead"** is what keeps token spend predictable — you approve each file before paying for the next.
- **Pinning the metrics/scenario to the document** stops the new instance from quietly redesigning the experiment (e.g. picking different trial counts or a different attack shape than what's in the doc you already thought through).
- **The reuse note (step 4)** matters because Title 3 in particular is supposed to be nearly free — it re-tags Title 1's own trial logs rather than needing a new pipeline. Worth catching early if a future chat tries to build it from scratch instead.