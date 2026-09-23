# ATTRIBUTION

**Story:** Chauffé Éclairé
**Date:** 2026-08-23

## Human

**Jhave (David Jhave Johnston)** — direction, register specification, the source constraint
(Lynne Tillman's *Weird Fucks* as prosodic guide), the Montreal 2028 relocation brief, the
socioeconomic instruction, and the challenge that produced the voice engine.

## AI

**Claude Opus 5** — all harness roles: Initiator, Structural, Compositional, Reflexive.
Also authored `tools/tillman_check.py` and `reference/voice-engine.md`.

### Note on the AUTO_MODE model table

`narracode.md` → AUTO_MODE → *Model roles* assigns Initiator/Reflexive to Opus 4.7 and
Composition to Sonnet 4.6. That table is stale; those models were not available to this
run. The attribution norm ("every AI model credited by its exact model name, never a
generic vendor name") takes precedence over the table, so the record is exact: **a single
model, Claude Opus 5, performed every pass.** The role *separation* was preserved — passes
were run in sequence as distinct operations, with the validator interposed between
composition and revision — but the model asymmetry the table specifies did not occur, and
the critique should be read knowing that the critic and the composer were the same model.

## Source relationship — declared

*Weird Fucks* is the prosodic reference, named by the prompter. **No text by Lynne Tillman
appears in this story.** No character, incident, setting, or sentence of hers is
transposed. The prompter supplied one quoted phrase as a target specification; that phrase
appears nowhere in the draft, and the operation it demonstrates was rebuilt from first
principles in `reference/voice-engine.md` §3 and executed in our own nouns.

What was taken is measurable and structural: sentence-length distribution, figuration rate,
the semicolon hinge, episodic sectioning, affective flatness at the turn. Those properties
are enforced by `tools/tillman_check.py`, which contains no source material either — only
thresholds.

## Word count

1,430
