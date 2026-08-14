# TODO

## Affect / physics track (jhave, 2026-08-14)

Design in `plans/2026-08-14_physics-graph-llm-ensemble.md`; passes and findings in
`plans/2026-08-14_experiment-0-1-results.md`.

**The insight the track rests on.** The three-layer intuition — physics for emotion, graph
for plot, LLM for prose — is a description of Narracode as it already is, not a proposal for
something new. All three layers exist; they are written as prose. So the only real question
is *which structural files should stop being prose and start carrying numbers*. That makes
the whole programme cheap: no new model, no training run, no rewrite.

**The rule that governs all of it.** Measurement belongs to the outer loop. Any number the
harness computes is a reading taken afterwards, never a target set before. A structural
quantity that becomes a goal stops describing the story and starts writing it. Now stated in
`narracode.md → The two loops`.

### Done
- [x] **Experiment 0 — promote the Affect module.** Ported into live `narracode.md`
  (two loops, `affect.md`, Discovery mode, failure signatures, `on_affect_discovery`).
  Designed 2026-05-24, built into the May-29 testing harness, unpromoted for 82 days,
  used by zero stories. Snapshot: `narracode_2026-08-14_pre-affect-promotion.md`
- [x] **`### The mix`** — affect as a studio effect: level per scene, judge the mix in the
  mix, effects come off first. The May design specified *which* primitives, never *how much*;
  uniform saturation was the module's real failure mode
- [x] **Experiment 1 instrument** — `tools/obligation_pressure.py`, probes declared in
  `obligations.md` so touch-detection is reproducible rather than recalled
- [x] Validated on *Interim Edge*: monotone-rising curve, 3.00 → 12.22, zero fade events.
  **The signature of refused resolution is a monotone curve with no fades** — which predicts
  that a conventionally resolving story shows sawtooth instead. Testable with one more story

### Next
- [ ] **Push `Garaiv` and `Spiral Brief`** — neither exists in this repo (checked working
  tree, all branches, full history, tags). Everything below is blocked on them
- [ ] Run Experiment 1 on both, **blind**: write probes from `obligations.md` alone, before
  opening the draft, and do not revise them after seeing where they fire. The *Interim Edge*
  probes were written with the answer in view — that run shows the tool works, not that the
  metric means anything
- [ ] Run `on_affect_discovery` on both after draft 2. Read the prose beside the proposed
  `affect.md`. This is the only question that matters before anything else gets built:
  **does a written-down vitality contour help the prose, or does it re-import the rendering
  grammar the phenomenological primitives were built to refuse?** A number is a name
- [ ] Compare curve shapes against jhave's own ranking of the finished pieces. *This is the
  falsification condition.* If the curves do not separate the pieces he rates highly from the
  ones he does not, the physics has no purchase on this project and the track stops here

### Held until the above says something
- [ ] **Experiment 2 — reader-belief ledger.** `reader-state.md` as open questions with
  probabilities; suspense = variance of next scene's beliefs, surprise = distance moved
  (Ely, Frankel & Kamenica). Checkable against the diff corpus in §A below: the prediction is
  that scenes jhave edits heavily are scenes where measured surprise is near zero
- [ ] Decide first: probabilities or ordinal bands (`unlikely / open / probably / assumed`).
  A model will happily emit `P = 0.63`; suspense-as-variance survives either
- [ ] **Experiment 3 — character state vectors**, blind-ranked A/B against the same sequence
  written without them
- [ ] **Experiment 4 — survival predictor** trained on the diff corpus. A critic, not a
  generator. The one place graph structure earns its keep, as features rather than as an
  architecture

### Refused, with reasons
- **No GNN.** Graph-as-data-structure and graph-neural-network are unrelated proposals
  sharing a word. No training data (25 stories), wrong output type (embeddings, not prose),
  and dominated by the LLM on its own task. Keep the graph, type its edges, drop the neural
- **No plot planner emitting outlines for the LLM to fill.** The failure joint of every
  symbolic story generator since Talespin. `narracode.md` already refuses it
- **No sentiment-driven controller at scene scale.** The sensor cannot see irony
- **No physics in `pre_draft`** until it has been read-only across several complete stories.
  Once a suspense number exists the harness optimises it and the prose becomes a thriller —
  the same dynamic already logged in `master_ai_tells.md` under "our own remedies are the
  next tells"
- **No Grade-C physics vocabulary** (force, momentum, conservation as literal claims). If
  nothing is conserved, do not say conservation. `narracode.md` is read by the model, and
  metaphor in the harness becomes metaphor in the output

### Reading
- Ely, Frankel & Kamenica, *Suspense and Surprise* — formal definitions over a belief path
- Pianzola 2024, *Dynamical systems, literary theory, and the computational modelling of
  narrative* — the theoretical citation for the whole idea
- arXiv:2606.16481, *Steering Emotional Dynamics for Art Therapy* — closest published
  neighbour to the three-layer intuition, and a limit case: a prescribed emotional trajectory
  is the deliverable in therapy and the failure mode in literature

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

### 3. Interim Edge
- [ ] jhave editing pass on `drafts/7-condensed-final.md` §2–§6 (rewritten 2026-07-30 against his §1)
- [ ] Image assets — figures are caption-only, `Fig 0.1`–`Fig 6.7` written and ready
- [ ] Homepage card + `metadata.md` entry when he's ready to publish (both hand-maintained)
- [ ] 5 unapplied hits in `critiques/tells-7-condensed-final.md` — mostly folded into the rewrite; re-scan after his pass

## Done
- [x] `master_ai_tells.md` registry, 11 classes (2026-07-30)
- [x] Tell-scan mode + `post_draft_tell_scan` hook in `narracode.md` (2026-07-30)
