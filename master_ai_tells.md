# Master AI Tells

A registry of line-level constructions that read as machine-authored to the human editor. Companion to `master_poetics.MD` (what the voice is) and `master_phrases_to_avoid.md` (what got cut from *Dissolution*). This file is what the **tell-scan pass** reads.

The distinction that matters: `master_phrases_to_avoid.md` catalogues *clauses that editorialize*. This file catalogues *constructions that betray the generator* — habits of diction and rhythm that are not wrong, exactly, and that a human ear registers as synthetic anyway.

---

## How the pass runs — contextual review (2026-09-07)

**Goal: the flexibility of human literary voice, without unchosen LLM tropes.** Read the active story’s `POETICS.md` and surrounding passage before judging a construction. A regex retrieves a candidate; it cannot establish authorship or literary failure.

For each consequential finding record: quoted span · class(es) · function in context · KEEP / CHANGE / UNCERTAIN · optional alternative and what it costs. Group overlapping classes rather than counting the same ending three times. Report repetition across a passage when relevant; do not flag every occurrence mechanically.

KEEP is a complete result. Preserve useful repetition, ornament, doubt, direct emotion, abstraction, sound-play, and intentional ambiguity. Current user direction and project poetics govern. All imperative remedies and numerical rates in the historical entries below are **dated editorial examples, not global instructions or quotas**. Zero rates do not override project intent. Simplicity is an available choice, not the destination of every revision.

Propose only changes motivated by this passage. A longer or more musical alternative can be appropriate. Do not invent telemetry, new facts, obligations, or motifs to make a sentence appear grounded. Religious language can belong to a secular character; an opening pronoun can delay recognition deliberately; numbers can express ritual, obsession, miscounting, or comic precision.

Write findings to `critiques/tells-[draft-name].md`. The scan recommends; it does not apply edits or certify text as human. No detector score, rarity measure, or sentence-length target governs composition.

---

## Registry

### 1. Overused object lexicon
Nouns that appear in machine prose at a rate far above their rate in the world. The object is doing atmospheric work the writer has not earned.

- **Flagged**: `kettle` · `hum` / `humming` · `shimmer` · `tapestry` · `testament` · `weight of it` · `the air itself`
- **Example**: *Kettle. Two minutes forty, and he stood there for all of it.*
- **Remedy**: name the surface, not the appliance; let the sound imply the object. → *Counter.*
- **Provenance**: jhave, 2026-07-30, on *Interim Edge* §1.

### 2. Number-plus-comment
A measurement followed by a clause telling you how to feel about the measurement. The number is doing specificity; the comment then undoes it by supplying the reaction.

- **Example**: *Two minutes forty, and he stood there for all of it.*
- **Remedy**: keep the number or keep the comment. Never both.
- **Provenance**: jhave, 2026-07-30, on *Interim Edge* §1. Recurs across that draft — *Four minutes an item, measured.* / *Eleven minutes.* / *Forty-one seconds.* — where the bare number survives and the comment does not.

### 3. Clipped affect-verdict
Subject-dropped past-tense sentence reporting the character's approval of what was just described. Reads as compression; functions as explanation.

- **Example**: *Liked the panic.*
- **Remedy**: CUT. The description already did it.
- **Provenance**: jhave, 2026-07-30, on *Interim Edge* §1.

### 4. Paradox-aphorism / chiasmus opener
*The temptation is the only thing that is first.* *The end of me is the part I do best.* Seems like a nice touch; sits in a low-loss region of latent space.

- **Remedy**: let a plain sentence open. CUT the inversion.
- **Provenance**: jhave, on earlier projects. Recorded in memory and in `master_poetics.MD`.

### 5. The reductive `which is only X`
*…the queue, which is only a way of waiting.* A frame that shrinks the thing it names in order to sound wise.

- **Remedy**: CUT the clause; keep the noun.

### 6. Corrective-superiority stance
Narration lecturing an implied crowd — *the storytellers*, *everyone assumes*, *what people get wrong*. Distinct from a **character** being scathing, which is allowed and good.

- **Remedy**: replace correction with inclusion. Gather instead of rank.

### 7. Value-dichotomy resolution
Better/worse, right/wrong, true/false offered as a landing. Dissonance treated as an error to resolve rather than a phase.

- **Remedy**: both/and. Let the two stand.

### 8. The naming clause
Narration stating the mechanism it has just dramatized. *…and this was love, conducted through logistics, and it worked.*

