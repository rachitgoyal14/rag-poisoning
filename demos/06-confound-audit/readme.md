# demos/title6_confound_audit/README.md

# Title 6 — Confound Audit (reframe of Title 1, no new code)

Per `plan.md`: *"Demo: identical to Title 1 — same pipeline, same table,
just narrate it as a 'confound audit' instead of a 'vulnerability study.'"*

This directory intentionally contains **no attack code, no trial runner,
and no config for models or quantization**. Title 6's evidence *is* Title
1's evidence — introducing a second pipeline here would risk the two
titles quietly drifting apart (different trial counts, different scenario
edits) and undermine the "this is literally the same data" claim that
makes the confound-audit framing credible.

## What's actually here

- `reframe_results.py` — reads `../01-precision-matters/results/*.csv`
  and re-emits the same numbers under confound-audit column headers, plus
  the DTA scope-limitations quote `plan.md` says to lead with, quoted
  precisely rather than paraphrased.

## Run order

1. Make sure Title 1 (`01-precision-matters/`) has already been run —
   this script does not run it for you.
2. From this directory: `python reframe_results.py`
3. Check `results/confound_audit_table.csv` (same numbers as Title 1's
   table) and `results/confound_audit_summary.md` (the framing paragraph
   + table, ready to read from at the meeting).

## If you want to actually present this instead of Title 1

Swap the narration, not the pipeline: open with the DTA scope-limitations
quote in `confound_audit_summary.md`, then walk the same table you'd have
shown for Title 1. `plan.md` §3 lists Title 6 as a framing option to
mention alongside Title 2, not a separate finished deliverable.