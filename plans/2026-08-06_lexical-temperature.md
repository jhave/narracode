# Lexical temperature: can it be measured retroactively?

*2026-08-06. In answer to jhave's question — is it possible to assess the temperature
of already-written text, machine draft versus human edit?*

---

## The literal answer is no

Sampling temperature is a parameter of the token distribution at generation time. It
cannot be inverted from a finished text: many combinations of temperature, prompt and
model produce the same output. And jhave's edits were never sampled at all — a human
revising a sentence has no temperature.

## The useful answer is yes, via a proxy

What temperature *does* is shift probability mass toward less likely tokens. That
effect is measurable after the fact, in two ways:

1. **Token surprisal** — average `−log P(token | context)` under a reference model.
   The direct measure. Requires log-probabilities, which the Anthropic API does not
   expose. Would need a local model or an API that returns logprobs.
2. **Lexical rarity** — how improbable the *word choices* are, from corpus frequency
   data. No model needed, and it turns out to be enough.

This document reports (2), measured on the full corpus using Zipf frequencies
(`wordfreq`). Zipf 7 is `the`; 4 is an ordinary word; 2 is rare; 0 means absent from
the frequency list entirely.

## Result

**jhave edits toward rarer words, and it is the strongest signal in the project.**

| measure | value |
|---|---|
| mean Zipf, words he removes | 5.884 |
| mean Zipf, words he adds | 4.905 |
| difference | **−0.979** — roughly ten times less frequent |
| per-pair change | mean −1.141, **t = −18.60**, n = 470 |
| pairs moving toward rarer words | **84.5%** |
| added words absent from the frequency list | **2.73%** vs 0.13% removed |

For comparison, the strongest of the four measures from Step 2 was em-dash count at
t = −5.72. This is three times that.

### Controlled

The obvious confound is that shortening deletes function words, which are common, so
mean rarity of removals would rise mechanically. Restricting to strict one-for-one
word substitutions inside high-confidence pairs, where the alignment is reliable:

| | |
|---|---|
| n | 150 |
| mean Zipf change | **−1.281** |
| t | **−9.07** |
| toward rarer | **80.7%** |

The effect strengthens under control rather than weakening. A first pass without the
confidence filter produced some nonsense pairs (`hold → fake`) from word-level
alignment inside dissimilar sentences; filtering to confidence ≥ 0.75 removes them.

### What the substitutions actually look like

```
held         -> crushed            5.24 -> 4.03
junk         -> spunk              4.03 -> 2.66
their        -> craw               6.33 -> 2.38
already      -> hastily            5.55 -> 3.30
workable     -> tractable          3.12 -> 2.21
small        -> tight              5.51 -> 4.57
the          -> prismatic          7.73 -> 2.75
engagement   -> trend-gagement     4.31 -> 0.00
exploitation -> maxploitation      3.84 -> 0.00
```

The last two are coinages. Not rare words — words that do not exist. This is why the
proportion of added tokens at Zipf 0 rises twenty-fold.

## Why this matters more than the measurement itself

Step 2 concluded that the four live measures explained 9% of edits and that the other
91% was texture no detector could see. Lexical rarity sees a large part of it:

| explains | share of pairs |
|---|---|
| the four Step 2 measures | 9.0% |
| lexical-rarity shift (|ΔZipf| ≥ 0.5) | **50.9%** |
| either | **54.0%** |
| still unexplained | 46.0% |

**Coverage goes from 9% to 54%.** The 91% residual was not entirely untheorisable; it
was substantially one thing that had not been measured, because every dimension in the
original vector was structural or punctuational and none looked at word choice.

## The revised description of the direction

Step 2's four measures plus this one:

> **shorter · rarer · fewer em-dashes · no naming clauses · less figuration**

Compression and rarefaction together. Fewer words, each one less probable. That is a
coherent operation and it has a name in the terms of the original question: jhave edits
at a **higher effective temperature than the model generates at**, while simultaneously
cutting length.

This also reframes the em-dash and naming-clause findings. Those are the machine's
high-probability connective habits. Removing them and substituting rarer content words
are the same move seen from two sides: away from the probable.

## Consequences

1. **Add rarity as the fifth live measure.** It is stronger than the other four
   combined and it is content-independent, so it works for the Step 3 evaluation.
2. **Do not use it as a generation target.** Instructing a model to "use rarer words"
   produces thesaurus prose. The measure is diagnostic; the corpus is what transmits
   the discrimination between `craw` and an arbitrary rare synonym.
3. **It strengthens the case for retrieval.** Exemplars carry which rare word, not
   merely that rarity is wanted. That distinction is the whole difficulty and no rule
   states it.
4. **Worth doing next: true surprisal.** Zipf frequency is context-free — it does not
   know that `craw` is surprising *there*. A model that returns logprobs would measure
   surprisal in context and would likely account for more of the remaining 46%. This
   needs either a local model or an API exposing logprobs.

## Honest limits

- Zipf frequency is context-free and lemma-blind; inflection shifts (`analyze` →
  `analyzing`) register as near-zero change though they are real edits.
- The 46% still unexplained includes syntax, punctuation-only changes such as a full
  stop becoming a question mark, and reordering.
- Rarity is a property of the lexicon, not of whether the word is *right*. It measures
  the direction of the reach, not its success.
