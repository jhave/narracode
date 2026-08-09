# Step 2 result: what the measures found, what they missed, and what to do

*2026-08-06. Written after the displacement test, in answer to jhave's question:
is this worth doing anymore?*

---

## The four live measures

Length-controlled, from 1,234 pairs and 20 document-level transitions:

| measure | movement | t | consistency | holds in every story |
|---|---|---|---|---|
| mean sentence length | −2.01 words | −4.36 | 95% | yes (5/5) |
| em-dash count | 158 → 114 | −5.72 | 97% | yes |
| naming-clause count | 12 → 1 | −3.07 | 100% | yes |
| figuration count | 33 → 22 | −2.86 | 87% | yes |

Dropped: sentence-length variation (42% consistency, null), adjacent-jump (null once
normalised), tricolon (73 → 74, null).

**Every surviving measure is subtractive.** Nothing the corpus can detect is additive.

## The number that matters

Of 689 pairs with text on both sides:

- **9.0%** move any lexical marker the measures can see
- **74.9%** change length with no marker moving
- **16.1%** change neither

**The four measures say something about 9% of the edits. 91% is rewriting they are
blind to.**

Samples from the unexplained 91%, same length, no marker:

```
"The paper curled between their fingers, thin and warm from the thermal…"
   ->  "The paper curled between craw fingers, thin and warm from tippled thermal…"

"Users implicitly analyze pronouns."   ->  "Users implicitly analyzing pronouns."
"how is that fake."                    ->  "how is that fake?"
```

`their` → `craw`. `thermal` → `tippled thermal`. A full stop to a question mark. No
rule states these and no detector in the registry sees them.

## So jhave's reading is right, with one correction

Right: there is no tractable procedural account of the writing. The measurable part is
a thin subtractive shell — cut length, cut em-dashes, cut the clause that explains the
image — around a 91% core that is exactly what he described: substitution at the level
of texture, weight and sound.

The correction is about what follows. The measures failed as a **theory** of the
voice. They did not fail as a **corpus**. Those are different objects and only the
first was falsified.

One further result deserves recording: the direction that survived is entirely
negative. That is the same finding `2026-05-14_architectural_harness_observations-CLAUDE.md`
reached from inside composition — *the active discipline of the system is what it
forbids, not what it organizes* — now measured rather than observed. It has been
independently confirmed twice by different methods, which makes it the most robust
result this project has.

## Why the work continues anyway

The six dimensions existed to give the model a **target**: aim here. That is dead,
and should stay dead — a 9% instrument used as a control signal would optimise the
shell and leave the substance untouched, which is Goodhart with extra steps.

Retrieval needs no target. Putting eight real `before → after` pairs into `pre_draft`
transmits `their → craw` without anyone naming why it is better. The exemplars carry
the 91% precisely because nobody had to theorise it. **The failure of the vector is an
argument for retrieval, not against it** — it establishes that the corpus holds far
more than the measurements could name.

## Revised plan

| step | status |
|---|---|
| 1. corpus | **done** — 1,234 pairs, validated PASS |
| 2. displacement test | **done** — direction exists, explains 9% |
| 3. retrieval into `pre_draft` | **do this** — does not depend on the dimensions |
| 4. event-triggered loop | do, if 3 works |
| 5. mechanical micro-pass | **drop** — at 9% coverage it would touch almost nothing |

The cadence vector is retained as a **diagnostic only**. It may be reported. It must
never be used as a generation target or a gate.

## The test for Step 3, decided before building it

Step 2 earned its keep by being able to fail. Step 3 gets the same discipline. Two
stages: the first is free and can kill the idea before jhave spends any time; the
second costs one story he was going to write anyway.

### Stage 1 — leave-one-story-out, automatic, no human time

Uses ground truth already in the corpus. For each story `S` with enough pairs:

1. Take a machine draft `M` from `S` and jhave's edited version `H` of the same draft.
   Both already exist.
2. Re-draft the same scene with retrieval enabled, drawing exemplars **only from
   stories other than `S`** — 669 pairs remain when the largest story is held out, so
   this is comfortable. Call the result `M'`.
3. Measure position on the four live measures. Does `M'` sit closer to `H` than `M`
   does?

This does **not** use edit distance between `M'` and `H`. Two independently generated
drafts of the same scene differ mostly in content, and content would swamp any style
signal. The four measures are style-level and content-independent, which is exactly
what makes them usable as an evaluation even though they failed as a target.

The logic is a kill-switch, not a proof: retrieval that cannot move the 9% shell will
certainly not move the 91% underneath. Passing stage 1 means little; failing it ends
the line of work for a few hours of compute.

### Stage 2 — blind arm assignment inside a real story

Only if stage 1 passes.

The flawed version of this test is to draft each scene twice and have jhave edit both.
He would be reading the same content twice, and the second pass is contaminated by
already knowing it. So each scene is seen **once**:

1. Start a **new** story, not in the corpus, so no exemplar can be drawn from it.
2. For each scene, flip a coin. Heads, `pre_draft` gets eight retrieved exemplars.
   Tails, `pre_draft` runs as it does today. Record the assignment; do not show it.
3. jhave writes the story exactly as he normally would, editing each scene as it comes.
   He is never told which arm a scene came from and never sees an alternate version.
4. Aim for eight to ten scenes, so four or five land in each arm.

**The measure is already built.** Run `tools/extract_pairs.py` over his edits and count
pairs per thousand words, per scene, by arm. That is literally the quantity this whole
pipeline was constructed to produce, so no new instrument is required and the units are
the same ones used throughout.

Secondary measures from the same run: mean words removed per scene, and the share of
edits that are pure substitution — the 91% class — versus the 9% the markers catch.
Whether retrieval moves the substitution class is the real question; the marker class
is only the kill-switch.

### What each outcome means

- **Retrieval arm needs materially less editing.** Step 3 works. Build step 4.
- **Indistinguishable.** Retrieval does not transmit the 91% either. Stop. The corpus
  then stands as a documented negative result about the measurability of literary
  revision, which is publishable and worth having.
- **Retrieval arm needs more editing.** Exemplars are pulling toward a house average
  rather than toward the project. That is the median-collapse failure appearing inside
  the remedy, and it is worth writing up on its own.

Cost: one story, written as normal, plus the coin flips.
