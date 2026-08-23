# Voice engine — the flat declarative

*Built 2026-08-23 for* Chauffé Éclairé. *Companion to `POETICS.md`. Enforced by `tools/tillman_check.py`.*

The prompter asked for the essence of a register, explicitly not a clone. So this file
does not hold a single sentence by Lynne Tillman. It holds the **operations** that produce
the effect, each one stated as a procedure and demonstrated on our own material —
Montreal, 2028, our narrator, our men. The exemplars below are original. They are the
reservoir the compositional pass draws from.

---

## 1. The eight-word governor

The sentence ends before it explains itself. Most sentences are five to eight words.
The period is not punctuation; it is refusal.

> Rent was 1,340. I took it.
> He had a futon and a cat.
> The cat was called Docteur.
> I stayed four months.

**Failure mode.** The eight-word rule produces staccato monotony if every sentence is
also the same *shape*. Vary the shape, not the length: declarative, fragment, question,
speech, a bare noun phrase, a number.

## 2. The semicolon hinge

The one licensed long sentence. A clause, a semicolon at the middle, then ten words or
fewer. The hinge is where a fact turns into a position without any word announcing it.

> He said he loved his wife; I believed him and stayed anyway.
> The tribunal date was in fourteen months; I painted the kitchen.
> She was crying in the stairwell; nobody in the building came out.

## 3. Located abstraction

The prompter's specification, generalized. Take an abstract interior noun. Give it a
physical address inside the body. Then one flat adjective, refusing to elaborate.

Operation: `[abstract organ] + [located in] + [body part] + [, one adjective]`

> Shame sat behind the knees, patient.
> Want in the jaw, stupid.
> Whole future parked in the throat, unpaid.

**Cap: three per story.** Above that it becomes a device and the flatness curdles into
mannerism. The tells registry's own warning applies — every remedy acquires a detector
the day it is adopted.

## 4. Sex, said once

Name it with the plain word. Do not build to it, do not aftermath it. The next sentence
is about something else entirely, and that adjacency is the whole effect.

> We fucked on the floor because the bed was his roommate's.
> Afterwards he showed me the mould behind the radiator.

**Refused:** lyricism, euphemism, slow motion, a paragraph about what it meant,
weather participating.

## 5. Money as number

Never "expensive." Never "couldn't afford." The figure, bare, in a sentence with no
adjective in it.

> 1,340. 1,655 by the third year. 2,100 when I left.
> He made 31 an hour and told everyone.
> The deposit was illegal. I paid it.

## 6. The four-sentence man

A person is a name, a job, one physical fact, one thing they said. Then they are gone
and do not return. Refuse to develop anyone the reader has begun to like.

> Milad drove for two apps and slept at his sister's.
> He had a burn on his forearm from the fryer at the other job.
> He said Parc-Ex was finished, everybody knew.
> I never saw him again.

## 7. The convulsion

Each section turns in its last three to six sentences. The turn is a fact stated in the
same flat tone as everything preceding it, and the flatness is what makes it land. It is
never prepared, never followed by commentary.

> He asked if I wanted to see the baby. There was a baby.
> I said the thing I had never said out loud. Then I asked about the heat.

**Refused:** any sentence after the turn that tells the reader the turn happened.

## 8. Neighbourhood as class

The header does the socioeconomics. The prose never says gentrification, precarity,
inequality, or crisis. It says a street, a number, a smell, a commute time.

> Côte-des-Neiges. Fifty minutes to work, two buses.
> In Verdun the dep sold natural wine.
> Griffintown had no grocery store. Everyone ordered.

---

## The anti-patterns — hard refusals

| refused | because |
|---|---|
| extended metaphor | the register's entire proposition is that experience is not *like* anything |
| a simile chain | two figures in a paragraph reads as literary performance |
| the summarizing last line | `master_ai_tells.md` §8, the naming clause — the single largest risk here |
| a paradox opener | §4 — flat prose tempts the aphorism as compensation |
| triadic escalation | §9 — "the rent, the smoke, the whole century" |
| an em-dash joining clauses | in this voice a period does it; the dash softens |
| "I realized that" | realization is shown by what the next sentence is about |
| weather doing emotional work | snow is snow, smoke is smoke, neither is participating |
| a character explaining the city | no one delivers analysis of Montreal |

---

## Calibration

Run before every draft is considered finished:

```
python3 tools/tillman_check.py "Stories written with Narracode/23-08-2026_Chauffe_Eclaire/drafts/1-chauffe-eclaire.md" --verbose
```

