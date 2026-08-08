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

Step 2 earned its keep by being able to fail. Step 3 gets the same discipline.

Draft six scenes twice, once with retrieved exemplars in `pre_draft` and once without,
same prompt and same structural state. Present them to jhave unlabelled and in random
order. He edits both as normal.

**Measure: total edit distance he applies to each.** If the retrieval version needs
materially less editing, it works. If the two are indistinguishable, retrieval does not
transmit the 91% either, and the honest conclusion is that this line of work has
reached its limit — at which point the corpus stands as a documented negative result
about the measurability of literary revision, which is publishable and worth having.

Cost: six scene-pairs and one evening of editing.
