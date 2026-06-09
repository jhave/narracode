# v3 — Loop Notes

## Prompter's request (verbatim, this loop)

> switch to branch smorky-origin-episode-N5Lff And I'd like to non-destructively allow. sonnet 4.6 to do a compositional pass over the entire set learning from the first zero out of the box episode. keeping the the sort of succinctness of the entire structure so that there's no need to make any self-referential commentary about objects of the room. internal thoughts are always put into the thought bubbles and really we're seeking some sort of like something that is startlingly funny at a very profound, articulate honest level. this looks at into relationships between people who who in this case are one is a robot chatbot and another is a tattoo artist but both of them are in a sense people who are different and that difference like as in the odd couple or Mork& Mindy or I dream of Jeannie, becomes the origin of a kind of friction that is ultimately resolved in a sweet and comic way. not too sweet. not too comic but just enough to make it clear. and if we're going to eventually have a romantic tension, it has to be clear somehow that the tattoo artist Cinder is female identifying as non-binary and the ro-bot Smorky is non-binary identifying physiologically as male. Part of this can be about like just the atypical queer culture. it's not like a rom-com with a marriage or a princess at the end. this is like much more edgy kind of microalienated but not brutal or violent in any way. this is just you know beings that are quirky.

## What this snapshot preserves

The **post-Gemini-edit, pre-Sonnet-pass** state. Between v2 and here, the prompter edited the drafts (with Gemini Flash 3.5) — commits `fb5e376`, `9c97768`, `7dcc147`, `36117b6` — most heavily on Episode 0, which they sharpened into the **gold-standard exemplar**: concrete and filmable, un-filmable commentary scrubbed, the heretical-tableau pause trimmed to pure action, the on-the-nose "Companion Diary" ending replaced with an oblique beat (Smorky trying out the cat's name in the dark), the room richly specified (welcome-to-hell doormat, walkup hallway, baby-blanket cat shelf). Eps 1–4 left largely as the Opus drafts.

## Edit observations (Gemini Flash 3.5 pass, diffed against v2)

The prompter's edits teach a consistent register:
- **Concrete over commentary.** Every gloss about what an object *means* was cut; objects are shown and left to act.
- **Restraint on bubbles and early intimacy.** Excess thought-bubbles and "early intimacy dialogue" were removed (commit `36117b6`).
- **Oblique endings.** The thesis-button tag is retired in favor of a small, strange, deflecting final beat.
- **Pure filmability.** Stage directions reduced to what a camera receives.
These are now encoded as commitments in POETICS (Form & format; the thought-bubble device; the tag note).

## This loop's action

1. `on_new_direction`: updated POETICS + structural for the **new gender configuration** — Cinders female-bodied & non-binary (she/they, narration leans they/them); Smorky reads male & non-binary (he/they); the attraction is **queer/atypical, edgy, micro-alienated, never rom-com**.
2. Ran a **non-destructive Sonnet 4.6 compositional pass** over all five episodes (five parallel agents), learning from the edited Episode 0, writing to `drafts/sonnet-pass/`. Canonical `drafts/` untouched.
3. Opus review in `critiques/sonnet-pass-check-2026-05-29.md`.

The diff target for the next snapshot is whichever version the prompter merges from `drafts/sonnet-pass/`.