Green on all prosody and figuration checks is necessary and not sufficient. The tool
cannot detect the naming clause, sentimentality, or a man who got five sentences instead
of four. That is the reflexive pass's job.

---

# Calibration II — measured against the source, 2026-08-23

The prompter supplied a photographed page. It was measured. **The first engine was wrong**,
and wrong in a way worth recording, because it was wrong by obeying an instruction.

| | source page | chapter 1 (built to instruction) |
|---|---|---|
| mean sentence | **12.5** | 6.3 |
| median | **9** | 6 |
| longest | **30** | 14 |
| coefficient of variation | **0.73** | 0.46 |
| over 14 words | **36%** | 0% |
| at or under 4 words | 18% | 31% |
| semicolon chains | 2 in 137 words | 0.4 per 300 |

The brief said *rarely a sentence above eight words*. On the measured page, **55% of
sentences are over eight**. The instruction described the punches and mistook them for the
prose. Chapter 1 was built to the instruction and came out telegraphic, which the prompter
diagnosed independently before the page was measured. Both routes arrived at the same place.

**The signature is variance, not shortness.** A 27-word sentence and a 2-word sentence in
the same paragraph. The short one only lands because the long one went first.

## The operations the page teaches

**1. Open on a relation and a duration.** Not on a room and a price. A name, how long, where,
and what the two of you were doing there — chained through commas into one long sentence
that gets the whole situation standing up before anything happens.

> Kat and I had been friends eleven years, first in Montreal and then not at all, and then
> again because she picked up the phone.

**2. The chained character introduction.** One sentence, semicolons, four or five facts in
descending order of respectability, ending on a blunt verdict of three or four words.
Occupation, proximity, a credential, a marriage that isn't working, then the verdict.

> Dez did sound for other people's films, lived above a garage on Sterling; had toured with a
> band nobody remembers, had a kid in Halifax he saw twice a year; he was easy.

**3. The punch.** Two or three words, alone, after a long run. It is not a fragment for
texture. It is the next fact, arriving with everything else stripped off it.

> Later, the fires.

**4. The gnomic place-line.** Present tense, second or third person, a rule of the city
stated as fact and never explained. One per section, at most.

> In Winnipeg nobody stands outside to finish a conversation.

**5. The one-line paragraph of practical motive.** A whole paragraph, one short sentence,
giving the errand that moves her. Desire and errand are the same movement and the errand is
what gets said.

> He might have a couch.

**6. Simile is permitted.** The measured page has two in 137 words. They are casual and
comparative, never decorative — *like hash*, not *like a wound opening*. The cap is taste,
not abstinence: four per thousand words.

**7. Carry the period on the body.** A Victorian nightgown, a fur coat thrown over it. The
year is worn, not announced.

## Retired from Calibration I

- The eight-word governor. Wrong. Replaced by mean 10–15, median 8–12, CV ≥ 0.60.
- The em-dash prohibition. The source uses them. ~5 per 1,000 permitted.
- The figuration cap of 2. Raised to 4.
- The refusal of long sentences. **A section with no sentence over 22 words now fails.**

---

# Calibration III — the second page, 2026-08-23

A second photographed page. Two operations on it that the engine did not have.

## 9. The transforming motif

The word *signs* appears four times inside one short paragraph and **changes category on
every appearance**: astrological signs, symptoms indicated by a fainting, the abstract
accumulation, and then a literal sign on a wall which is immediately misread into something
else. Four senses. One word. No gloss, no nudge, no acknowledgement that a pattern is
occurring.

Set against what chapter 2 did with *chest* — loose like a belt off, then ringing like a
struck pipe — same organ, same opening, same slot at the end of a section, no movement. And
*the land does not open* echoing it a section later.

**The rule: the second appearance must change category, not intensity.** If you cannot name
the category it moved to, you have repetition wearing a motif's coat. Registry class 23.
`tools/tillman_check.py --motifs` lists candidates; only a reader can judge whether the
sense moved.

## 10. The procedure chain

For a bodily task that is difficult, undignified and takes real time, the prose drops the
subject and goes to bare verbs at full duration — begin, think, reach, pull, snap, squat,
kneel — with semicolons inside the action rather than between thoughts, then returns to *I*
at the moment of maximum indignity, then lifts into mock-epic, then lands on two words.

This is `master_ai_tells.md` §15 (skipped procedure) stated positively, and it is the
register in which the source handles contraception, embarrassment and the body. Chapters 1
and 2 have no passage like it anywhere. **One per chapter, minimum, enforced.**

## 11. Sex is the engine, not the weather

