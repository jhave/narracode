# Architectural harness observations — 2026-05-14

Notes on what in `narracode.md` is doing real work during composition, what is bookkeeping, and what is missing. Written from inside the Aft of Nowhere project after three scenes drafted (1b, 2, 3).

## What earns its keep

1. **The `post_draft` silence.** The single most load-bearing rule in the harness. The default failure mode of a single-shot LLM is to follow a draft with a self-critique, which then defensively trains the next pass toward consensus. Forbidding the chain — "Stop. Do not run critique. Do not propose the next scene. Do not summarize what you just wrote." — is what keeps prose from collapsing toward median between scenes.

2. **POETICS.md, specifically the Refusals section.** The Commitments section (what the piece *is*) anchors voice. But the Refusals (what the piece *will not do*) is what actively narrows the move-space. "No neat revelation that explains the child," "no prophecy-child structure," "no sentimental rescue arc" — each refusal closes off the trained default and forces invention elsewhere. Negative constraints are more generative than positive ones. Worth weighting Refusals more heavily than Commitments in any future projects.

3. **history.md, specifically the "Said" section.** Useful when it captures *exact phrasings already on the page* rather than plot summary. "The child smells of three layered registers: fruit-wrapper glue, chalk dust, faintly civic soap" lets me reach for that specificity in a later scene without re-reading the draft. Generic summaries ("Vera meets the child") would not.

4. **The draft naming convention (`1`, `1b`, `2`).** Cheap, almost trivial, but it cost nothing to fork the opening into a parallel `1b`. No overwrite, no ambiguity. The user's edits to either version remain legible. Worth keeping.

5. **The pre/post hook framing itself.** Even when I do not formally invoke a hook, having the hooks named ("pre_draft," "post_draft," "on_snapshot") makes my own steps audible to me. The vocabulary is a self-discipline tool.

## What does not earn its keep, at least not yet

1. **scene-ledger.md.** Redundant with history.md once history.md is well-maintained. Two scenes in, the ledger was already paraphrasing the history file. Suggest letting it stay thin, or absorbing it into history.md under a "Scenes" heading.

2. **reader-state.md.** Premature in a single-author session. Reader-state in this mode is just the writer's intuition; externalising it as a file produces generic statements ("reader expects X").

3. **The formal pre_draft structural pass when state is simple.** At scenes 2 and 3, I already knew the state. Writing it into the files was bookkeeping, not orientation. Suggest: when the prior scene was drafted in the same session, skip the formal structural pass and rely on context. Only run it when returning after time away (which the `on_orient` hook already covers).

4. **The Reading-agent annotations of named-only references.** Useful for projects where the prompter has uploaded source texts. For an entirely original world like Aft, the named influences in POETICS function more as a voice palette than as sources to annotate. The annotations would just reproduce my training-data summaries.

## What might earn its keep, if added

1. **A "phrases already burned" list.** Specific to this kind of voice-driven project, a small file capturing motifs that have already done their work — "polite want," "civic fold," "small ceramic sigh" — so I can avoid recycling them past their freshness window. Different from history.md (which tracks plot/state) and from POETICS.md (which sets palette).

2. **An explicit "do not repeat this scene's moves" line at the end of each draft.** A tiny self-imposed constraint. E.g. after scene 2: "Do not restage the wristband category-failure exchange." Forces the next scene to invent rather than reach for a working trick.

3. **A sentence-rhythm target in POETICS.** The current POETICS specifies syntax goals ("long syntactic pressure broken by sudden contemporary deflation") but not measurement. A target — e.g. "at least one sentence per scene running longer than 80 words; at least one paragraph composed entirely of sentences under 8" — would let me check rhythm without subjective taste alone.

4. **A small note on what *kind* of memory is allowed in a given pass.** Vera's interiority is the central pressure of this story, and a hook that distinguishes "memory triggered by sense" from "memory delivered as exposition" would protect against the second drift. Could live in POETICS as a clause under Character logic.

## Meta-observation

The harness is more useful than I expected, but not for the reasons it advertises. It is sold as a structure for separating passes (read, draft, critique, reflect). In practice, the *separation* is less load-bearing than the *silences* — the post-pass refusal to chain, and the documented refusals in POETICS. The active discipline of the system is what it forbids, not what it organizes.

This is consistent with how prose actually improves: not through more passes, but through smaller move-spaces.
