# POETICS.md — project commitments

*Initiated 2026-08-23. Working title: Chauffé Éclairé. Loop: 0. AUTO_MODE.*

---

## Display title

Chauffé Éclairé

## Display synopsis

Montreal, 2028. A woman moves through eleven apartments, jobs, and men in a city priced past her. Heat included, lights included, nothing else included. Episodic, blunt, sexual, unsentimental — the socioeconomics of a rental listing applied to a life.

## Governing lineage — override

`master_poetics.MD` declares the house lineage (Ōe, Butler, Akomolafe, Blanchot). **This project overrides it.** The single coordinate here is the register the prompter named: Lynne Tillman's *Weird Fucks* — episodic sexual autobiography written in short flat declaratives, without artifice, arriving at confession by refusing to decorate it.

**Emulation, not cloning.** No sentence of Tillman's is reproduced. No character, scene, city, or incident of hers is transposed. What is taken is *prosody and stance* — measurable properties of sentence length, figuration rate, and affective flatness — reconstructed from first principles in `reference/voice-engine.md` and enforced by `tools/tillman_check.py`. The prompter's stated goal is the essence, not a rule-regulated clone. The engine measures the essence; it does not carry her words.

**One phrase quoted by the prompter** — *"heart located in cunt, inarticulate"* — is held as a target *specification*, not as material: a body-part located inside another body-part, an abstract organ given a physical address, then a single flat adjective refusing to explain it. That is a buildable operation. It is built, in our own nouns, and the source phrase appears nowhere in the draft.

## Form

- **Episodic sections, each one man or one apartment or both.** Numbered. No connective tissue between them. Time skips without announcement.
- **Each section arrives at an inversion** — a convulsion, a raw confession, a flat reversal — in its last three to six sentences. The turn is never prepared and never explained afterward.
- **Section headers are neighbourhood and month.** Parc-Ex, February. Verdun, July. The header carries the socioeconomics; the prose never editorializes about rent.
- **People enter fast and leave.** A man gets four sentences and a name. Some get a name only. Some get neither.

## Voice — measurable

The voice is a set of numbers, not an adjective. Targets enforced by `tools/tillman_check.py`:

| property | target |
|---|---|
| median sentence length | ≤ 7 words |
| sentences ≤ 8 words | ≥ 65% |
| sentences > 14 words | ≤ 8% |
| any sentence > 12 words | must break on `;` or be speech |
| words after a `;` | ≤ 10 |
| simile / `like a` / `as if` / `the way you` | ≤ 2 per 1,000 words |
| paragraphs | ≤ 9 sentences |

- **First person, past tense, female narrator.** No name until someone says it.
- **Flat declarative.** Subject, verb, object. The period does the work a comma would beg for.
- **No extended metaphor. No mixed metaphor. No conceit.** A figure that runs past one clause is cut, not shortened.
- **Sex is named and not decorated.** The plain word, once, unglossed. No euphemism, no lyricism, no aftermath paragraph explaining what it meant.
- **Money is a number.** Rent, pay, fare, fine. Never "expensive," never "couldn't afford it."
- **Humour is dry and arrives in the same flat register as the grief.** No signalling.

## Linguistic pressure

- Copular avoidance per `master_poetics.MD` §2.C, but *not* replaced with tactile lushness. Replaced with a shorter sentence.
- Lexical diet (§2.E) holds: `thing`, `spent`, `held`, `bent`, `small` audited on sight.
- No self-reflexive commentary, no analytical clauses, no editorializing (`master_phrases_to_avoid.md`).
- No paradox-aphorism or chiasmus openers (`master_ai_tells.md` §4). No `which is only X` (§5). No corrective-superiority stance (§6). No triadic escalation (§9). No naming clause (§8) — this is the primary risk in this register, because the flat style tempts a summarizing final line.
- **Em-dash rationed hard.** This voice joins clauses with a period. Em-dash is a tell here in a way it is not elsewhere in the house style.

## Montreal 2028 — the socioeconomic instrument

Neighbourhood is the class system and does all the work adjectives would do.

