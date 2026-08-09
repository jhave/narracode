# Next steps — 2026-08-05

*Record of the 3–5 August 2026 working session, and what to do next. Companion to `plans/2026-08-05_cadence-displacement-implementation.md`.*

---

## What was decided

| question | answer |
|---|---|
| Adopt Fugu-style orchestration? | **No.** Needs a reward function; literary quality has none. |
| Use an LLM to judge prose quality? | **No.** Rubric judges rank AI stories *above* New Yorker fiction. The signal points backwards. |
| Fine-tune a model as a subtler editor? | **No.** Corpus is ~10² pairs; fine-tuning needs ~10⁴. It also averages away each project's target voice and ends provider-agnosticism. |
| Add a smoothing pass before jhave's edits? | **No.** It would diff future edits against smoothed text instead of machine default, corrupting the corpus as it grows. |
| So what? | **An addition to the harness: retrieval over the edit corpus, injected at `pre_draft`.** |

**The key reframe (jhave's):** the corpus is not jhave's voice. It is the voice he was reaching for in each project. So the learnable thing is not a destination — it is the **direction of correction**, which repeats across projects even though the targets don't.

---

## What exists now

Written this session, all on branch `claude/narracode-harness-qualitative-research-report`:

- `2026-08-01_ai-tell-assessment.html` — the tell registry documented as a report.
- `2026-08-03_harnessing-a-qualitative-domain-JHAVEdit_Opus5.html` — the research report, expanded for readers new to the project. jhave's edits preserved intact.
- `plans/2026-08-05_cadence-displacement-implementation.md` — the full technical spec for everything below.

Already on disk, unused: 15 `versions/` trees, 25 stories, 40 `edit-observations.md` files. Provenance is readable from directory names (`v3-...-jhave-section1` = human edit). **The corpus can be rebuilt retroactively.**

---

## Next steps

### Step 1 — Build the extractor *(half a day)*

Write `tools/extract_pairs.py`:

- walk every `versions/` directory
- find transitions from a machine snapshot to a jhave snapshot
- diff the drafts sentence by sentence
- write each before/after pair to `corpus/edit_pairs.jsonl`

No model call. Pure string processing.

**Output:** a few hundred to a couple thousand aligned pairs.

### Step 2 — Run the test *(an afternoon)* ← **this gates everything else**

For each pair, compute six numbers before and after the edit:

1. sentence-length variation
2. biggest jump between adjacent sentences
3. metaphor/simile rate
4. triplet rate
5. naming-clause rate
6. em-dash rate

Subtract before from after. Average across the corpus.

**Decision:**

- **Edits push consistently in the same direction** → the premise holds. Go to Step 3.
- **Directions scatter, or variance swamps the mean** → there is no recurring correction to learn. **Stop.** Do not build steps 3–5.

This is one afternoon against data already on disk. Do not build anything else before running it.

### Step 3 — Wire retrieval into `pre_draft` *(a day)*

Before drafting a scene, pull the 8 most similar past edits from the corpus and put them in the prompt as before/after examples, plus target ranges for the six numbers.

~600 tokens. **Replaces** the current top-N tell injection rather than adding to it.

This is the thing that does what fine-tuning would have done.

### Step 4 — Make it self-maintaining *(half a day)*

Trigger on commit or version snapshot — **not** a 24-hour cron. Re-run extraction, append new pairs, recompute targets. Every step deterministic; no LLM anywhere in the loop.

### Step 5 — Mechanical micro-pass *(optional, last)*

Only classes with survival ≥ 0.9. Deletions and fixed substitutions only. Writes a provenance log so the pre-pass text stays recoverable.

Do this last or not at all. It handles the boring edits only.

---

## Separate track — three file changes, independent of all the above

From the Aug 3 report. Cheap, unrelated to the corpus work, do them whenever:

1. **Per-character sentence-length targets** — different characters should measurably differ. Catches the "one narrator, several names" failure.
2. **Knowledge-asymmetry table** in `character-interiority.md` — turns plot reversals into a query over what characters conceal, instead of invention on demand.
3. **Signed `pressure` field** in `scene-ledger.md` — records whether a scene raised, held, or lowered stakes. Prevents the thriller-by-default shape.

---

## Do not

- Fine-tune anything that generates prose.
- Build the smoothing pass before Step 2.
- Add an automated quality score anywhere.
- Chase *delve* or em-dash counts as primary signals. Keep the em-dash count running; treat it as the least important dimension.

---

## The one-line version

**Extract the edit pairs, compute six numbers before and after each edit, and check whether the edits point the same way. If they do, feed the nearest past edits into `pre_draft`. If they don't, stop.**