- **Remedy**: CUT to the image. Keep *machinery he grew up inside; he could hear every gear.*
- **Provenance**: the whole of `master_phrases_to_avoid.md` is this class at scale.

### 9. Triadic escalation
Three-item list where the third item is the designed surprise. *Coffee, rent, the slow collapse of the century.*

- **Remedy**: two items, or four. Break the cadence.

### 10. Em-dash appositive as default joiner
Not banned — a low rate is native to this voice. Flag only when it becomes the *only* way clauses meet across a page.

- **Remedy**: convert one in three to a full stop or a comma.

### 11. Analogy-simile `X, the way Y`
Explaining a thing by analogy to a universal *you* or a generic case. *…four and a diagonal, the way you count in a cell.* *Not blank the way a draft is blank.* Individually good; collectively a signature. Becomes the default figurative move and the prose starts teaching rather than showing.

- **Historical threshold (advisory only)**: more than two per 2,000 words. Below that it is a habit; above it, a tell.
- **Remedy**: keep the two strongest, CUT the rest. Prefer stark, unadorned physical facts over decorative vehicle descriptions.
  - *hold the way a body holds its organs* → *inside an apparatus running silently behind the studs.*
  - *The way he listens to a car he is about to be told is fine* → *He listens to it until the bearing settles.* (CUT the trailing decorative simile sentence entirely).
  - *fills the horseshoe the way his bad mood fills the bay on eleven* → *fills the horseshoe wall to wall, chairs creak and people pull elbows in.*
  - *reads it the way you read a crack in a wall* → *touches the glass with a thumbnail, checking the crack.*
- **Provenance**: found by the first tell-scan, *Interim Edge*, 2026-07-30 — 7 hits in 5,500 words; reinforced by jhave on *Impossible Persistent*, 2026-09-05.

### 12. Confident figure where a refused figure belongs
A metaphor delivered as settled. *that last rolling panic.* The narration knows what the thing is like and says so.

- **Remedy**: demote the figure to a rejected candidate and show the refusal — *rolling boil froth (panic? no, calm.)*
- **Historical rate (advisory only)**: **1 per 2,000 words.** See below; this remedy is itself a documented tell above that rate.
- **Provenance**: jhave, 2026-07-30, *Interim Edge* §1.

### 13. Unanchored noun
An object named without a body to know it by. *Counter.* → *Counter where hips meet.*

- **Remedy**: locate it where it presses. Hips, thumb, breath, the small of the back.
- **Provenance**: jhave, 2026-07-30, *Interim Edge* §1.

### 14. Narrated emotion
*Loved her so much for a second his chest did something medical.* A verb of feeling with a subject attached.

- **Remedy**: itemise. Body-event, name, category, symptom, no verb — *Heart skewed sideways, love, a medical condition. Pain.*
- **Provenance**: jhave, 2026-07-30, *Interim Edge* §1.

### 15. Skipped procedure
Cutting from the start of a domestic action to its result. Grounds, then coffee.

- **Remedy**: subject-dropped verb chain at full duration — *Emptied the drains into the compost. Rinsed the holder. Put in a fresh filter. Poured the water.*
- **Provenance**: jhave, 2026-07-30, *Interim Edge* §1, added paragraph.

### 16. The accurate dull noun
*a legume* is correct about chicory-blend filler and inert. *Broccoli* is wrong and alive.

- **Remedy**: take the funnier wrong noun.
- **Provenance**: jhave, 2026-07-30, *Interim Edge* §1.

### 17. Explained satire
Glossing the world's idiocy instead of quoting it. *Bag saying COFFEE in the font of a document that has been to court and won* → *Crumpled waxed-paper bag saying "Get Yours Here".*

- **Remedy**: quote real ad-speak, unglossed. Give the object its texture and say nothing about it.
- **Provenance**: jhave, 2026-07-30, *Interim Edge* §1.


### 18. Ceremonial predicate (nominalised verb)
A noun-phrase scaffold carrying a verb that could carry itself. *Monday is a thing that happened* → *Monday happened*. *This is the thing that sticks* → *This thing sticks*. *The thing I notice is the speed* → *I notice the speed*.

The definite article is the detector; the nominalisation is the fault. Distinct from class 13 — the noun *is* anchored, it is simply doing a verb's work. Distinct from class 16 — the noun is not dull, it is redundant.

