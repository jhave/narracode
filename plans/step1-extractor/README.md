# Step 1 — the extractor: substep guides

*2026-08-05. Six briefs, one per substep. Each is written to be handed to an agent as its working instruction.*

---

## Correction to the 08-05 plan

`plans/2026-08-05_cadence-displacement-implementation.md` §0 states that provenance is encoded in version directory names and the extractor can be fully automatic. **That was based on `Interim Edge` alone and is wrong across the corpus.** A survey of all version trees found:

| pattern | example | provenance |
|---|---|---|
| explicit human marker | `v3-2026-07-20-human-edit-pass`, `v0-2026-06-20-user-edits`, `v3-2026-07-30-jhave-section1` | **readable** |
| content-named only | `v2-kitchen`, `v1-2026-05-11-the-magnet`, `v0-2026-05-08-pre-geography-shift` | **unknown** |
| ambiguous temporal | `v2-2026-06-08-before-human-style-propagation` | **unknown — is the edit in this snapshot or the next?** |
| bare numbered | `v0`, `v1` in `Project_A-0` | **not snapshots** — contain only `edit-observations.md` and `loop-notes.md`, no `drafts/` |
| loose files | `1-glistening_2026-07-26_backup.md` in `versions/` | **not snapshots** — backup files, not directories |

Roughly half the corpus is auto-labellable. The other half needs a manual provenance pass — bounded at about 40 decisions, each of which jhave can answer in seconds. That is substep 1.2 and it is unavoidable.

**Do not let an agent guess provenance from content-named directories.** A wrong label silently inverts a displacement vector, and Step 2's entire result is the average of those vectors.

---

## Model recommendation

The extractor makes **no model calls at runtime**. It is diffing and counting. The question is only which model *writes* it.

| substep | task character | model |
|---|---|---|
| 1.1 corpus survey | reading messy real data; must report inconsistency rather than a clean answer | **Opus 4.6** |
| 1.1b git-history extraction | recovers pairs from in-place edits invisible to 1.1 | **Opus 4.6** |
| 1.2 provenance ledger | ambiguous cases, needs jhave in the loop | **Opus 4.6** |
| 1.3 sentence segmentation | literary prose — fragments, dialogue, ellipses break standard tokenizers | **Opus 4.6** |
| 1.4 alignment | mechanical once the spec is pinned | **Sonnet 4.6** |
| 1.5 schema and emit | purely mechanical | **Sonnet 4.6** |
| 1.6 validation | must not report a pass it did not verify | **Opus 4.6** |

**Why Opus for 1.1, 1.2 and 1.6 specifically.** The risk in this step is not that the code is hard — it is ~150 lines of standard library. The risk is *silent wrong answers on messy data*: an agent that reports "extracted 847 pairs" without noticing that 300 of them came from machine-to-machine transitions. This corpus is the foundation for Steps 2 through 5. Errors here do not surface as crashes; they surface as a displacement vector that points nowhere, at which point Step 2's falsification test returns a false negative and the whole line of work is abandoned for the wrong reason.

Use the cheaper model for 1.4 and 1.5, where the spec is already exact and errors are loud.

---

## Order

1.1 → 1.1b → 1.2 → 1.3 → 1.4 → 1.5 → 1.6

1.1 and 1.2 must complete before any code is written. 1.3 can proceed in parallel with 1.2.
1.1b runs after 1.1 and can proceed in parallel with 1.2.

**`versions/` is not the only source.** Early stories were edited in place and committed,
so their machine state exists only as a git parent commit. `26-06-2026_The_First_Water_Molecule`
yields 0 pairs from snapshots and 174 from git. See 1.1b.

---

## Standing instructions for every substep

These apply to all six briefs and are repeated in each.

1. **Report counts you actually computed.** Never estimate a number and present it as measured. If you did not run it, say so.
2. **Do not skip files silently.** Every file that errors, is empty, or does not match an expected pattern goes in an explicit exceptions list in the output.
3. **Do not infer provenance from prose style.** Only from the ledger (1.2) or an explicit name marker.
4. **Prefer dropping a pair to guessing one.** A missing pair costs one sample. A wrong pair corrupts the mean.
5. **State assumptions as assumptions.** If you assumed `drafts/*.md` is the only draft location, write that down where it can be checked.
6. **If the acceptance criteria are not met, say so plainly.** Do not report partial completion as completion.