The prompter, plainly: *the prurient interest of sexuality* was at the forefront of the
source and is a subdued threat here. Rent, moving, and shifting fortunes are the taxes of
the story; they were carrying sections that should have been carried by appetite. *This is a
young woman who has chosen a life of exploration with appetites, so just be accurate and
honest about following the implications of that.*

Accurate and honest means: she wants people, she gets some of them, some of it is very good,
some is a bad twenty minutes, she is not punished for any of it and does not repent. Say what
happened. Do not build to it and do not process it afterward.

## 12. Delete the extraneous

The narrator is always honest, so she never says she is being honest. Registry class 22.
Every one of these was in chapter 2 and every replacement is the prompter's:

| written | corrected |
|---|---|
| I want to be honest that it was one of the better days. | It was one of the better days. |
| The bad one was nothing, which is what I want to put down. | It was as if a shoe fell into the toilet. |
| He said something about my mother that was a joke and was accurate. I laughed. | He made a joke about my mother; it was too accurate; we both laughed. |
| I want to be clear that I do not think it was my father. | It was not my father. |

Chapter 2 is frozen and keeps its versions. Chapter 3 is written under the corrected rule.

## The `swirl` profile — chapter 3

*A great hurtling swirling sweaty libido acutely insightful sentences ricocheting through
paragraphs.* CV ≥ 0.65 · longest sentence ≥ 26 · over-fourteen ≥ 22% · **procedure chain: at
least six bare-verb sentence openers** · zero class-22 hedges · retired words: *open* as a
motif, *chest* as the site of feeling.

**Acutely insightful is not the same as commentary.** The insight arrives as a fact or an
image, never as a maxim. *I had carried it nine hundred kilometres and he had only been
living here* is allowed. *Desire carried that far arrives heavier than a person can hold* is
the naming clause with better shoes.

---

# Calibration IV — how she starts a section, 2026-08-23

Four photographed openings. Not one of them begins with a place and a date, and not one
begins the same way as another. Time is established by a **device**, and the device is
different every time.

| device | how it works |
|---|---|
| **present-tense trigger** | An ordinary act now dislodges the past. *Watching an English television play reminds me of life with Roger, an English actor I lived with for two months.* Duration and relation arrive in the same clause as the trigger. |
| **a policy of life** | *I was staying away from men and lived and worked in Amsterdam where I found it easy to do so.* A rule she had set herself, which the section will break. |
| **a gnomic generalisation** | *By now everyone knows that Valium is one way to get over a love affair.* A flat universal about a substance or condition, then straight into the particular. |
| **a flat cliché** | *Breaking up is hard to do.* Deployed without irony marks and immediately outrun by specifics. |
| **anniversary layering** | *Two years before I'd written a short story on this day about the day and this year I found myself falling in love again.* Three time-planes in one sentence. |
| **prolepsis with deferral** | *John's uncanny instinct for the kill would reappear, but not for another two weeks.* The future named and withheld. |

## The wit devices in the same passages

- **Assert, then puncture.** *…the cast became friends too. Of course no one makes friends that easily.*
- **Colon-redefinition.** *life becomes intensely fair: everything is the same.* The colon reverses the word in front of it.
- **The pun that comes free with the noun.** *work at the film cooperative was impossible — no one cooperated.*
- **Comic collision of registers.** *I read Jane Austen while on the train and feared that I might have to marry the Greek man.*
- **Double-negative self-portrait.** *I'm not one not to smile.*
- **Vagueness assigned to a person, not to the prose.** *public relations person for something or other* — the fuzz characterises his job, not the writing.
- **The cool dismissal that is not contemptuous.** *His enthusiasm only intrigued me.*
- **Gnomic close.** *It is safer to stay indoors.*

Compare our own *which everybody tells you and nobody believes until their thumbs stop
closing* — a maxim about nobody, doing no work. Hers are about a named substance, a named
city, a specific fear, and each is funny.

## The audit

`tools/prose_audit.py` is the durable artefact of this loop. It measures nothing and passes
nothing. It reports vaguenesses, absolutes, meta-commentary, sentence-final *it*, numeric
clustering, section-opener shapes, triplet formulas, every proper name with its first
mention, and callbacks that may not land — and leaves every judgement to a reader.

Run against chapter 3 it independently reproduced **all** of jhave's line-notes, including
the *eleven* cluster (ten occurrences) and the eight sentences ending on *it*. The checks
exist because a human found something first; the tool is a memory of his attention, not a
replacement for it.

```
python3 tools/prose_audit.py <draft.md>
python3 tools/prose_audit.py <draft.md> --only=numbers,it,meta
```