- **Parc-Extension** — the densest, poorest postal code in the city; South Asian and now also everyone priced out of Mile End. Université de Montréal's campus arrived in 2019 and the rent followed.
- **Verdun** — flipped inside a decade. Wellington voted coolest street in the world in 2022 and never recovered from it.
- **Hochelaga-Maisonneuve** — the eastern edge of the flip, still arriving.
- **Côte-des-Neiges** — immigrant, transient, students, the cheapest rooms with the longest commutes.
- **Saint-Henri** — condo towers against the canal, the old parish underneath.
- **Mile End** — priced out, then priced out again. The narrator's mother's era.
- **Griffintown** — glass, no grocery store, wind.
- **NDG, Villeray, Rosemont** — the middle that is closing.

2028 texture, used flatly and never explained: renoviction notices, the housing tribunal backlog, wildfire smoke summers, heat warnings and cooling centres, the REM's east extension, Bill 96 in its seventh year, gig work under an app, Airbnb conversions, a deposit that is illegal in Quebec and asked for anyway, `chauffé éclairé` on every listing.

## Refused

- Redemption. She does not get the apartment, the man, or the insight.
- Any sentence explaining what an encounter meant.
- Lyrical sex. Lyrical weather. Lyrical poverty.
- A closing section that gathers the others into a meaning.
- Trauma as engine. Things happen; the register does not escalate to meet them.
- Montreal as charm. No cobblestones, no accordion, no snow described as anything.
- Reproduction of, or direct allusion to, any specific Tillman sentence, scene, or character.

---

## Amendment — loop 1 (`on_new_direction`, 2026-08-23)

Prompter direction: chapter 2, she goes on the road — Toronto, Winnipeg, the prairies, Banff,
Vancouver. Chapter 1 is frozen and not to be edited. A photographed page of the source was
supplied. Four criticisms were made and all four are accepted.

### 1. The voice targets are replaced

The page was measured. Chapter 1's targets were wrong — built from the prompter's stated
rule (*rarely above eight words*), which describes the punches and not the prose. Measured
source: mean 12.5, median 9, longest 30, CV 0.73, 36% of sentences over fourteen words.
Chapter 1: mean 6.3, median 6, longest 14, CV 0.46, 0% over fourteen.

**The signature is variance, not shortness.** New profile in `tools/tillman_check.py`
(`road`): mean 10–15 · median 8–12 · **CV ≥ 0.60** · at least one sentence ≥ 22 words ·
18–42% over fourteen · punches (≤ 4 words) ≥ 8% · semicolon chains ≥ 0.8 per 300 words ·
figures ≤ 4 per 1,000 · em-dashes permitted. The old profile is kept as `telegraphic` and
chapter 1 still measures against it. Chapter 1 fails the new profile on six of nine checks.
That failure is left standing in the record.

### 2. The formula opener is retired

Sections may no longer open on room-and-price. By §8 it had become a template that replaced
perception. Chapter 2 opens sections on a relation and a duration, a departure time, a
person, a piece of ground. Registry class 21.

### 3. Renée now has a character

`structural/character-interiority.md` was rewritten from nothing. Backstory exists so the
prose has ground under it and **may never be used as explanation** — no causal chain, no
*because*. What she notices is hands and forearms, which was already latent in chapter 1
and unrecognised by the draft that wrote it. Socks are retired unmotivated (class 20);
chapter 1 keeps them because chapter 1 is frozen.

### 4. New commitments

- **Friends.** Chapter 1 gave her none. Kat can be rude to her; the Banff kitchen is a cast
  that lasts a whole section and likes each other.
- **Desire built through physical proximity before emotion.** Eight inches at a counter for
  the length of a song. The tension is spatial first.
- **Direct perception.** She is a lapsed photographer, never stated as a reason. Muskeg, a
  dead deer, dust standing up gold, a grid road. Noticing is now a thing the prose does.
- **Fluctuation, not arc.** Desire arrives at the wrong intensity, sometimes lands, sometimes
  produces nothing, sometimes catastrophizes twenty minutes late for no assignable cause.
  §12 is a section where nothing happens and this is not a failure of the section.
- **2028 on the surface.** The year said outright, and carried in the corridor works, the
  freight priority, September frost, an October fire, staff accommodation deducted at source.

### 5. Comedy declared

Per the loop-0 drift finding, which recommended it and was not acted on until now: humour in
the same flat register as the grief, never signalled. The parrot doing the thing.
