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
