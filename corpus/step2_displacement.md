# Step 2 — displacement test

`tools/step2_displacement.py` · cadence 1.0.0
## VERDICT: **PROCEED**

Document-level dimensions with a consistent direction: d1_mean_sent_len, d3_figuration, d6_emdash.

Pair-level: d3_figuration, d5_naming, d6_emdash.


**The question:** do jhave's edits push prose in a consistent direction?

If displacements scatter, there is no recurring correction to learn and Steps 3-5 should not be built.

`t` is a one-sample t against zero (normal approximation; scipy is not available here). `**` marks |t|>2, `***` |t|>3. `consistency` is the share of non-zero displacements agreeing with the mean's sign.

## Document level

20 machine&rarr;human transitions, whole drafts. The only level where d1 and d2 exist.

| dimension | n | mean Δ | sd | t | consistency |
|---|---|---|---|---|---|
| d1_mean_sent_len | 20 | -2.0116 | 2.0618 | -4.36*** | 95% |
| d2_len_cv | 20 | -0.0278 | 0.0872 | -1.42 | 42% |
| d3_figuration | 20 | -0.5500 | 0.8646 | -2.84** | 100% |
| d4_tricolon | 20 | +0.6000 | 2.3537 | +1.14 | 64% |
| d5_naming | 20 | -0.2500 | 0.6225 | -1.80 | 100% |
| d6_emdash | 20 | -3.1500 | 4.9927 | -2.82** | 89% |
| word count | 20 | -123.4000 | 200.2529 | -2.76** | 72% |

## Pair level

689 pairs with text on both sides. d1 and d2 are omitted: 951 of 954 before-spans are a single sentence, so a length series does not exist.

| dimension | n | mean Δ | sd | t | consistency |
|---|---|---|---|---|---|
| d3_figuration | 689 | -0.0160 | 0.1467 | -2.86** | 87% |
| d4_tricolon | 689 | +0.0015 | 0.2876 | +0.13 | 51% |
| d5_naming | 689 | -0.0160 | 0.1364 | -3.07*** | 100% |
| d6_emdash | 689 | -0.0639 | 0.2931 | -5.72*** | 97% |
| word count | 689 | -3.6009 | 9.1052 | -10.38*** | 65% |

## Does the direction hold across stories?

Mean displacement per story, document level. Agreement matters more than magnitude: a direction that reverses between projects is not a direction.

| story | d1 mean sent len | d2 len cv | d3 figuration | d4 tricolon | d5 naming | d6 emdash | n |
|---|---|---|---|---|---|---|---|
| 12-06-2026_Post_Everything | -0.068 | +0.005 | +0.000 | +0.000 | +0.000 | +0.000 | 2 |
| 15-06-2026_TheCompulsionLoop | -0.330 | -0.100 | -1.000 | +0.000 | +0.000 | +0.000 | 1 |
| 25-06-2026_Crepuscular | -1.419 | -0.028 | -0.800 | +0.400 | -0.300 | -4.300 | 10 |
| 26-06-2026_The_First_Water_Molecul | -4.247 | -0.032 | -0.333 | +1.333 | -0.333 | -3.333 | 6 |
| 30-07-2026_Interim_Edge | -0.100 | +0.007 | +0.000 | +0.000 | +0.000 | +0.000 | 1 |


---

## Control analysis: why the dimensions were redefined

The first run used all six dimensions as **rates per 1,000 words**, as the plan
specified. Under edit the text shortens by 19.7% (18.3 → 14.7 words per span), which
inflates every per-1,000 rate by roughly 25% for free. Re-running on raw counts
changed one result's sign and strengthened three others:

| dimension | as a rate | as raw counts | conclusion |
|---|---|---|---|
| tricolon | +2.35 (t=+1.98) | 73 → 74 (t=+0.13) | **artifact — no effect** |
| em-dash | −0.84 (t=−1.69) | 158 → 114 (t=**−5.72**) | real, far stronger |
| naming clause | −0.79 (t=−2.63) | 12 → 1 (t=−3.07) | real, near-total |
| figuration | −0.24 (t=−0.75) | 33 → 22 (t=−2.86) | real |

The two sequence dimensions were confounded the same way. The 90th-percentile
adjacent sentence-length jump looked like the strongest signal in the corpus
(mean −5.95, t=−3.28, 93% consistency), but normalising it by mean sentence length
collapses it to nothing (mean −0.089, t=−1.10, 53%). Shortening sentences shrinks the
gaps between them arithmetically. What actually moves is mean sentence length:
−2.01 words, t=−4.36, 95% consistency.

| measure | mean Δ | t | consistency |
|---|---|---|---|
| d2 raw adjacent jump | −5.950 | −3.28 | 93% |
| d2 normalised by mean length | −0.089 | −1.10 | 53% |
| d1 sentence-length CV | −0.028 | −1.42 | 42% |
| **mean sentence length** | **−2.012** | **−4.36** | **95%** |

## What this means for the plan

`plans/2026-08-05_cadence-displacement-implementation.md` §2.1 proposed sentence-length
*variation* as the core cadence signal, on the reasoning that human prose is burstier
than machine prose and that burstiness carries prosody. **That is not what the corpus
shows.** Variation is flat — 42% consistency, indistinguishable from noise. Length
itself is what moves, consistently, in every story measured.

The tricolon hypothesis also does not survive. jhave's edits neither add nor remove
three-item patterns once length is controlled for.

The direction of correction, stated from the data rather than from the hypothesis:

> **shorter sentences · fewer em-dashes · no naming clauses · less figuration**

Prosodic variation is not part of it. Three of the six proposed dimensions are live,
one is null, and two were measuring the same underlying shortening.
