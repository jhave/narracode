# Loop 2 — notes

## Prompter's request (verbatim)

> I'm gonna suggest we alter the harness to incl a "scan for AI tell pass" such as "Kettle. Two minutes forty, and he stood there for all of it." -- 2 tells: Kettles (disproportinately used by AI) and # plus comment sentence format. Suggested replacemnt with one word: "Counter" --- Next, cut: "Liked the panic." --- is this version committed and online? If so, it's quicker if i just edit the md and then re-commit the human-edit

## What changed

**Harness (repo-level, not project-level).**
- New file `master_ai_tells.md` — registry of line-level constructions that read as machine-authored. Eleven classes, each with span, remedy, and provenance. Sits alongside `master_poetics.MD` (what the voice is) and `master_phrases_to_avoid.md` (what got cut from *Dissolution*).
- `narracode.md`: Reflexive agent gains a fourth mode, **Tell-scan**. New hook `post_draft_tell_scan`, wired into the AUTO_MODE pipeline beside `post_draft_check` and added to the output contract. The hook requires that any construction the prompter names which the registry does not already hold gets **appended to the registry** — a scan that finds only known classes has learned nothing.

**Story.**
- §1 *Kettle.* → *Counter.* (class 1, overused object lexicon)
- §1 *Two minutes forty, and he stood there for all of it.* CUT (class 2, number-plus-comment)
- §1 *Liked the panic.* CUT (class 3, clipped affect-verdict)
- §6 consequence — the ending was a frame-return to the §1 kettle and carried both flagged spans. Reduced to *Then got up, and the water went from nothing to a hiss to that last rolling panic.* The frame now closes on the sound, not the object.
- `critiques/tells-7-condensed-final.md` — first run of the pass. 5 further hits proposed and unapplied; 4 flagged and kept as load-bearing.
- `index.html` rebuilt. 5,482 words.

## Edit observations (Seamless Edit)

First human edits on this project. Three spans, all in the first four sentences, all cutting in the same direction: **remove the object, keep the sound; remove the reaction, keep the description.** *Counter* over *kettle* leaves the appliance to be inferred from hiss and click — the reader assembles it. *Liked the panic* was the narration approving its own image.

The diagnosis he supplied is more valuable than the edits: he named the *class* both times rather than the instance ("kettles — disproportionately used by AI", "# plus comment sentence format"). That is what made a registry the right artefact rather than a longer phrases-to-avoid list.

Largest finding of the resulting scan, and not one he named: the `X, the way Y` analogy-simile at 7 hits per 5,500 words. Now class 11.

## Recommendation for POETICS

Hold. Three spans is not yet a pattern for this project's `POETICS.md` — the rules landed in the repo-level registry instead, where they apply across projects. Revisit after his md pass.

## Next

He edits `drafts/7-condensed-final.md` directly; `index.html` rebuilds from it via `build_page.py`. Final HTML touches deferred to a later iteration.