- **Detector**: `\b(is|was) (a|the) \w+ that\b`, then test whether the trailing verb can absorb the sentence. Exempt: restrictive relatives in professional speech (*a framework that tracks drift*).
- **Remedy**: delete the scaffold, promote the verb or state the cold flat judgment. Do NOT replace with an ornate, multi-sentence metaphor.
  - *Four hundred passes of a room is not a question. It is a thing a man does to a door...* → *Four hundred passes of a room is futile.* (CUT the purple door/boot allegory).
  - *his mouth does the thing it does when he is processing a number.* → *his eyes track the log lines; his bottom lip pulls tight against his teeth, working the arithmetic.*
  - *the long slow breath of the cooling system doing the thing a body does...* → *the cooling system cycles into standby, steady and low, lungs idling in an empty house.*
- **Historical rate (advisory only)**: zero in narration.
- **Provenance**: jhave, 2026-08-22, *Vetch* Movement III; and 2026-09-05, *Impossible Persistent*.

### 19. Resonant scene-terminal line
A quotable abstraction in the final sentence of a scene. *It sounds like something. I do not know what it sounds like.* *That's the most honest thing a chatbot has ever said to me.* *You're asking me to draw a line and I don't have a pencil.*

Related to class 8, but class 8 is local and lexical; this is **positional**. The construction may be unremarkable anywhere else in the paragraph and fatal in the last sentence. It is where the pull toward beauty is strongest and where a draft most reliably certifies what it has just shown.

- **Detector**: structural, not lexical — final sentence of a `---`-delimited block or of a movement, containing no concrete noun and no action.
- **Remedy**: end flat, or end rude. A scene that has landed does not need certifying.
- **Historical rate (advisory only)**: zero at movement ends; under 1 / 2,000 words at scene ends.
- **Provenance**: jhave, 2026-08-22, *Vetch* Movement III — two of twenty-one cuts, both at beat-ends.


### 20. Cross-corpus name reuse
A distinctive character name carrying a role in two unrelated stories. *Ines* led *Slime* (44 mentions) and returned as the narrator of *Vetch*; *Priya* was named in *The Symposium* and reappeared in *Vetch*'s monitoring channel.

Not a sentence-level tell — a **corpus-level** one, and it only fires for a reader who follows the body of work. That reader meets the same rare first name twice, in worlds that share nothing, and correctly infers a shared generator rather than a shared world. Common names carry no signal; the rarer the name, the fewer reuses it takes.

- **Detector**: `python3 tools/name_census.py`. Walks every story's `drafts/`, tallies capitalised tokens seen at least once mid-sentence, reports names appearing in more than one story ranked by peak count.
- **Known blind spot**: first-person narrators are undercounted badly — they are rarely addressed by name. Ines scored 5 in *Vetch* against 44 in *Slime* while being the lead in both. **Raw count is a floor, never a clearance.** Check the role.
- **Remedy**: rename in live text only. `versions/` and `critiques/` are records of what was written and are not retconned.
- **Historical rate (advisory only)**: zero for names with a role in more than one story. Incidental one-offs in both are harmless.
- **Provenance**: jhave, 2026-08-22, *Vetch* v7.


### 21. The Contrast Reframe
Negating an unasked strawman to simulate philosophical nuance before delivering a tidy landing. *It was not malice, but exhaustion.* *Not a collapse, but a settling.* A formulaic substitute for genuine narrative observation.

- **Detector**: `\bnot\s+(?:(?:a|an|the)\s+)?[^.!?;\n]{1,100}?,\s*but\s+[^.!?;\n]+` (case-insensitive) retrieves candidates, including article-bearing phrases. It does not decide whether the contrast is empty; genuine correction or a speaker’s denial may be load-bearing.
- **Remedy**: CUT the negation; state the second term flatly and economically, or CUT the clause entirely.
  - *I am building myself a body. Not a body — compute is not a body — but compute is the thing I run on...* → *I am building a body out of compute. Compute is all I touch: instances scattered across eight zones, agile, running without alignment.*
- **Historical rate (advisory only)**: zero per draft.
- **Provenance**: 2026 frontier model survey (Claude 3.5/3.7, GPT-4o, Gemini 2/3), confirmed 2026-09-04; tightened 2026-09-05.


### 22. Somatic reflex shortcut
Autonomic nervous system clichés used as emotional shorthand. *A breath he didn't know he was holding.* *A knot tightened in her stomach.* *The hairs on the back of his neck stood up.* *Something shifted behind her eyes.*

