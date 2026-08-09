# Comparison against van Nuenen: a correction to the rarity claim

*2026-08-06. Prompted by the dimensionality-reduction survey jhave uploaded. Corrects
the conclusion of `2026-08-06_lexical-temperature.md`.*

---

## The comparison that was available and had not been made

`Voice Under Revision` (arXiv:2604.22142) has been in our bibliography since the
August 3 report, cited only for the fact that LLM editing normalises personal voice.
Its actual content is the **exact inverse of this project's experiment**:

| | van Nuenen | Narracode corpus |
|---|---|---|
| who revises | three frontier LLMs | jhave |
| what is revised | human personal narrative | machine literary fiction |
| n | 300 narratives | 1,234 pairs |

If human revision were stylometrically distinctive, the two should move in opposite
directions. They mostly do not.

## Result

Their thirteen markers, the five computable directly on our pairs:

| marker | jhave Δ | t | van Nuenen (LLM) | direction |
|---|---|---|---|---|
| mean word length | +0.35 | +8.53 | +8.5% | **same** |
| type-token ratio | +2.95 | +10.29 | +53% (MTLD) | **same** |
| comma rate | +11.21 | +3.52 | +67% | **same** |
| first-person density | −0.46 | −3.27 | −9% | **same** |
| contraction rate | +1.65 | +1.10 | −31% | opposite, not significant |
| em-dash | −3.15 (doc), −5.72 (pair) | −2.82 / −5.72 | **+326%** | **opposite** |

## What this does to the rarity finding

`2026-08-06_lexical-temperature.md` reported that jhave edits toward rarer words at
t = −18.60 and called it the strongest signal in the project. The measurement stands.
The **interpretation** does not.

Lexical rarity, type-token ratio, MTLD, Honoré's R and mean word length are one family.
Both jhave and the models move that family the same way. Rarity therefore appears to
measure **that a text was revised**, not **who revised it**. It was presented as
evidence of a distinctively human direction and that claim is withdrawn.

A prediction made before running this was also wrong. The reasoning was that van
Nuenen's mechanism produces *formal, latinate* substitutions, which are long, whereas
jhave's — `craw`, `spunk`, `trend-gagement` — are rare but short, so mean word length
should separate them. It does not: jhave's word length rises by almost exactly the
proportion theirs does.

## What survives

**The em-dash, and only the em-dash.** LLM revision raises dash frequency by 326% and
lifts the share of texts containing dashes from 26% to 72%. jhave removes them, at
t = −5.72 with 97% consistency. Both effects are large and the signs are opposite.
It is the one marker in either study that distinguishes the reviser.

That also explains why it kept coming out strong here while looking, in jhave's words,
like an overhyped meme. It is not a good detector of machine *authorship*. It is a good
detector of machine *revision*, which is a different and, for this harness, more useful
thing.

## The caveat this comparison deserves

The two studies do not share a baseline. van Nuenen revises casual spoken-register
personal narrative; this corpus revises machine literary fiction. Moving casual speech
toward formality and moving generic machine prose toward literary density could both
raise word length and lexical diversity while being opposite acts. The shared direction
is real; the shared *meaning* is not established.

Two mechanisms visibly differ under the same sign. Their comma increase comes from
introduced parenthetical structures — punctuation smoothing. jhave's comes with
sentences getting **shorter**, which is fragment punctuation. Same marker, opposite
construction.

## The larger point

Human revision and machine revision, on this evidence, are largely indistinguishable by
aggregate stylometry — while producing prose no reader would confuse. That is the
strongest available demonstration that aggregate stylometry does not capture the thing.
It is what jhave said intuitively before any of these measurements existed.

It does not weaken the retrieval proposal. Retrieval never depended on the markers
discriminating; exemplars carry the substitution itself. If anything this strengthens
the case, since it removes the temptation to use the vector as a target.

## What else the uploaded survey offers, ranked

1. **This comparison.** Done, above. Most valuable thing in the document.
2. **PCA on the displacement vectors.** Already proposed in
   `2026-08-05_cadence-displacement-implementation.md` §2.4 and now runnable on 1,234
   displacements. Answers how many dimensions actually carry variance rather than
   assuming six or seven. Cheap.
3. **Fightin' Words with informative priors** (Wilkens, via the survey). Identifies
   which specific words distinguish two corpora, with variance-adjusted priors so rare
   words do not dominate. Applied to words jhave adds versus words the model writes,
   this could name the discriminating vocabulary that aggregate measures cannot. The
   most promising untried method here.
4. **UMAP fitted on a human manifold, machine text projected in as test points**
   (Wilkens). Sound at CONLIT's 2,754 volumes. At nine stories it would fit noise.
   Not worth doing.
5. **BERTopic.** Thematic clustering for large literature reviews. No application here.

## Correction discipline

The lexical-temperature document keeps its measurements, which are correct, and gains
a pointer to this one. The interpretive claim that rarity is a human signature is
withdrawn rather than quietly edited, because the sequence — measure, over-claim,
control, retract — is the record worth keeping.
