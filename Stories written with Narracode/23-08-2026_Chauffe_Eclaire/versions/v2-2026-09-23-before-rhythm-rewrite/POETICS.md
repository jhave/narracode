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

---

## Amendment — loop 2 (`on_new_direction`, 2026-08-23)

Prompter direction: chapter 3, back across the country, *a great hurtling swirling sweaty
libido acutely insightful sentences ricocheting through paragraphs*. Ends in Toronto, final
section boarding a plane to Amsterdam. Chapters 1 and 2 both frozen. A second photographed
page supplied.

### 1. Sex is the engine

Accepted without qualification. Rent, moving and shifting fortunes are the **taxes** of this
story and they had been carrying sections that appetite should have carried. She has chosen a
life of exploration with appetites; chapter 3 follows the implications accurately and does not
punish her for any of it. She wants people, gets some of them, some of it is very good, one
Sunday costs fifty-two dollars, and she repents of nothing.

### 2. Motifs must change category

From the supplied page: *signs* four times in one paragraph — astrological, symptomatic,
abstract, then literal signage, misread. Chapter 2's *chest* meant the same thing twice and
*open* meant it a third time. Registry class 23. Chapter 3's motif is **cover**, carrying
bedding, a covered shift, reciprocity, smoke, **insurance coverage**, shelter, a cover charge
and a covers band. Seven senses, no gloss. *open* and *chest* are retired.

### 3. The procedure chain

New required form, from the page: for a bodily task that is difficult, undignified and takes
real time, drop the subject and go to bare verbs at full duration, semicolons inside the
action, return to *I* at maximum indignity. `master_ai_tells.md` §15 stated positively.
Minimum six bare-verb openers per chapter, enforced by the `swirl` profile. §17 carries it.

### 4. Delete the extraneous

Registry class 22. The narrator is always honest and therefore never says she is being honest.
Zero tolerance — no load-bearing exception exists for this class. All four of the prompter's
corrections are recorded verbatim in `reference/voice-engine.md` §12.

### 5. Class 24 binds the scanning pass

Twice the tell-scan located a defect precisely, argued it load-bearing, kept it, and the
prompter cut it anyway. The registry's *a tell that is load-bearing stays* was functioning as
a licence to keep favourites, because the pass judging load-bearing is run by the model that
wrote the span. **A span the scan names as a top risk is now cut, not defended.** Three spans
were cut under this rule while drafting chapter 3, including one that had already been written.

### 6. Acutely insightful ≠ commentary

The insight arrives as a fact or an image, never as a maxim. Permitted: *I had carried the
thing nine hundred kilometres. He had only been living here.* Refused: any sentence that could
be printed on its own and still sound wise.

---

## Amendment — loop 3 (`on_new_direction`, 2026-08-23)

Prompter direction: chapter 4 — Europe briefly, then Bergen; an affair with a Slovenian
doctoral candidate at the Centre for Digital Narrative studying the sexual orientation of
NPCs, avatars and AI influencers; falling in love with him and sleeping with a married
dentist in the same weeks; a voyage north; a woman having a seizure in a grocery store;
return to Bergen, pack, fly to Amsterdam. *Witty, ironic, succinct, dry, terse, exact as
Joan Didion. Every sentence that is not an exact perception, make it so.* Chapters 1–3 frozen.

### 1. The harness becomes a set of checks, not rules

The prompter's instruction: *build up this harness style guide for this particular system,
that is not rule-based, but actually just kind of performs a bunch of checks — vaguenesses,
numeric repetitions, motifs, relational continuity problems.*

`tools/prose_audit.py`. It measures nothing and passes nothing. Eight checks: vagueness and
absolutes · meta-commentary · sentences ending on *it* · numeric clustering · section-opener
shapes · triplet formulas · every proper name with first-mention context · callbacks that may
not land. Run against chapter 3 it independently reproduced every one of the prompter's
line-notes, including the *eleven* cluster and the eight terminal *it*s.

### 2. Six new registry classes (25–30)
think/want pattern · numeric clustering · the sentence ending on *it* · stories about stories ·
the unearned callback · fickleness mistaken for economy. All jhave's provenance, with his
replacement phrasings recorded verbatim.

### 3. Time is established by a device, and the device changes every section

From four photographed openings, none of which uses a place-and-date: a policy of life · a
gnomic universal · a present-tense trigger · a flat cliché · anniversary layering · prolepsis
with deferral. Chapter 4's six sections use six different ones. Recorded in
`reference/voice-engine.md` → Calibration IV, with the wit devices from the same passages.

### 4. She is not fickle

Registry class 30. *I liked him about thirty hours* made her petulant. The source register is
clinical and impulsive at once — appetite and coolness in one person, and also love, and
being wrong for months, and grief. Chapter 4: she is in love with Blaž and going to Terje on
Thursdays and the story does not adjudicate. Durations are facts, not verdicts.

### 5. The new pressure is fatigue

Constant emotional availability plus constant appetite, producing a distorted unsettled
reality. Shown as an amplitude problem — everything arriving at one volume after Florø — and
never as self-diagnosis. She does not know what is wrong with her and is not made to find out.

### 6. Motif for this chapter: **charge**
Six senses, one per section, none glossed: battery · erotic · authority · money · assuming
control · overload. A seventh use was cut for repeating the money sense. *cover*, *open* and
*chest* stay retired.

---

## Amendment — loop 4 (`on_new_direction`, 2026-08-23) — the governing correction

Prompter direction: rewrite chapter 4. The first chapter of the project he has asked to be
rewritten rather than frozen. Chapters 1–3 remain untouched.

**The fault.** Across four chapters one sentence in five carried a number: 48, 33, 37 and 26
numerals per thousand words. *It took nineteen days to make the sentence true* is accounting.
Nobody counts the days it takes to make a lie true. The number was there because a number has
the shape of specificity while costing none of the looking that specificity requires.

**The deeper fault.** The harness was built to interrupt a default and became one. Counting is
what got done instead of writing; a clean audit stood in for a good page. Registry classes 31
(quantification as a substitute for perception) and 32 (the check as an alibi) record both.

**The rule that now governs composition, above every threshold in this file:**

> Write as the woman — free, travelling, appetitive, unsentimental, with an exact eye — and
> interrogate every sentence as she would. If it is vague, or merely competent, or does not
> build the texture and the tension of an actual perception, delete it.

Checks run *after* the looking, never as the method of it. A number earns its place only where
a person would register one. Where a measurement is doing the work, a sensation is missing.

**Demonstrated in this loop:** the rewrite leaves three `didion` checks failing, on the grounds
that the prose is right and the thresholds are mine. That refusal is the point of the loop.