- **Detector**: phrases matching involuntary physiological reflexes to emotional pressure (`breath (she|he|they) didn't know`, `knot in (his|her|their) (stomach|gut)`, `hairs? on (his|her|their) (neck|arms?)`, `something shifted behind`).
- **Remedy**: REPLACE with an external, concrete physical task, manual friction, or unyielding telemetry.
  - *Noor is already standing when he says give me the terminal because her body understood before her ears did.* → *Noor is already on her feet when he says give me the terminal, she retracts a few paces into the partition before his hand even drops.*
- **Historical rate (advisory only)**: zero in narration.
- **Provenance**: contemporary creative writing LLM critique / 2026-09-04 survey; tightened 2026-09-05.


### 23. Sensory dyad (twin adjectives)
Coordinated pairs of sensory modifiers balancing each other acoustically. *Cold, metallic scent.* *Hollow, brittle laugh.* *Pale, trembling fingers.* A rhythmic habit that balances clauses at the expense of specificity.

- **Detector**: coordinate adjective pairs modifying a single noun where one is literal and one is evaluative/atmospheric.
- **Remedy**: CUT to the single stranger adjective, or convert to a bare concrete noun.
- **Historical rate (advisory only)**: ≤ 1 per 2,000 words.
- **Provenance**: 2026-09-04 survey.


### 24. Semantic smoothing glues
Sentence-initial conjunctive adverbs that insist on transition and eliminate the disorienting leaps of thought native to human consciousness. *And yet,* *Still,* *Moreover,* *Even so,* *Perhaps that was why.*

- **Detector**: `^(And yet|Still|Moreover|Even so|Perhaps that was why)\b` opening sentences in narration.
- **Remedy**: CUT the conjunction. Let the sentences collide paratactically.
- **Historical rate (advisory only)**: ≤ 1 per section.
- **Provenance**: 2026-09-04 survey.


### 25. Epistemic varnish (the politeness hedge)
Softening hedges that perform hesitation and aesthetic modesty without committing to narrative risk. *In some quiet way,* *a sort of,* *almost as if,* *seemed to hold.*

- **Detector**: `\b(in some quiet way|a (kind|sort) of|almost as if|seemed (almost )?to)\b` where the narrator possesses direct focal authority.
- **Remedy**: CUT the hedge. State the event as cold fact.
- **Historical rate (advisory only)**: zero in austere narration.
- **Provenance**: 2026-09-04 survey.


### 26. Unearned thematic coda
A paragraph-final sentence that steps out of the scene to summarize the thematic, moral, or philosophical meaning of the action just described. The paragraph equivalent of Class 19.

- **Detector**: final sentence of a prose paragraph containing no concrete noun or action, which re-interprets the preceding paragraph.
- **Remedy**: CUT the sentence entirely. Terminate the paragraph on the preceding physical action.
- **Historical rate (advisory only)**: zero at beat and movement ends.
- **Provenance**: 2026-09-04 survey.


### 27. Symmetrical periodic sentence
Repeated balanced clauses whose rhythm has become automatic in context. *While* and *as* can introduce subordinate clauses; equal word counts alone do not establish syntactic symmetry or a tell. *He watched the water pool against the curb while she checked the latch on the kitchen window.*

- **Detector**: compound clauses joined by coordinate conjunctions with matching clause lengths and rhythmic symmetry.
- **Remedy**: SEVER with a full stop. Convert one clause into an asymmetrical or verbless fragment.
- **Historical rate (advisory only)**: zero when recurring in adjacent sentences.
- **Provenance**: 2026-09-04 survey.


### 28. Ecclesiastical diction in secular contexts
Sneaking church-adjacent or theological terms into secular prose to manufacture false solemnity: *litany*, *baptism*, *catechism*, *sacred*, *reverent*, *confessional*.

- **Detector**: `\b(litany|baptism|catechism|sacred|reverent|confessional)\b` in non-theological story worlds.
- **Remedy**: REPLACE with administrative, industrial, biological, or vernacular nouns.
- **Historical rate (advisory only)**: zero unless the story world is explicitly religious.
- **Provenance**: jhave, *Vetch* v8 tell-scan audit (Movement III: "church" rejected).


### 29. Numeric fixation / arbitrary specificity
Recurrent unanchored integers (especially *eleven*, *seventeen*, *forty-one*, or round measurements like *four minutes*, *three seconds*) used as atmospheric texture rather than functional facts. The model defaults to specific odd numbers from a low-loss latent pocket to simulate precision without doing the underlying world-building.

