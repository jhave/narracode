# TODO

## Accepted — build these (jhave, 2026-07-30)

### A. The diff corpus
*"We already have the corpus and nobody meant to build it — that's the answer."*

`versions/` holds pre-edit and post-edit drafts of the same content across 25 stories. Paired supervision with the confound removed. Build it from the diffs.

- [ ] Walk every story folder; for each `versions/vN/drafts/*.md` pair, emit aligned span triples `before → after → derived rule` into a single corpus file
- [ ] Store the **spans**, not my interpretation of them — interpretations rot, spans don't (plan §7.5)
- [ ] Handle the messy cases: stories with no `versions/`, snapshots taken mid-composition rather than at a human edit, and edits made directly to `index.html` instead of the md
- [ ] Seed pair already exists and is verified: Interim Edge `v1 §1` ↔ PR #9 `§1` → 13 operations → registry classes 12–17
- [ ] Once populated, derive the two metrics from it: **tell density / 1,000 words** and **survival rate**

### B. The requirement list
Ban lists shift a tail; requirement lists move the distribution. Forms we *under*-produce relative to humans.

- [ ] Start from the documented case — **erotema** (rhetorical question), measurably suppressed in LLM text
- [ ] Candidates to measure before adopting: sentence-initial conjunctions, anacoluthon, unresolved deixis, flat repetition that models smooth into variation
- [ ] Structure it as the mirror of `master_ai_tells.md`: class, detector, **floor** rate rather than ceiling, human-corpus anchor
- [ ] Wire into `pre_draft` as generation constraints, not into `post_draft_tell_scan` as cleanup

## Open

### 1. AI-tells registry mechanics — design in `plans/2026-07-30_ai-tells-benchmark.md`
- [ ] Give every tell class a **machine-checkable detector** (regex / heuristic) so scans produce counts, not opinions
- [ ] Anchor target rates on **human corpora** (Williams, Knausgaard, Ōe, Butler) rather than on zero
- [ ] Expansion protocol: web sweep quarterly + every span he cuts twice. Prioritise by `severity × liveness`; liveness decays from **last confirmation**, not first sighting
- [ ] Standing question: **is there an idiomatic cadence signature to AI text?** Current answer and sources in the plan doc

### 2. Harness — remaining shifts
- [ ] Move tell constraints from post-draft cleanup to **pre-draft injection** (plan §7.1 — folded into B above where it overlaps)
- [ ] **Two-corpus scan** (plan §7.6): scan each draft against the registry *and* against the last three published stories, to catch self-quotation across projects
- [x] Rate-cap our own remedies the day they're adopted — done, `master_ai_tells.md` §"Our own remedies are the next tells"

## Knowingly deferred
Gaps we're leaving open for now, recorded so they don't get rediscovered as surprises.

- **Human-corpus baselines unmeasured.** Target rates are relative. *3.7 em-dashes per 1,000* only means something beside Knausgaard's number, and we don't have it. Every `target_rate` in the registry is provisional until this lands
- **Whose idiom is the target?** The benchmark measures distance from machine default, not proximity to jhave. Only his acceptances define the direction — hence survival rate
- **Does the registry generalise across projects, or is it per-poetics?** *Broccoli over legume* may be an Interim Edge fact or a jhave fact. Two more projects will tell
- **Where the floor is.** At some constraint density prose becomes constraint-satisfaction. Worth finding deliberately, in a throwaway

### 3. Alpha-Gaia (2026-07-31)
- [ ] jhave editing pass on `drafts/4-alpha-gaia-plainspoken.md` — no direct human edits yet; seamless-edit diff starts whenever he touches a draft
- [ ] Figure assets — five `Fig` blocks are diegetic render instructions (`Fig 0.1`–`Fig 4.5`). Fig 0.1 is now a full audio-description build, ~600 words, detailed enough to hand to an image model as-is
- [ ] Homepage card + `metadata.md` entry when ready (both hand-maintained)
- [ ] §1 is much the longest section after v3; the land/protein/opinion block is the movable part if the balance wants fixing — it could become its own feed item
- [ ] **Open thread left deliberately unresolved:** the avoidance anomaly (sensitized people take *fewer* precautions; three replications; unexplained). It is the reader's hook and the one piece of evidence CONSTANT could have used and did not. Do not close it in a later pass without deciding to
- [x] Registry classes 18 (statistic-with-a-shrug) and 19 (false-plainness list) appended to `master_ai_tells.md`
- [x] Registry class 20 (**genre-average instead of document-shape**) — v2, 2026-07-31. The strongest finding of the project so far, and the one with the clearest procedure: fetch the source, take its furniture, reset the content. Sub-tell: narration metaphor inside reportage (the *Nature* piece carries **zero** figures in the reporter's own narration)
- Second data point for **"does the registry generalise across projects?"** (Knowingly deferred #3): classes 1, 2, 8, 9, 11, 14 all fired again on a completely different poetics. Class 16 (accurate dull noun) and 17 (explained satire) did not fire — possibly Interim Edge facts

### 4. Interim Edge
- [ ] jhave editing pass on `drafts/7-condensed-final.md` §2–§6 (rewritten 2026-07-30 against his §1)
- [ ] Image assets — figures are caption-only, `Fig 0.1`–`Fig 6.7` written and ready
- [ ] Homepage card + `metadata.md` entry when he's ready to publish (both hand-maintained)
- [ ] 5 unapplied hits in `critiques/tells-7-condensed-final.md` — mostly folded into the rewrite; re-scan after his pass

## Done
- [x] `master_ai_tells.md` registry, 11 classes (2026-07-30)
- [x] Tell-scan mode + `post_draft_tell_scan` hook in `narracode.md` (2026-07-30)
