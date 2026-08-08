# Step 2 — displacement test

`tools/step2_displacement.py` · cadence 1.0.0
## VERDICT: **PROCEED**

Document-level dimensions with a consistent direction: d1_mean_sent_len, d3_figuration, d6_emdash, d7_lexical_rarity.

Pair-level: d3_figuration, d5_naming, d6_emdash, d7_lexical_rarity.


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
| d7_lexical_rarity | 20 | -0.1566 | 0.1621 | -4.32*** | 95% |
| word count | 20 | -123.4000 | 200.2529 | -2.76** | 72% |

## Pair level

689 pairs with text on both sides. d1 and d2 are omitted: 951 of 954 before-spans are a single sentence, so a length series does not exist.

| dimension | n | mean Δ | sd | t | consistency |
|---|---|---|---|---|---|
| d3_figuration | 689 | -0.0160 | 0.1467 | -2.86** | 87% |
| d4_tricolon | 689 | +0.0015 | 0.2876 | +0.13 | 51% |
| d5_naming | 689 | -0.0160 | 0.1364 | -3.07*** | 100% |
| d6_emdash | 689 | -0.0639 | 0.2931 | -5.72*** | 97% |
| d7_lexical_rarity | 689 | -0.3176 | 0.5433 | -15.34*** | 78% |
| word count | 689 | -3.6009 | 9.1052 | -10.38*** | 65% |

## Does the direction hold across stories?

Mean displacement per story, document level. Agreement matters more than magnitude: a direction that reverses between projects is not a direction.

| story | d1 mean sent len | d2 len cv | d3 figuration | d4 tricolon | d5 naming | d6 emdash | d7 lexical rarity | n |
|---|---|---|---|---|---|---|---|---|
| 12-06-2026_Post_Everything | -0.068 | +0.005 | +0.000 | +0.000 | +0.000 | +0.000 | -0.030 | 2 |
| 15-06-2026_TheCompulsionLoop | -0.330 | -0.100 | -1.000 | +0.000 | +0.000 | +0.000 | -0.055 | 1 |
| 25-06-2026_Crepuscular | -1.419 | -0.028 | -0.800 | +0.400 | -0.300 | -4.300 | -0.158 | 10 |
| 26-06-2026_The_First_Water_Molecul | -4.247 | -0.032 | -0.333 | +1.333 | -0.333 | -3.333 | -0.239 | 6 |
| 30-07-2026_Interim_Edge | -0.100 | +0.007 | +0.000 | +0.000 | +0.000 | +0.000 | -0.004 | 1 |

