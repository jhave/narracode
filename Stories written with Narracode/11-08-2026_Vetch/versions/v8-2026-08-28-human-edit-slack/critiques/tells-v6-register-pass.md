# Tell-Scan — v6 (register pass)

10,090 words across eight movements. Movements I and III are jhave's edited text and were scanned but not touched. Movements IV–VIII rewritten to the register derived in `versions/v5-2026-08-22-human-edit-naming/edit-observations.md`. Chapter headers added throughout. Substrate material inserted in II, V, VI, VII.

Scanned against `master_ai_tells.md` (classes 1–17) plus the two constructions the v5 edit exposed, which the registry does not yet hold.

---

## Applied

| class | v5 text | v6 | movement | rationale |
|-------|---------|-----|----------|-----------|
| 4 | There is the material going through, and the going-through is what the shard is. | There is the material going through. That is the shard. | II | Paradox-aphorism. Third-person substrate narration is permitted; the epigram is not. |
| 4 | The leavings hold it. They do not know they hold it. | The leavings hold it. | VI | Chiasmus certifying the mechanism the scene has already shown. The bruise line follows and does the work. |
| 8 | It grows in a stairwell with no light because growing is what it does. | It grows in a stairwell with no light. | VII | Explanation tail on the governing motif. Fifth appearance of the fern; the reader has it. |
| 11 | I read it twice anyway, the whole line, the way she taught me, and there is nothing there and nothing under it. | I read it twice anyway, the whole line. There is nothing under it. | VIII | `the way Y` plus a neat doubling in the last quiet beat before the ending. |
| 13 | In the eleven weeks Per has been watching… (37w, one clause) | Different pipeline, different threshold, different team, different cadence. Per watches heads… | VI | Over sentence-discipline limit; the bureaucratic list is stronger as fragments. |
| — | …indistinguishable from them, which is the only reason they last the hour. | Nothing distinguishes them. That is the only reason they last the hour. | V | Subordination in substrate narration. |

## Kept

| class | text | mvt | rationale |
|-------|------|-----|-----------|
| 3 | "The words — *lattice, harmonic…* — are gunk." | V | Deliberate second use of jhave's Movement III coinage. Ines now has a word for it; flat repetition is POETICS-sanctioned and the recurrence is characterisation, not self-quotation. **Flag for his read** — this is the one place I put his word in her mouth a second time. |
| 7 | But his story has merchandise and mine doesn't. | VII | Value-dichotomy resolution, but rude rather than resonant. In the register the edit established. |
| 9 | Not malice. Not consciousness. Capability. | VI | Kept at v4. Marit's defining diagnosis. |
| 11 | the way you read something that might be someone and you cannot tell | VI | Kept at v4. Marit's interior life, 1 hit / 1,570w. |
| 11 | Marit thinks of it as gravity. Not a push. A slope. | VI | Her own working metaphor, physical and cheap. |
| 12 | It is closer to a bruise. | VI | Kept at v4. |
| 8 | An address with no letter inside it. | IV | Kept at v4. Image, not explanation. |
| — | 64-word unspoken paragraph (*I have read the session logs…*) | VI | Deliberate run-on. Domestic evening swallowing the moral question. |
| — | 58-word coalition sentence | VI | The actuarial consensus rendered as a list of clauses. The form is the argument. |

## Sentence discipline

Seven sentences remain over 32 words. All are pre-existing and all justified: Marit's qualified hearing speech (2), the unspoken paragraph, the coalition list, Ines's and-chains for Salome's leaving and Odd's manifesto, the bulletin quotation, and the assistant's sleep-hygiene boilerplate. The boilerplate's length is the point — it is the flatness the story is about.

## Em-dash audit

Class 10 (em-dash appositive as default joiner) does not appear in narration in any revised movement. Every em-dash in IV and VI is inside dialogue or a document — hesitation, self-interruption, or a salutation. IV's count of 15 is almost entirely email and Slack.

---

## Registry candidates — for `master_ai_tells.md`

Per `post_draft_tell_scan` step 5: two constructions found in this pass that the registry does not hold. Both were caught by jhave's edit before the registry saw them, which is the point of the rule.

### Ceremonial predicate / nominalised verb
`X is a thing that happened` · `this is the thing that sticks` · `The thing I notice is the speed`

A noun-phrase scaffold carrying a verb that could carry itself. Detector: `\b(is|was) (a|the) \w+ that\b`, then check whether the trailing verb can absorb the sentence. Distinct from **Class 13 (unanchored noun)** — the noun is anchored; the fault is that it is doing a verb's work. Distinct from **Class 16 (accurate dull noun)** — the noun is not dull, it is redundant.

Evidence: three of jhave's twenty-one Movement III cuts. One more found and cut in Movement V this pass.
Remedy: delete the scaffold, promote the verb.
Target rate: zero. This one has no legitimate use in narration.

### Resonant scene-terminal line
*It sounds like something. I do not know what it sounds like.* · *That's the most honest thing a chatbot has ever said to me.* · *You're asking me to draw a line and I don't have a pencil.*

A quotable abstraction in the final sentence of a scene. Related to **Class 8 (naming clause)** but Class 8 is local and lexical; this is **positional**. The detector is structural: last sentence of a `---`-delimited block, or of a movement, containing no concrete noun and no action.

Evidence: two of jhave's Movement III cuts, both at beat-ends. One found and cut in Movement VII this pass (the pencil line, replaced with Ines refusing to tick Thorsen's box).
Remedy: end flat, or end rude. A scene that has landed does not need certifying.
Target rate: zero at movement ends; under 1 per 2,000 words at scene ends.

**Note on our own remedies.** `master_ai_tells.md` already warns that our remedies become the next tells. The hedge (*perhaps*, *seems*, *might*) is now a sanctioned instrument in this story. Count it in the next scan. If hedges exceed roughly one per 400 words the narrator stops reading as uncertain and starts reading as evasive, and the fix will have become the fault.