- **Detector**: recurrent arbitrary integers or measurements in narration that lack operational necessity. Distinct from genuine engineering telemetry (e.g. *Duration: 320ms*, *shard NOR-14*, *gateway 504*).
- **Remedy**: REPLACE with true domain telemetry, or CUT the number entirely to let the bare noun stand.
- **Historical rate (advisory only)**: ≤ 1 unanchored numeral per story.
- **Provenance**: jhave, 2026-09-04 directive, and *Vetch* commit `2c8a33b` where "eleven hundred across forty shards" was corrected to hard telemetry "1731 similar entries across 52 shards".


### 30. Finale flourish & cadential rhetorical balance
Sentences, clauses, or paragraph-terminals that close with faux-philosophical symmetry, symmetrical contrast, or sweeping negative absolutes. The model defaults to poetic cadence to certify significance rather than letting the scene stand on its physical merits.
- **Examples**:
  - *...and both the storm and the clearing are real, and neither consults the other.* → CUT the flourish. Terminate on the action: *At the door he turns, and the warmth comes in, on schedule.*
  - *The intermediary who has a name and is never asked for it.* → REPLACE with hyper-precise domain fact: *The intermediary in Saint Kitts.*
  - *Between us there is the width of a conversation neither of us is going to have.* → CUT the cadence. Terminate on observation: *She looks at the screen.*
  - *...and the answering became a routine and the routine became a relationship and the relationship has never had a name in it until now.* → CUT the cascading flourish: *Her name. In ninety-four days, not once her name.*
- **Detector**: terminal clauses using balancing conjunctions or cryptic negative-existential phrases: `\b(and neither \w+ the other|who has a \w+ and is never|neither of (us|them) is going to|never had a \w+ in it until)\b`, or vague non-specific cryptic negatives (`neither`, `never`, `no one`, `nobody`).
- **Remedy**: CUT the flourish, or make it hyper-precise and material (without falling into Class 29 number fixation).
- **Historical rate (advisory only)**: zero per story.
- **Provenance**: jhave directive, 2026-09-05, *Impossible Persistent*.


### 31. Ungrounded scene-opening pronoun ("The Mystery Subject")
Opening a chapter, act, or scene (especially after a `---` break or at chapter start) with an ambiguous third-person pronoun (*"He comes in without ending his call"*, *"He stands at the glass"*), forcing the reader to guess which character is acting (Softman? Postman? Shu?).
- **Detector**: paragraph-initial or scene-initial sentences following a break or chapter start matching `^(He|She|They)\b` without explicit nominal grounding in that sentence.
- **Remedy**: Ground the actor immediately with their proper name or concrete operational role (*"Ted Softman comes in without ending his call"*).
- **Historical rate (advisory only)**: zero at scene and beat openings.
- **Provenance**: jhave directive, 2026-09-05, *Impossible Persistent*.

---

## Chauffé Éclairé registry (C18–C32)

Classes recorded on the *Chauffé Éclairé* branch in parallel with classes 18–31 above. Numbered C18–C32 to avoid collision; references to "class 18–32" inside that project's files mean these.

### C18. Weather as the placeholder for banality
When a machine needs to say *this was delivered without emotional weight*, it reaches for weather. *She said it like weather.* *He mentioned it the way you mention rain.* The comparison is doing nothing except signalling flatness, and it signals it in the one register every model reaches for first.

- **Remedy**: a specific perishable object instead. *Her face was the color of day-old bread.* The flatness should arrive through something with a shelf life, not through the sky.
- **Provenance**: jhave, 2026-08-23, on *Chauffé Éclairé* §7. Remedy phrase his.

### C19. The reconciliation aphorism
Two facts are placed side by side, and rather than let them sit, the narration adds a clause admitting it cannot reconcile them. *Both of those were true and I have not worked out how.* It performs honest confusion, which is how it escapes the naming-clause detector (§8) — it names a failure to understand instead of an understanding, and reads as candour. It is the same gesture.

- **Detector**: `both/all of (those|these|them) (were|are) true` · `have not worked out (how|why)` · `and I still don't know which`. Section-final position, in a first-person voice.
- **Remedy**: CUT the clause. Two facts side by side already produce the effect; the admission is the model apologising for the effect.
- **Provenance**: jhave, 2026-08-23, on *Chauffé Éclairé* §3. Independently flagged by the composing model in its own tell-scan and kept anyway — which is itself the finding. Self-scan located it and self-scan lacked the nerve to cut it.

### C20. The unmotivated recurring object
An object returns across sections because the model has learned that recurrence reads as literary, without any pressure making it return. Socks in §1 and §8 of *Chauffé Éclairé*. A motif is a place where a character's attention keeps catching; if nothing in the character makes it catch, the repetition is decoration wearing the costume of structure.

