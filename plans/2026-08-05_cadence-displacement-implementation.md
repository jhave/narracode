# Cadence displacement — implementing the edit corpus as a live harness input

*2026-08-05. Claude Opus 5, at jhave's request. Successor to `plans/2026-07-30_ai-tells-benchmark.md` §7. Responds to the question: given the paired corpus, what is the optimal thing to build — fine-tuning, or an addition to the harness?*

---

## 0. Your reading is correct, and it sharpens the problem

Yes: the proposal is to store the actual diff between machine output and human-edited text as aligned span pairs, explicitly labelled, and treat the accumulation as a corpus. Three things I checked while writing this:

- **Provenance is already encoded and needs no manual labelling.** Version directories carry it in the name — `v1-2026-07-30-automode-first-pass`, `v2-...-tell-scan`, `v3-...-jhave-section1`, `v4-...-register-rewrite`. A transition from a machine-named snapshot to a jhave-named snapshot is a human edit. The extractor can be fully automatic.
- **The corpus is larger than the benchmark doc assumed.** 15 `versions/` trees, 40 `edit-observations.md` files, 25 published stories.
- **It is currently stored in the wrong form.** All 40 observation files hold prose interpretation ("Simplification to Essential Presence: Stripping of structural scaffolding in favour of direct spatial presence"), not aligned spans. §7.5 of the benchmark doc identified this. The underlying draft text still exists in the version snapshots, so **the corpus can be rebuilt retroactively.** Nothing has been lost, but nothing is currently machine-usable either.

### 0.1 Your correction to the "whose voice" question

The benchmark doc listed as unanswerable: *the registry measures distance from machine default; it does not know which direction is your voice versus merely not-machine.*

Your correction: the corpus is **not your voice**. It is, in each instance, the voice you were attempting to find for that project.

This is not a softening of the problem. It changes what the corpus is. A corpus of one author's prose defines a point — a fixed style you could in principle train toward. A corpus of one author's *edits*, each made under a different project's commitments, defines something else: a set of **displacements**, each from where the machine landed toward where that project needed to be.

The consequence is concrete and determines everything below:

> The stable, learnable quantity is not the destination. It is the **direction of correction** — the vector from machine default toward project target, which recurs across projects even though the targets do not.

*Interim Edge* wanted one register, *Aft of Nowhere* another. But in both, the edit moved figuration down, sentence-length variance up, and named emotion out. That recurring direction is the extractable thing, and it is extractable at the sample size you actually have.

---

## 1. Pushback

You asked for it in two places. Here it is in three.

### 1.1 Fine-tuning — right conclusion, wrong reason

You rejected fine-tuning because the models are platform-based, not local, and capable open-weight models do not yet run on your machine. That premise is not quite right, and the conclusion survives anyway for a stronger reason.

**The premise is wrong.** Fine-tuning does not require local models. OpenAI offers supervised fine-tuning on GPT models through its API; Google offers tuning on Gemini through Vertex AI. You could fine-tune today without owning a GPU. Anthropic does not offer it broadly, which matters given the Compositional role currently runs on Sonnet, but "no local models" is not the blocker.

**The conclusion is right for three other reasons:**

1. **Sample size.** Supervised fine-tuning for style needs order 10⁴ examples to beat few-shot prompting, and degrades below roughly 10³. Your corpus, fully extracted, will yield somewhere between a few hundred and low thousands of aligned span pairs. That is squarely in the range where **retrieval outperforms fine-tuning** and is the single decisive argument.
2. **It freezes a moving target.** This follows directly from §0.1. A fine-tune bakes in a weighted average of every project's target voice. The averaging is precisely what the harness exists to prevent — it produces one register applied uniformly, which is median collapse arrived at by a more expensive route.
3. **It ends provider-agnosticism.** You stated this constraint in June when declining the Fugu routing table. A fine-tune binds the harness to one vendor's model generation and has to be redone when that model is deprecated. The corpus, as text, survives every model transition.

**One narrow case where a fine-tune would be legitimate**, recorded so it is not lost: training a small model as a *span detector* rather than a writer — input a sentence, output which registry class it instantiates. That is a classification task with a clear objective and would work at a few thousand labelled spans. It is worth revisiting only if regex detectors prove insufficient (§2.4). Do not fine-tune anything that generates prose.

### 1.2 The "final smooth pass before human edits" — resist this

This is the part of the brief I think is wrong, and the strongest argument against it is already in your repository.

