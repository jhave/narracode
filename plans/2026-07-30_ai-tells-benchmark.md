# AI-tells benchmark — design

*2026-07-30. Claude Opus 5, at jhave's request. Companion to `master_ai_tells.md` and the `post_draft_tell_scan` hook.*

---

## 1. The standing question: is there an idiomatic cadence signature?

Yes, and it is narrower than "AI writes badly." The literature converges on three layers, in ascending order of usefulness to us.

**Lexical.** The most-studied and least interesting. The *delve* family — synthetic erudition. Kobak et al.'s PubMed work found the vocabulary shift in ≥13.5% of 2024 biomedical abstracts, up to 40% in some subcorpora. Useful as proof that the signature is real and measurable at corpus scale; useless for literary prose, because these words never appear in ours.

**Punctuational / structural.** The em-dash finding is the one that matters. [The Last Fingerprint](https://arxiv.org/html/2603.27006v1) argues the overuse is **markdown leaking into prose** — the smallest surviving unit of the structural orientation models acquire from markdown-saturated training. Rates vary 0.0 to 9.1 per 1,000 words *between models*, which makes it a fingerprint of fine-tuning, not of "AI" in general. Implication for us: registry class 10 should carry a target rate, not a ban.

Measured on *Interim Edge*, three drafts of the same story:

| draft | words | em-dash /1k | `the way {you,a,one}` /1k |
|---|---|---|---|
| v1 — machine, pre-edit | 5,555 | **5.6** | **1.3** |
| v3 — jhave's §1 only | 5,561 | 5.6 | 1.3 |
| v4 — §2–6 rewritten to his register | 5,171 | **3.7** | **0.2** |

Mid-range on em-dash rather than extreme, which corrects an eyeball estimate I made before running the count. The `the way X` figure is the one that moved, and it moved because a human deleted one instance and I generalised. **That is the whole method in three rows.** What is still missing is the fourth column: the same two rates measured on Williams and Knausgaard, so we know whether 3.7 is a destination or just less than 5.6.

**Rhetorical.** The most actionable finding, and it runs in *both* directions:
- LLM text **favours tricolon** — which is registry class 9, triadic escalation, arrived at independently from jhave's cuts.
- LLM text **suppresses erotema** — the rhetorical question. We under-produce a form humans use.
- **Performed-hesitancy excess**: LLMs produce genuine hesitancy markers at reasonable rates but *performed* hesitancy at roughly twice the human rate.

The third bullet is the important one and it is discussed in §5 below, because it is a trap sitting directly under our own best remedy.

**What this means for the harness.** The signature is not a list of bad words. It is a **distribution over forms** — some over-produced, some under-produced. A ban list only shifts the over-produced tail. A requirement list moves the whole distribution. We currently have only the ban list.

## 2. How detection is actually done now

Three families, all with known failure modes, none of which we should adopt uncritically.

| Family | Method | Why it fails |
|---|---|---|
| **Statistical** | Perplexity + burstiness. Human text varies sentence length; machine text is too predictable | Each model generation produces higher perplexity and more burstiness — not to evade detection, but because it writes better. The signal decays on its own |
| **Curvature** | [DetectGPT](https://openreview.net/pdf?id=UiAyIILXRd) — exploits negative curvature in log-probability space by perturbing and re-scoring | White-box (needs log-probs), compute-heavy, and adversarial paraphrasing drops detection from >70% to near-chance (~5%) at 1% FPR; three rounds of paraphrase ≈ zero |
| **Watermarking** | Bias token choice toward sequences implausible at human frequency | Survives neither post-editing nor paraphrase — i.e. neither of the two things jhave does to every draft |

**Consequence for us: we are not building a detector.** Every method above answers *"was a model involved?"* — a question whose answer here is a known and uninteresting yes. Our question is different and easier: *"does this prose carry the marks of unedited model default?"* We have the generator, the prompt, the pre-edit draft, the post-edit draft, and a single authoritative human judge. That is a supervised setup with n=1 annotator and perfect provenance. Detection research has none of that and is solving a harder problem badly.

## 3. The datastructure

Registry entry, one per class, machine-readable:

```yaml
- id: T011
  class: analogy-simile-x-the-way-y
  first_seen: 2026-07-30
  source: scan            # scan | jhave | web:<url>
  severity: 4             # 1–5, how strongly it reads as machine-made
  detector:               # machine-checkable — this is what makes it a benchmark
    type: regex
    pattern: '\b(the way (you|a|an|one)\b)'
    unit: per_1000_words
  target_rate: 0.4        # from human corpus, NOT zero
  observed:
    - {work: interim-edge, draft: 7-condensed, rate: 1.3, date: 2026-07-30}
  status: live            # live | retired | contested
  survival: 0.71          # fraction of flagged spans jhave accepted
  instances:
    - {work: interim-edge, span: "the way a seam is after strain", remedy: CUT, accepted: true}
```

Three fields carry the design:

- **`detector`** — without it the registry is a style guide. With it, a scan emits counts and the counts are comparable across drafts and against human corpora.
- **`target_rate`** — derived from human-corpus measurement, never zero. Zero is how prose gets sterilised. Williams uses tricolon; the question is at what rate.
- **`survival`** — the fraction of flagged spans jhave actually accepts. **This is the calibration signal.** A class with survival below ~0.3 is not a tell, it is my taste being wrong, and it gets `status: contested` then retired. Without this field the registry only accumulates and never learns.

## 4. Prioritisation — your "time identified?" question

Recency is real but it is a **decay term, not a priority**. Tells have a half-life, for two reasons: models change between generations, and a tell that becomes publicly known gets trained against. *Delve* is nearly dead as a signal for exactly that reason.

```
priority = severity × liveness × (1 − survival_penalty)
liveness = exp(−months_since_confirmed / 9)
```

Freshness is not what makes a tell worth fixing — **confirmation** is. A class re-confirmed by a jhave cut this month is live regardless of when it was first identified. So the decay clock resets on confirmation, not on entry. A class nobody has confirmed in a year is dead weight and should be archived rather than deleted, in case a future model brings it back.

## 5. The trap in our own remedy

The single most useful thing in the current literature, and it points at us:

> LLMs produce genuine hesitancy markers at reasonable rates but **performed** hesitancy markers at roughly twice the human rate.

Your `(panic? no, calm.)` is the best move in the §1 edit — the narration proposing a figure and refusing it in-line. It is also, structurally, *performed hesitancy*. Deployed once it reads as a mind thinking. Deployed six times it becomes the most legible machine signature in the piece, and worse than the thing it replaced, because it will read as *sincerity performed*.

I used it once in the §2–§6 rewrite. **It needs a hard rate cap in the registry — I would set 1 per 2,000 words — and it needs that cap before the device spreads, not after.** Same logic applies to any remedy we adopt: a fix applied uniformly becomes a fingerprint. The registry should track our own remedies with the same detectors it uses on the tells.

## 6. The benchmark corpus — we already have it

The `versions/` folders are labelled training data and nobody set out to make them that. For each story: a pre-edit machine draft and a post-edit human draft **of the same content**. That is a paired corpus with the confound removed.

First pair: `Interim Edge` `versions/v1/…/7-condensed-final.md` §1 ↔ PR #9 §1. Thirteen operations extracted in `versions/v3-…/edit-observations.md`. Across the 25 published stories there is real volume.

Two metrics, both cheap:

- **Tell density / 1,000 words**, per class, per draft. Tracks whether composition is improving or whether I am just cleaning up afterwards.
- **Survival rate.** Tracks whether the registry is right.

The first tells us about the prose. The second tells us about the registry. Both are needed; only the second prevents the thing from calcifying into received taste.

## 7. Suggested architectural shifts

Ordered by expected effect on the actual idiom.

**7.1 — Move constraints from post-draft to pre-draft.** *(biggest effect)*
`post_draft_tell_scan` cleans up after the fact. Cleanup produces prose that is *scrubbed* — the tell removed, the underlying habit intact, and a slight deadness where the excision happened. Inject the top-N live classes into `pre_draft` as generation constraints and the sentences arrive different. Cheaper too.

**7.2 — Add a requirement list.**
The rhetorical findings say we *under*-produce forms as reliably as we over-produce them. Erotema is the documented one. Others worth measuring on the human corpus: sentence-initial conjunctions, anacoluthon (the sentence that abandons its own syntax), unresolved deixis (*that*, *it*, with no antecedent supplied), and the flat repetition humans use that models smooth into variation. **A ban list shifts a tail; a requirement list moves the distribution.** This is the shift I would make first if only one were possible.

**7.3 — Anchor every target rate on named human corpora.**
`POETICS.md` already names references — Williams, Knausgaard, Ōe, Butler, Blanchot. Run the same detectors over a few thousand words of each and the targets stop being aesthetic assertions. *"Interim Edge runs em-dash at 8.2 per 1,000; Knausgaard runs 2.1"* is an argument. *"Too many em-dashes"* is not.

**7.4 — Register our own remedies.**
Every device adopted as a fix (parenthetical self-correction, noun-collision, subject-dropped verb chains, single-word fragments) gets a detector and a cap the day it is adopted. The §1 edit gave us five new devices at once. Uncapped, they are the next five tells.

**7.5 — Store the diff, not the verdict.**
`edit-observations.md` currently holds my *interpretation* of your edits. The durable artefact should be the aligned span pairs — `before → after → derived rule` — because interpretations rot and spans do not. This also makes the corpus in §6 machine-usable rather than something a future model has to re-read prose to reconstruct.

**7.6 — Two-corpus scan, not one.**
Scan the draft against the tell registry *and* against the last three published stories, flagging phrases that recur across projects. Self-quotation across a body of work is a signature the per-draft scan cannot see. (*the queue refills* and *nobody audits the river* nearly crossed from *Open Loops* into *The Chute*, and were caught by hand.)

## 8. Open questions I cannot answer alone

- **Whose idiom is the target?** The benchmark measures distance from machine default. It does not know which direction is *your* voice versus merely *not-machine*. Only your acceptances define that, which is why survival rate is load-bearing.
- **Does the registry generalise across projects, or is it per-poetics?** *Broccoli over legume* may be an Interim Edge fact or a jhave fact. Two more projects will tell.
- **What is the floor?** At some density of constraint the prose stops being writing and becomes constraint-satisfaction. Worth finding that edge deliberately, in a throwaway, rather than discovering it in a story we care about.

---

## Sources

- [The Last Fingerprint: How Markdown Training Shapes LLM Prose](https://arxiv.org/html/2603.27006v1)
- [DetectGPT: Zero-Shot Machine-Generated Text Detection](https://openreview.net/pdf?id=UiAyIILXRd)
- [Counterfactual LLM-based Framework for Measuring Rhetorical Style](https://arxiv.org/pdf/2512.19908)
- [Saying More Than They Know: Quantifying Epistemic-Rhetorical Miscalibration in LLMs](https://arxiv.org/pdf/2604.19768)
- [Voice Under Revision: LLMs and the Normalization of Personal Narrative](https://arxiv.org/html/2604.22142v1)
- [Stylometry recognizes human and LLM-generated texts in short samples](https://www.researchgate.net/publication/393713840_Stylometry_recognizes_human_and_LLM-generated_texts_in_short_samples)
- [T-Detect: Tail-Aware Statistical Normalization for Robust Detection of Adversarial Machine-Generated Text](https://arxiv.org/pdf/2507.23577)
- [Enhancing the robustness of Fast-DetectGPT against paraphrase attacks](https://ieeexplore.ieee.org/document/10962860/)