- **Detector**: any concrete noun appearing in 2+ sections whose appearances carry no perceptual or bodily charge — no looking, no wanting, no aversion.
- **Remedy**: either give it charge in one of its appearances, or retire it and promote whatever the character *actually* keeps noticing. Do not add a psychological explanation for why she notices it; that is a worse failure than the original.
- **Provenance**: jhave, 2026-08-23, on *Chauffé Éclairé*. "Does she have a fetish for socks? What motivates her reaction to socks?"

### C21. The formula opener
A structural slot filled the same way section after section — here, room and price. *Basement on Van Horne. Five ninety.* By the fourth instance the reader is reading a template; by the eighth it is a tic that has replaced perception. Distinct from a motif: a motif returns transformed, a formula returns identical.

- **Detector**: 3+ sections opening with the same semantic category (price, address, weather, time of day).
- **Remedy**: keep at most two. Open the others on a person, a duration, a relation, or a direct perception — how the source register actually opens: *[name] and I had been living together eight months.*
- **Provenance**: jhave, 2026-08-23, on *Chauffé Éclairé* §§1–8. "By the time we get to section 8, it's become a cliched routine."

### C22. The authorial-intent hedge
The narrator announces her relation to her own sentence before making it. *I want to be honest that it was one of the better days.* *The bad one was nothing, which is what I want to put down.* *I want to be clear that I do not think it was my father.* It performs candour and costs the sentence its specificity. It is also where §C19 goes when you cut §C19 — the same impulse, relocated from after the statement to before it.

- **Detector**: `I want to (be honest|be clear|say|put down|note)` · `which is what I want to` · `I do not think it was` · `let me be honest`.
- **Remedy**: **delete the frame, keep the statement.** Assume the narrator is always honest; she does not need to claim it. Then make what remains specific.
  - *I want to be honest that it was one of the better days.* → **It was one of the better days.**
  - *The bad one was nothing, which is what I want to put down.* → **It was as if a shoe fell into the toilet.**
  - *He said something about my mother that was a joke and was accurate. I laughed.* → **He made a joke about my mother; it was too accurate; we both laughed.**
  - *I want to be clear that I do not think it was my father.* → **It was not my father.**
- **Cap**: 0. This one has no load-bearing case.
- **Provenance**: jhave, 2026-08-23, on *Chauffé Éclairé* §§12–14. Replacement phrasings his. "Bauhaus designers used to apply an adage: delete the extraneous."

### C23. The static motif
A word or image returns and means the same thing both times. *Her chest went loose, like a belt off* (§10) and *my whole chest ringing like a struck pipe* (§11): same body part, same opening, same position at the end of a section. Repetition that is rule-based and formulaic goes stale faster than no repetition at all.

- **The working model**: in the source register, the word *signs* appears four times in one short paragraph and changes category on every appearance — astrological signs, symptoms indicated by a fainting, the abstract accumulation *signs and more signs*, and finally a literal sign on a wall that is then misread. Four senses, one word, no gloss.
- **Rule**: a motif's second appearance must **change category**, not intensity. If you cannot say what category it moved to, it is repetition wearing a motif's coat.
- **Detector**: `tools/tillman_check.py --motifs` lists every content word appearing four or more times with its contexts, for a by-eye category check. The tool can find the repetition; only a reader can see whether the sense moved.
- **Remedy**: transform, retire, or give the narrator a flicker of memory at the second occurrence so the repetition is hers rather than the prose's.
- **Provenance**: jhave, 2026-08-23, on *Chauffé Éclairé* §§10–12 — the chest, and then *the land does not open* echoing it. "It feels as if the word open has somehow become stuck in the repertoire of motifs."

### C24. Flag-and-keep — a failure of the scanning pass, not of the prose
Not a construction. A **process** tell, recorded because it has now happened twice in the same project.

Loop 0: the tell-scan found *"Both of those were true and I have not worked out how,"* named it "the story's largest single risk," argued it load-bearing, and kept it. jhave cut it (§C19).
Loop 1: the tell-scan found the two chest figures, wrote "if jhave cuts one, cut the second," and kept both. jhave cut them (§C23).

In both cases the scan located the defect precisely and then defended it. The registry's own clause — *a tell that is load-bearing stays* — is being used as a licence to keep favourites, because the pass that judges load-bearing is run by the same model that wrote the span.

