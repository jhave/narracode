# Tell-scan — 4-chauffe-eclaire

*Span · class · remedy. Not applied. Accept or refuse line by line.*

"She said it the way you say a phone number." · **§11 analogy `the way you`** · CUT
→ **CUT in draft 4.** Initially kept as load-bearing. Reversed on the grounds that it was simultaneously a registry §11 tell *and* the third figure in a story capped at two per thousand words — one span failing two independent constraints is not load-bearing, it is a favourite. Replaced with a flat statement: *She did not have to think about it.* The line lost its polish and kept its meaning, which is the trade this register exists to make.

"as if something had been announced." · **§12 confident figure** · demote or CUT
→ **Kept.** The next sentence refuses it outright ("Nothing had been announced."), which is the §12 remedy executed in place rather than a violation of it. Refused-figure count for the story: 1. At cap.

"He cried without any noise, which is a skill." · **§5-adjacent, the appended verdict** · CUT "which is a skill"
→ **Kept.** It is the narrator's dryness, not the narration's wisdom. Distinguishable because it is unkind.

"Both of those were true and I have not worked out how." · **§8 naming clause, near-miss** · CUT
→ **Kept, flagged as the story's largest single risk.** It survives only because it names a failure to understand rather than an understanding. One word further toward insight and it becomes the machine-made summarizing line the register exists to prevent. A human edit pass should look hard at this sentence.

"It was always better cold." · **§3 clipped affect-verdict** · CUT?
→ **Kept.** The verdict is about food, not about the character's own emotional state, which is what §3 actually catalogues.

"a laugh that came late" · **§13 unanchored noun risk** · locate it
→ **Kept.** Adjacent to "hands you noticed," which anchors the sequence in the narrator's looking.

## Not found
No §1 object lexicon (no kettle, hum, shimmer, tapestry, testament). No §2 number-plus-comment — every number in the story stands bare, which was the hardest constraint to hold and the one most likely to have failed. No §4 paradox opener. No §6 corrective superiority. No §7 value-dichotomy landing. No §9 triadic escalation (one triad in §2 was broken into three sentences during revision for exactly this reason). No §10 em-dash default: zero em-dashes in the story.

## New candidate class — proposed for `master_ai_tells.md`

**The flat-register compensation aphorism.** In a deliberately flat, short-sentence voice, the model compensates for withheld affect by landing a section on a quiet universal ("...and I have not worked out how", "...which is a skill", "Sort of is most of it"). Individually these are the register working. Above roughly one per 500 words they become the same summarizing gesture the flatness was adopted to refuse — the naming clause (§8) wearing a shorter coat.

- **Detector:** section-final sentence containing a present-tense generalization or a copula with an abstract complement, in a text whose median sentence length is below 8.
- **Rate cap:** 1 per 500 words. *Measured here: 3 in 1,430 — at cap, not over.*
- **Provenance:** Claude Opus 5, self-scan, *Chauffé Éclairé*, 2026-08-23. Requires jhave's confirmation before promotion to the registry.


## Instrument gap found during this run

Draft 3 passed the figuration check at 1.40 per 1,000 while containing two similes the
detector could not see: *"It smelled like solvent"* and *"She said it like weather."* The
pattern list matched `like a` and `like the` and missed `like` followed by a bare noun.

Fixed in `tools/tillman_check.py` by adding a perception-verb pattern
(`said|smelled|tasted|looked|felt|sounded + like`), which is narrow enough not to fire on
*I like*. Re-run against draft 4: *smelled like solvent* was rewritten to *smelled of
solvent* (it was never a figure, only phrased as one), and *like weather* now shows in the
report and is kept deliberately.

**The general lesson, recorded because it will recur:** a validator that passes a draft is
evidence about the properties it measures and about nothing else. The first version of this
tool reported a clean figuration score for a text with 50% more figures than it counted.
Green is not proof; it is the absence of one particular kind of disproof.