`2026-05-14_architectural_harness_observations-CLAUDE.md` records that the most load-bearing rule in the harness is the `post_draft` silence — the prohibition on following a draft with another pass. The stated reason: a self-critique chain "defensively trains the next pass toward consensus." The benchmark doc reaches the same conclusion from the other side, describing post-hoc cleanup as producing prose that is "scrubbed — the tell removed, the underlying habit intact, and a slight deadness where the excision happened."

A smoothing pass inserted between generation and your reading is that chain, reintroduced at the point where it does most damage. Two specific harms:

**It destroys the measurement.** This is the serious one. If a smoothing pass runs before you read the draft, then your subsequent edit is a diff against *smoothed* text, not against machine default. The corpus stops recording the displacement in §0.1 and starts recording a residual — the part of the correction the smoother failed to make. The signal degrades exactly as the system accumulates more data, which is the worst possible failure shape.

**It optimises the registry rather than the prose.** A pass that removes everything the registry flags produces text with a survival rate of 1.0 by construction, which makes the calibration signal uninformative. The registry can then never be shown to be wrong (benchmark doc §3).

**What you actually asked for is served better by moving earlier, not later.** Your goal is to reduce your editing burden. §7.1 of the benchmark doc already identifies the change with the largest expected effect: inject live constraints at `pre_draft` so the sentences arrive in the right register, rather than removing constructions afterwards. Less editing, no corpus damage, and cheaper — one constrained generation instead of a generation plus a scan plus a rewrite.

### 1.3 What survives of the micro-pass, and how to make it safe

There is a version worth building. Restrict it to operations that are **deterministic, reversible, and already ratified at high survival rates**:

- Only classes with `survival >= 0.9` over at least 20 flagged instances.
- Only remedies that are a deletion or a fixed substitution — never a rewrite, never a judgement call.
- **Every change written to a provenance log**, so the pre-pass text is recoverable.

The provenance log is what makes it safe. With it, your subsequent edit is diffed against the *original machine output*, with the micro-pass changes subtracted out. The corpus stays clean. Without it, §1.2's first harm applies in full.

```
drafts/3-scene.md                    # what you read and edit
drafts/.3-scene.premicro.md          # machine output before the micro-pass
drafts/.3-scene.micro.jsonl          # every change: span, class, offset
```

Expect this to handle a small fraction of your edits — the mechanical ones. It will not touch the judgement-heavy edits, which are the ones worth measuring anyway.

### 1.4 The 24-hour cycle — use an event trigger instead

A daily cron is the wrong shape. Edits arrive in bursts when you are working on a story and not at all for days. The full extraction is deterministic string processing and runs in well under a second on this corpus, so there is no batching argument.

Trigger on the event that already exists: a version snapshot, or a git commit touching `drafts/`. The system is then current at all times rather than up to 24 hours stale, and costs less.

---

## 2. The measurement: cadence displacement

You said you suspect there is a numeric indicator in the cadence, related to the tendency to produce triplets and confident metaphors. That intuition is correct and is directly implementable. This section formalises it.

You also said, correctly, that *delve* and the em-dash are overhyped. They are in the vector below only because the em-dash is cheap to count and you asked for persistent checking; it is the least important dimension.

### 2.1 The vector

Six dimensions, all computable by tokenizer and regex, **no model call**:

| dim | name | definition | why |
|---|---|---|---|
| `d1` | sentence-length variation | coefficient of variation (sd/mean) of sentence lengths in the passage | cadence; the burstiness signal |
| `d2` | adjacent jump | 90th percentile of \|len(sᵢ) − len(sᵢ₋₁)\| | cadence; whether long and short sentences actually collide |
| `d3` | figuration rate | registry classes 11 + 12 per 1,000 words | your "fancy metaphors" |
| `d4` | tricolon rate | registry class 9 per 1,000 words | your "triplet" |
| `d5` | naming-clause rate | registry classes 5 + 8 per 1,000 words | narration explaining itself |
| `d6` | em-dash rate | registry class 10 per 1,000 words | persistent check only |

`d1` and `d2` are the cadence pair; `d3` and `d4` are the two tendencies you named. That is your hypothesis, written as four numbers.

Computed per **scene**, not per draft. A whole-draft average conceals the thing being measured, for the same reason a frequency conceals rhythm.

### 2.2 Displacement, not score

For every aligned pair in the corpus, compute the vector before and after the human edit:

```
d = v_after − v_before          # one displacement per edit
D = mean(d) over corpus         # the direction of correction
D_project = mean(d) within one project
```

`D` is the formal statement of §0.1: the direction you consistently move prose, independent of where any individual project was heading.