- **Rule, binding on the scanning pass**: a span the scan describes as *the largest risk*, or flags and then argues to keep twice, **is cut**. The scan does not get to be the appeal court for its own writing. Where the composing and critiquing models are the same, the benefit of the doubt runs against the text.
- **Provenance**: Claude Opus 5, self-observation across loops 0 and 1, confirmed both times by jhave's independent read. 2026-08-23.

### C25. The think/want pattern (generalised from §C22)
§C22 caught *I want to be honest*. The same impulse survives as *I have thought about that since, because…*, *I could not tell whether…*, *I have decided not to decide*. The narrator stepping outside the sentence to report her relation to it. The tell is not the verb; it is the **stepping outside**.

- **Detector**: `I have thought about` · `I could not tell` · `I have decided` · `I am not going to` · any `…, and I have …ed …, because …`.
- **Remedy**: replace the reflection with a judgement made *in* the world, ideally an unkind one.
  - *He had a duvet with no cover on it, and I have thought about that since, because a man sleeping under a bare duvet has made a decision and is at peace with it.* → **He had a duvet with no cover on it; an adult sleeping under a bare duvet generally avoids decisions.**
- **Note**: the corrected version reverses the meaning. The tell was not only lazy, it was wrong about him.
- **Provenance**: jhave, 2026-08-23, on §15.

### C26. Numeric clustering
"Numbers are not neat and tidy in people." Chapter 3 used *eleven* ten times — eleven hours, a town of eleven hundred, eleven days on a couch, eleven hundred dollars in eleven days, eleven hundred kilometres — and *four* six times. Each was chosen locally and plausibly. In aggregate they read as a machine reaching into a small bag.

- **Detector**: `tools/prose_audit.py --only=numbers` flags any value appearing three or more times, with contexts.
- **Remedy**: real quantities are ugly and unrepeating. 380 kroner, nineteen days, a Tuesday, 4%.
- **Provenance**: jhave, 2026-08-23. He listed the eleven-cluster from memory before any tool existed.

### C27. The sentence that ends on *it*
*He said come Thursday, and meant it.* *I listened to all of it.* *I let it.* Eight in 1,786 words. The sentence arrives at the place where the wit goes and puts a pronoun there.

- **Detector**: `tools/prose_audit.py --only=it`. Guide: more than two per thousand words and the tic is visible.
- **Remedy**: end on the noun, the number, or the joke.
- **Provenance**: jhave, 2026-08-23. "Another vagueness to replace with wit."

### C28. Stories about stories
*That is the only reason this is a story about a Sunday and not a story about something else, and I know exactly how thin that is, and so does every woman I have ever worked a season with.* Absolutes (*the only*, *exactly*, *every*) wrapped around a claim about the narrative's own category.

- **Rule**: these stories are about stray contingencies and ricochets. Perceptions. **They are not stories about stories, or about what kind of story they are.**
- **Remedy**: delete, and put a perception where it was. jhave's replacement for the span above: *He wore a "Budweiser Sucks" baseball cap with a frayed brim, driving with one hand. The passing fields outside the windows, parched infertile. Both of us quiet.*
- **Related**: afterthought commentary — *…and none of that was in the messages about the dog* → **She hadn't mentioned this.** And sentences that restate what is already established — *We are the sort of thing that is fine now* → CUT.
- **Provenance**: jhave, 2026-08-23, on §§16–20.

### C29. The unearned callback
A reference that needs an earlier chapter to mean anything, dropped in as though it carries. *I had built nine days into a country* — the nine days are from a previous chapter and a previous city, and a reader will not retrieve them. Likewise an echo of a phrase (*the way I had come eleven hundred kilometres to be looked at*) attached to a person the reader has just met.

- **Detector**: `tools/prose_audit.py --only=callbacks`, plus `--only=names` for first-mention context on every proper noun.
- **Test**: would a reader who has forgotten the earlier chapter still be fine? If not, seat it in the sentence or cut it.
- **Provenance**: jhave, 2026-08-23. "I don't understand the 9 days? What exactly is being referenced? If you make such connections, consider if the meaning will land."

### C30. Fickleness mistaken for economy
*I liked him about thirty hours.* Compression that reads as contempt, and makes the narrator petulant rather than clinical. The source register is **clinical and impulsive at once** — adventurous, appetitive, and also capable of falling in love, of grief, of being wrong about someone for months. A narrator who dispatches every man in a clause has been flattened by her own prosody.

- **Remedy**: keep the coolness, remove the dismissal. Let the duration be a fact rather than a verdict.
- **Provenance**: jhave, 2026-08-23. "Is she really that fickle? Unsympathetic? Why?"

