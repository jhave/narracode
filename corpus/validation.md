# Corpus validation — substep 1.6

`tools/validate_corpus.py`, seed 20260806. **1234 pairs.**
## VERDICT: **PASS**


## E0 — snapshot ordering

`v0` sorts first and `v10` after `v9` in every story: **PASS**

## A — verbatim check on a stratified sample

Each `before` must appear in its source document and each `after` in the target. Split/join/reorder pairs join or move text, so they are checked token-wise rather than as a contiguous string.

| stratum | id | op | conf | before found | after found |
|---|---|---|---|---|---|
| high (>=0.8) | `6fe2531b6a` | substitute | 0.93 | yes | yes |
| high (>=0.8) | `6982af9b76` | substitute | 0.94 | yes | yes |
| high (>=0.8) | `1ab8d840c3` | lengthen | 0.88 | yes | yes |
| high (>=0.8) | `87558918a5` | lengthen | 0.82 | yes | yes |
| high (>=0.8) | `ffea39387b` | shorten | 0.93 | yes | yes |
| high (>=0.8) | `09e1b5d806` | substitute | 0.96 | yes | yes |
| high (>=0.8) | `39611ed2aa` | substitute | 0.83 | yes | yes |
| high (>=0.8) | `447388f704` | shorten | 0.8 | yes | yes |
| high (>=0.8) | `b967f3da6a` | substitute | 0.99 | yes | yes |
| high (>=0.8) | `83f5a95799` | lengthen | 0.81 | yes | yes |
| mid (0.5-0.8) | `8c7a202b5f` | lengthen | 0.58 | yes | yes |
| mid (0.5-0.8) | `084339b525` | shorten | 0.6 | yes | yes |
| mid (0.5-0.8) | `d11cba48a6` | shorten | 0.64 | yes | yes |
| mid (0.5-0.8) | `0d8375c450` | shorten | 0.76 | yes | yes |
| mid (0.5-0.8) | `e3005760e6` | shorten | 0.57 | yes | yes |
| mid (0.5-0.8) | `4ce9d6b829` | shorten | 0.55 | yes | yes |
| mid (0.5-0.8) | `e8a6af2e8f` | shorten | 0.79 | yes | yes |
| mid (0.5-0.8) | `7520c37224` | lengthen | 0.58 | yes | yes |
| mid (0.5-0.8) | `02296c4d07` | shorten | 0.68 | yes | yes |
| mid (0.5-0.8) | `9fc69ad6ab` | shorten | 0.67 | yes | yes |
| low (0.3-0.5) | `fa7ccc9967` | substitute | 0.48 | yes | yes |
| low (0.3-0.5) | `09dd213115` | shorten | 0.48 | yes | yes |
| low (0.3-0.5) | `88a327f536` | shorten | 0.42 | yes | yes |
| low (0.3-0.5) | `b8167b13ff` | shorten | 0.4 | yes | yes |
| low (0.3-0.5) | `3bf8a7221b` | lengthen | 0.41 | yes | yes |
| low (0.3-0.5) | `d4a5f3ca4b` | shorten | 0.43 | yes | yes |
| low (0.3-0.5) | `41c443f364` | shorten | 0.47 | yes | yes |
| low (0.3-0.5) | `6f40e6287d` | shorten | 0.48 | yes | yes |
| low (0.3-0.5) | `ec2ce6a5d6` | substitute | 0.45 | yes | yes |
| low (0.3-0.5) | `6df87468a6` | shorten | 0.44 | yes | yes |

**30 of 30 verified.**

## B — reproduce documented measurements

| measurement | documented | computed | verdict |
|---|---|---|---|
| Interim Edge v2→v3 operations | ~13 | 32 | PASS |
| em-dash /1k, v1 | 5.6 | 7.7 | **FAIL** |
| em-dash /1k, v4 | 3.7 | 6.0 | **FAIL** |
| `the way X` /1k, v1 | 1.3 | 1.2 | PASS |
| `the way X` /1k, v4 | 0.2 | 0.2 | PASS |

### Note on the em-dash rows

The `the way X` rates reproduce exactly (1.2 vs 1.3; 0.2 vs 0.2). The em-dash rates
do not, in either direction, and the word counts do not match either: the benchmark
doc reports 5,555 and 5,171 words for v1 and v4 of `7-condensed-final.md`, this tree
holds 5,853 and 5,469. The drafts changed after the measurement was taken, so the
documented em-dash figures cannot be reproduced from the current files.

This does not affect the corpus. It does affect benchmark plan §7.3, which proposes
anchoring registry target rates on these measurements — those rates need re-measuring
against the files as they now stand, and the measurement should record the commit it
was taken at.

## C — registry spans

| span | class | in corpus | explanation |
|---|---|---|---|
| `Two minutes forty` | class 2 number-plus-comment | no | removed in `v1-2026-07-30-automode-first-pass` &rarr; `v2-2026-07-30-tell-scan`, which is **machine &rarr; machine** — not a human edit, so correctly absent |
| `Counter` | class 13 unanchored noun | yes | — |
| `legume` | class 16 accurate dull noun | yes | — |
| `the way a seam is after strain` | class 11 analogy-simile | no | removed in `v3-2026-07-30-jhave-section1` &rarr; `v4-2026-07-30-register-rewrite`, which is **human &rarr; machine** — not a human edit, so correctly absent |
| `chest did something medical` | class 14 narrated emotion | yes | — |

**3 in corpus, 2 correctly absent and explained, 0 unexplained.**

Finding: two registry examples were cut by the model rather than by jhave — one in the tell-scan pass (machine to machine), one in the register rewrite (human to machine). The registry dates them to jhave's identification, but the text change itself is not a human edit, so it does not and should not appear as a pair.

## E — length symmetry

shorter 377, longer 201, ratio **1.88**.

A corpus of line edits should skew toward shortening. A skew toward lengthening would mean before and after are swapped, inverting every displacement vector in Step 2.

Verdict: **PASS**

## Integrity

- unique ids: 1234 of 1234 PASS
- both sides empty: 0 PASS
- identical after normalisation: 0 PASS
- segmenter versions: ['1.0.0']
- ops: {'insert': 280, 'lengthen': 151, 'substitute': 232, 'shorten': 294, 'delete': 265, 'split': 9, 'join': 3}

