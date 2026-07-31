# TODO

## Open

### 1. Internal AI-tells benchmark — design in `plans/2026-07-30_ai-tells-benchmark.md`
Turn `master_ai_tells.md` from a prose registry into a scored, expanding benchmark.

- [ ] Give every tell class a **machine-checkable detector** (regex / heuristic) so scans produce counts, not opinions
- [ ] Build the **paired corpus** from `versions/` — pre-edit draft vs post-jhave draft is labelled supervision for "what he removes." Interim Edge v1 §1 ↔ PR #9 §1 is the first pair
- [ ] Track two metrics per draft: **tell density / 1,000 words** and **survival rate** (fraction of flagged spans he accepts). Low survival = bad class, retire it
- [ ] Anchor target rates on **human corpora** (Williams, Knausgaard, Ōe, Butler) rather than on zero
- [ ] Expansion protocol: web sweep quarterly + every span he cuts twice. Prioritise by `severity × liveness`, where liveness decays with time-since-identified — tells have a half-life
- [ ] Standing question: **is there an idiomatic cadence signature to AI text?** Current answer and sources in the plan doc

### 2. Harness — architectural shifts proposed
- [ ] Move tell constraints from **post-draft cleanup to pre-draft injection** (top-N live tells as generation constraints)
- [ ] Add a **requirement list**, not just a ban list — forms LLMs *under*-produce (erotema, anacoluthon, unresolved deixis). Bigger distributional effect than banning
- [ ] Rate-cap the self-correction device before it becomes the next tell (see plan, §"The trap in our own remedy")

### 3. Interim Edge
- [ ] jhave editing pass on `drafts/7-condensed-final.md` §2–§6 (rewritten 2026-07-30 against his §1)
- [ ] Image assets — figures are caption-only, `Fig 0.1`–`Fig 6.7` written and ready
- [ ] Homepage card + `metadata.md` entry when he's ready to publish (both hand-maintained)
- [ ] 5 unapplied hits in `critiques/tells-7-condensed-final.md` — mostly folded into the rewrite; re-scan after his pass

## Done
- [x] `master_ai_tells.md` registry, 11 classes (2026-07-30)
- [x] Tell-scan mode + `post_draft_tell_scan` hook in `narracode.md` (2026-07-30)
