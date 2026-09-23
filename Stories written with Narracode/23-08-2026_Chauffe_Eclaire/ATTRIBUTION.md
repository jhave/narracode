# ATTRIBUTION

## Header image — 2026-09-23

At Jhave's request, GPT-6 in the local Codex desktop app directed a panoramic header through the built-in image_gen tool and added it to both HTML pages. The threshold, radiator and overnight bag extend the ordinary domestic setting of the section images. The final header is `img/header-no-fixed-arrangement.png`; its exact prompt, dimensions and hash are recorded under `header` in `visuals/generated-image-prompts.json`. The image model's version was not exposed. The illustrated edition now contains nine generated images: one header and eight section images.

## Illustrated edition and title — 2026-09-23

**Jhave (David Jhave Johnston)** — requested subtle, weird, niche, ordinary and occasionally raunchy images; requested their insertion into the story index; accepted **Chauffé, éclairé** / *No fixed arrangement.* as the title and subtitle.

**GPT-6, acting as Codex in the local Codex desktop app** — proposed the accepted title pairing; directed and inspected eight image generations; integrated them into the draft-15 reading edition and the four-chapter story index; preserved chapter-one prose and the later chapters; updated page metadata, image alternative text and prompt folds.

**Built-in image_gen tool** — generated eight original photographic illustrations. The image tool did not expose its underlying model version; no model name is inferred. Exact final prompts, the chair-orientation edit, image filenames and SHA-256 hashes are recorded in `visuals/generated-image-prompts.json`. Final assets are in `img/chapter-one/`. A courtyard version was rejected by the image tool; the final version uses a fully clothed neighbour and toast on borrowed bedding. Generated images are fictional illustrations, not documentary photographs.

The contributions below preserve the earlier stages, including the initial proposal-only reading edition.

## Reading edition and image proposals — 2026-09-23

**GPT-6, acting as Codex in the Codex desktop app (local session)** — fetched draft 15 from `claude/gifted-noether-qxuu13`, preserved the source bytes and commit provenance, prepared eight proposed images and a standalone HTML reading edition. No story prose was revised; images are proposals, not generated artwork. The executing model is exposed to this session as GPT-6, with no more specific suffix available.

## Imported attribution — draft 15

The following contribution record accompanies the remote draft at commit `28ba5d1789b5bec27c688b30a3ecfe42880dc75b` and is reproduced as recorded there:

## Revision contribution — 2026-09-23, human cadence

**Jhave (David Jhave Johnston)** — direction to revise draft 14 toward human cadence within the current poetics.

**Claude Opus 5.5, in Claude Code (remote session)** — snapshot `versions/v3-2026-09-23-before-human-cadence/`; wrote `drafts/15-chapter-one-human-cadence.md`; post-draft check and tell-scan; poetics amendment; state update; saved prompt. Single model, no subagents.

## Revision contribution — 2026-09-23

**Jhave (David Jhave Johnston)** — diagnosis of the repetitive clipped cadence and numerical accounting; direction toward an abrupt, raw, sensually attentive narrator whose appetite, boredom and unspoken trauma exert pressure without explanation. Authorized the snapshot, poetics revision, new draft and preservation of the prompt for a later index fold.

**GPT-6, acting as Codex in the Codex desktop app** — consulted the draft history; preserved all thirteen existing drafts and supporting records in version 2; synchronized working state; amended the poetics and voice-engine authority; wrote the alternative chapter-one draft `14-chapter-one-rhythm-rewrite.md`; saved the human prompt. The executing model is identified to this session as GPT-6; a more specific deployment suffix is not exposed, and none is inferred. No other model or subagent participated in this revision.

The new composition follows the human's stated qualities and this project's characters and situations. No external literary text was retrieved or used for sentence imitation in this pass. This contribution is to the working files; the existing story index has not been republished. Earlier credits below are preserved as recorded and are not independently reverified here. The historical word count below refers to the original chapter-one version.

---

## Original record

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