**For a new draft, do not compute a score.** Compute `v_draft`, and report per-dimension distance to the region your edits land in:

```
Scene 4 — cadence report
  d1 sentence variation   0.31   ↓ 1.8σ below post-edit region
  d3 figuration           2.9    ↑ 2.4σ above post-edit region
  d4 tricolon             1.1    within range
```

Three properties this has that a score does not:

- **It is diagnostic.** "Figuration 2.4σ high" names the operation to perform. "Quality 0.62" does not.
- **It is Goodhart-resistant.** There is no scalar to maximise. Each dimension has a target *range* with both an upper and a lower bound, so pushing any dimension produces a warning rather than a better number. This is the target-rate principle from the registry, generalised.
- **It never evaluates prose.** It reports the position of a draft relative to an empirically observed region. It contains no notion of good.

### 2.3 What this measures that the registry cannot

The registry counts constructions and asks whether each is above target. The vector measures the **joint position**, which is the aggregate case the benchmark doc left open (§2.4 of the 08-03 report): every dimension can sit within its individual range while the combination sits far from anywhere your edits have ever landed. Mahalanobis distance to the post-edit region catches that; per-class thresholds cannot.

### 2.4 Honest limits

- `d3`, `d4`, `d5` rely on regex approximations of semantic categories and will produce false positives. **Their precision is measurable**: the fraction of detector hits that coincide with an actual edit in the corpus. Report it per dimension and drop any detector below ~0.5 precision rather than trusting it.
- Six dimensions is a guess. The corpus can settle it: run PCA on the observed displacements and check how many components carry real variance. If two dominate, use two.
- Scene-level samples are short, and `d1`/`d2` are unstable below roughly 15 sentences. Report them with sample size attached, or pool short scenes.

---

## 3. Implementation

Four components. Total, on the order of 400 lines of Python and no new dependencies beyond what `build_site.py` already implies.

### 3.1 Extractor — `tools/extract_pairs.py`

Deterministic. No model call.

```
for each story in "Stories written with Narracode"/:
    snapshots = sorted(versions/)
    for (a, b) in consecutive(snapshots):
        provenance = "human" if "jhave" in b.name else "machine"
        if provenance != "human": continue
        for draft in common drafts of a, b:
            sentences_a, sentences_b = sent_tokenize(each)
            for op in SequenceMatcher(sentences_a, sentences_b).opcodes:
                if op is not 'equal':
                    emit pair(before, after, op_type, story, scene, date)
```

`op_type` is the operation field proposed in §4.3 of the 08-03 report — `split`, `join`, `shorten`, `reorder`, `delete`, `insert` — read directly from the opcode structure rather than inferred by a model.

Run once over history to rebuild the corpus retroactively; thereafter incrementally.

### 3.2 Index — `corpus/edit_pairs.jsonl`

One record per pair. Append-only, human-readable, diffable, survives every model change.

```json
{"id": "interim-edge/7-condensed/s014",
 "story": "30-07-2026_Interim_Edge",
 "scene": "§1",
 "date": "2026-07-30",
 "before": "Two minutes forty, and he stood there for all of it.",
 "after": "Two minutes forty.",
 "op": "shorten",
 "classes": [2],
 "v_before": [0.28, 11, 0.0, 0.0, 1.8, 5.6],
 "v_after":  [0.34, 19, 0.0, 0.0, 0.0, 5.6],
 "poetics_ref": "Stories.../30-07-2026_Interim_Edge/POETICS.md"}
```

`poetics_ref` is what keeps the corpus multifaceted rather than averaged: every pair remains attached to the project commitments under which the edit was made, so retrieval can prefer pairs from projects with similar commitments.

### 3.3 Retrieval at `pre_draft` — the actual replacement for fine-tuning

This is the addition to the harness, and the form matters more than the fact.

Before drafting a scene:

1. Compute the target vector for this scene — `v_after` centroid of corpus pairs matching this project's POETICS and this scene type.
2. Retrieve the **k nearest edit pairs** (k ≈ 8) by combined distance over cadence vector, scene type, and POETICS similarity.
3. Inject them into the `pre_draft` context as before/after exemplars, with the operation named.
4. Inject the target ranges for `d1`–`d5` as explicit numeric constraints.

```
Cadence target for this scene: d1 0.45–0.62, d3 below 1.2, d4 below 0.8.

Edits previously made in comparable passages:
  shorten: "Two minutes forty, and he stood there for all of it."
        -> "Two minutes forty."
  delete:  "...the queue, which is only a way of waiting."
        -> "...the queue."
  [six more]
```