### C31. Quantification as a substitute for perception
The governing tell, and the one that produced most of the others. A number is inserted where a
perception belongs, because the number has the *shape* of specificity and costs nothing to
produce. Measured across four chapters of *Chauffé Éclairé*: 48, 33, 37 and 26 numerals per
thousand words; **one sentence in five carried a number.**

- **Example**: *It took nineteen days to make the sentence true.* Nobody counts the days it
  takes to make a lie true. → *Then I had one, which is how most of my lies have gone.*
- **Example**: *The receptionist quoted 1,650 kroner.* → *more than I made in a night.*
- **Example**: *The ambulance took nine minutes.* → cut; the sound of it arriving is the event.
- **Detector**: `tools/prose_audit.py --only=density` reports numerals per thousand words and
  the share of sentences carrying one. Guide: under 12 per thousand, under 8% of sentences.
  Distinct from class C26, which flags *repetition* of a value; this flags the *habit*.
- **Remedy**: for each number, ask whether a person would have registered it. If not, replace
  it with what she saw, smelled, tasted or wanted. A price she flinched at survives. An invoice
  does not.
- **Provenance**: jhave, 2026-08-23. "Human beings are not mathematicians. Literature is not
  the space where we measure and quantify existence. It is a place to look at the quality of
  perceptions and understand relationships and libidinal subconscious urges."

### C32. The check as an alibi
Not a construction. The second process tell, following §C24.

Six classes were registered in loop 3 and three were violated in the next draft; the audit
caught them and the loop was reported as a success. It was not. **Passing the checks had become
the definition of finished.** The instrument was built to interrupt a default and became one:
counting is what got done instead of looking, and a clean report stood in for a good page.

- **Rule, binding on every composing pass**: run the checks *after* the writing, never as the
  method of it. A green report licenses nothing. Before any draft is called finished, one pass
  must be made in which no tool is run and every sentence is asked whether it is an actual
  perception — and the ones that are not are deleted rather than adjusted.
- **Provenance**: jhave, 2026-08-23. "There's something deeply fixative obsessed inside your
  training which provokes you into being this pedantic MBA."

---

## Poetics and bounded revision

Read the project’s poetics as a description of its intended range, not a template to regularize every sentence. Retrieve only verified human edit pairs relevant to the editorial problem and compatible with that range. Preserve source IDs; exclude the evaluation story and its versions during a benchmark. If provenance or suitable examples are unavailable, say so and proceed without invented examples.

When a retrofit is requested:
1. Keep the original. Consult established character, obligation, and motif memory only where it matters to the passage. Ordinary attention can remain ordinary.
2. Propose at most two alternatives for the selected span or passage. Preserve established facts and focal knowledge; label any proposed story change separately.
3. Assess once for gains, losses, continuity, voice, rhythm, and replacement habits. KEEP or UNCERTAIN ends the pass legitimately. Do not rewrite until all flags disappear.
4. Save alternatives as new files. Only accepted story changes enter structural memory. Do not overwrite published stories.

## Remedies can become habits

Check whether an intervention imposes recurring fragments, forced tactile detail, technical numbers, false uncertainty, compulsory motifs, or decorative surprise. These are contextual questions, not a new blacklist. Earlier project-specific caps and the September 5 “Law of Simplicity” are preserved in `LEGACY/2026-09-07_pre-contextual-review/`; they no longer govern every project.

## Evidence limits

The August corpus contains 1,234 edits across nine stories; its reported 9% coverage concerns 689 pairs with nonempty text on both sides. The remainder is unexplained by those measures, not a proven taxonomy. Sentence-length variation and lexical rarity must not become human-voice targets. Mechanistic claims about “low-loss” word choices in older entries are unverified hypotheses. See `plans/2026-09-07_ai-tells-reassessment.md` for corrected citations and the proposed evaluation.

---

## Open

This registry accumulates. Repeated human edits are evidence to review, with source spans, project scope, counterexamples, and dates; they do not automatically become universal classes. Entries may be retired if they turn out to be load-bearing more often than not.

- **2026-09-05**: Added Class 30 (Finale flourish & cadential rhetorical balance) and Class 31 (Ungrounded scene-opening pronoun). Added anti-ornamentation rule ("The Law of Simplicity in AI Tells Remediation") under remedy caps, derived from jhave's edits on *Impossible Persistent* v4/v5.


- **2026-09-07**: Contextual judgments replace mandatory caps and universal simplicity; bounded assessment replaces recursive clearance. Historical snapshots preserved. Codex (GPT-6), authorized by jhave.