Why this beats fine-tuning on every axis you named:

| property you asked for | retrieval | fine-tune |
|---|---|---|
| rapid | index rebuild < 1s | hours per run |
| agile — ingests fresh examples | new edit usable immediately | requires retraining |
| nuanced, multifaceted | exemplars conditioned on scene and POETICS | one averaged style |
| provider-agnostic | plain text in a prompt | bound to one vendor |
| works at your n | designed for small n | needs 10⁴ |
| inspectable | you can read why it retrieved | opaque |

The corpus does the work a fine-tune would do, without averaging away the per-project target.

### 3.4 The loop — `tools/ingest_edit.py`

Event-triggered (§1.4), not scheduled. On a commit touching `drafts/` or on a version snapshot:

```
1. extract new pairs since last run          (deterministic)
2. compute v_before, v_after per pair        (deterministic)
3. append to corpus/edit_pairs.jsonl         (deterministic)
4. recompute D, per-project D, target ranges (deterministic)
5. update registry survival rates from accept/reject (deterministic)
6. write corpus/cadence_targets.json         (deterministic)
```

**Every step is deterministic.** The loop you described needs no LLM at all — it is diffing and counting. That is the computationally elegant answer: the expensive component you were imagining does not need to exist.

The only place a model earns its cost is optional sentence-alignment for heavily rewritten passages where `SequenceMatcher` fails. Fall back to skipping those pairs rather than calling a model; a lost pair is cheaper than a wrong one.

---

## 4. Cost

| component | build | per-run |
|---|---|---|
| extractor | ~150 lines | < 1s full corpus |
| vector | ~80 lines | negligible |
| index | ~40 lines | negligible |
| retrieval at `pre_draft` | ~100 lines | ~600 tokens added to context |
| micro-pass (§1.3) | ~120 lines | one cheap model call, optional |

The 600-token figure is the number that matters, given context rot. It replaces, rather than adds to, the top-N registry injection proposed in benchmark §7.1 — the exemplars carry the same information in a more usable form.

---

## 5. Build order

1. **Extractor + index** (§3.1, §3.2). Everything depends on it, it is pure string processing, and it recovers the corpus retroactively from 15 version trees.
2. **Cadence vector + displacement** (§2.1, §2.2). Run over the rebuilt corpus. **This is also the test of the whole proposal** — see §6.
3. **Retrieval at `pre_draft`** (§3.3). The replacement for fine-tuning.
4. **Event-triggered loop** (§3.4). Makes it self-maintaining.
5. **Micro-pass with provenance log** (§1.3). Last, smallest, and only for classes at survival ≥ 0.9.

Steps 1 and 2 are worth doing even if 3–5 are never built: they answer whether the corpus contains a consistent signal, which is currently unknown.

---

## 6. What would falsify this

Run step 2 and look at the displacements before building anything else.

- **If `D` has no consistent direction** — if displacements across projects point in unrelated directions, or the variance swamps the mean — then there is no recurring correction to learn, §0.1 is wrong, and retrieval will retrieve noise. Stop.
- **If `d3` and `d4` do not move** under your edits, the triplet-and-metaphor hypothesis is wrong and the vector needs different dimensions. The corpus will say which, via PCA on the displacements.
- **If detector precision is below ~0.5** for `d3`–`d5`, the regexes are not measuring the categories they claim to, and the narrow fine-tuned *detector* from §1.1 becomes worth revisiting.

The whole proposal rests on one empirical claim — that your edits have a consistent direction in a low-dimensional cadence space — and that claim is testable in an afternoon with data already on disk. Test it before building the rest.

---

## 7. Summary

- Your reading of the corpus proposal is right, and provenance is already machine-readable from directory names.
- Your correction on whose voice this is turns the corpus from a style target into a **direction of correction**, which is the learnable quantity and is learnable at your sample size.
- Fine-tuning is the wrong tool — not because models are remote, but because n is two orders of magnitude too small, it averages away the per-project target, and it ends provider-agnosticism.
- A smoothing pass before your edits would corrupt the measurement it depends on. Move the constraint to `pre_draft` instead. Keep only a mechanical micro-pass, restricted to survival ≥ 0.9 operations, with a provenance log.
- The numeric indicator you suspect exists is a six-dimension vector, of which four are cadence variation and the two tendencies you named. Report displacement and per-dimension distance, never a score.
- The autonomous loop requires no LLM. It is diffing and counting, event-triggered, sub-second.

Build the extractor and the displacement calculation first. They test the premise.
