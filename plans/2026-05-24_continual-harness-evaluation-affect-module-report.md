---
status: testing
implemented-in: narracode_2026-05-29T0611_testing.md (sibling of live narracode.md; not yet promoted)
tested-on: (pending — awaits story selection appropriate to the Affect module)
note: testing harness derives from the May-14 narracode.md and does not yet include AUTO_MODE; reconciliation required before promotion
---

# Evaluation of Continual Harness (Karten et al., 2026) for Narracode

**Date.** 2026-05-24
**Source under evaluation.** Karten et al., *Continual Harness: Online Adaptation for Self-Improving Foundation Agents*, arXiv:2605.09998 — repo at github.com/sethkarten/continual-harness, project page at sethkarten.ai/continual-harness.
**Target of proposed changes.** `narracode.md` at the project root.
**Audience.** The prompter (single human author working with a Compositional/Reflexive/Structural separation).

---

## 1. What Continual Harness actually is

A Pokémon agent that, *within a single non-resetting episode*, edits its own harness state $\mathcal{H} = (p, \mathcal{G}, \mathcal{K}, \mathcal{M})$ — system prompt, sub-agents, skills, memory — by means of a Refiner that wakes every $F$ steps after a warmup window $W$, reads the last $F$ steps of trajectory $\tau_{t-F:t}$, identifies a small named taxonomy of *failure signatures* (navigation loops, tool-call failures, stalled objectives, missed exploration), and emits per-component edits $\Delta = (\Delta p, \Delta\mathcal{G}, \Delta\mathcal{K}, \Delta\mathcal{M})$ via the same meta-tool API the agent uses to act. CRUD on sub-agents and skills; gap-fill / refresh / demote on memory.

A second loop closes the model itself into the process: a pairwise process-reward model scores transitions; low-reward windows are relabeled by a frontier teacher (Gemini 3.1 Pro); a soft SFT update produces the next student. Reset-free across iterations — the emulator state at the end of iteration $k$ is the start of $k+1$.

The clean architectural insight is the *two-loop* shape: the inner loop *acts*; the outer loop *edits the scaffolding from inside which acting will next occur*. The clean engineering insight is that the Refiner uses the *same meta-tool API* as the Agent — they differ only in *when* they're invoked and *on what window of context*.

## 2. Why most of it does not transfer

Pokémon has an objective reward signal: button presses to milestone, milestones unambiguous, victory binary. Literature has none of this. The prompter is the only competent judge of whether a sentence has earned itself, and that judgment is unstable, evolving with the piece, and partly the *point* of writing it. So:

- **No PRM is computable.** There is no automatic "this paragraph is better than that paragraph." The Seamless Edit Method (`on_snapshot` actions 1–3 in narracode.md) is the only PRM available — and its grain is the human's silent micro-edits in the IDE.
- **No teacher model is desirable.** Relabeling low-reward windows with a frontier teacher would median-collapse the prose. Frontier teachers are precisely the failure mode the harness exists to interrupt (cf. narracode.md final note: "competent, fluent, slightly sentimental, slightly explicatory prose that reads like a thousand other models writing about the same thing").
- **No reset-free training of *weights*.** The model is fixed; the harness is the only thing that learns.
- **A literary "failure signature" is not a navigation loop.** It is, e.g., *the second sentimentalisation of a child's mortality within the same scene*, or *a sentence that names an affect rather than performing it*. These are *literarily local*, not statistically detectable from trajectory alone, and they are project-specific because POETICS' Refusals define them.

The fertile transferable insight is therefore not the algorithm but the *separation*: an outer-loop Refiner that lives at a different temporal scale and edits the scaffolding inside which the inner loop will next compose. Narracode already approximates this in `post_draft_check` (succinct outer-loop scan after each draft) and `on_snapshot` (slower outer-loop scan after a session). What is missing is (a) the explicit treatment of these scans as *editing operators on the harness state itself*, with a CRUD vocabulary, and (b) a sufficiently rich representation of *interiority* for the inner loop to draw on without lapsing to default emotional grammars.

## 3. What does transfer

### 3.1 The CRUD framing for structural memory

Continual Harness explicitly types its mutations: creation, update, deletion, demotion. Narracode's structural files currently grow monotonically; the only operation defined is "update." Adding *demote* (move to an archive section) and *retire* (move out of the active window without losing the memory of having had it) would let `motifs.md` and `obligations.md` carry their full history without bloating the live working memory the Compositional agent consults.

**Proposed edit.** Each structural file gains an `## Archived` section. The Structural agent may *demote* without prompter approval; *deletion* always asks.

### 3.2 The named failure-signature taxonomy

Continual Harness names four failure signatures and the Refiner scans for them by name. Narracode's `post_draft_check` currently lists section headings (continuity, obligations, motifs, scene function, voice/default, reader-state) but does not name the failure *patterns* to look for inside them. The 2026-05-14 observations file is the natural source of a literary failure taxonomy already in use, e.g.:

- *Affect-naming.* The prose names the emotion ("she felt sad") rather than performing the operation by which a reader would arrive at the emotion.
- *Sentimental closure.* A scene ends by giving the reader the gesture that resolves the emotional debt the scene just incurred, instead of leaving the debt to compound.
- *Genre-default reach.* A move the writer has used before and which now "works" reliably — i.e., is a trick. Distinct from a motif; a trick is a closed move.
- *Explicatory drift.* The narrator becomes a teacher, summarising the figural meaning of the scene for the reader.
- *Register flattening.* The piece's attentional dialect, declared in POETICS, collapses toward middle-decade-American-literary-fiction default.
- *Cathartic premature.* An inflection point declared in `character-interiority.md` as a *potential* is delivered to discharge tension at the expense of pressure.

These are the literary equivalent of "navigation loop." The Reflexive agent (`on_check`, `on_critique`, `on_drift`) should scan against this *named* list rather than against generic section headings.

**Proposed edit.** Introduce `POETICS.md → Refused signatures` (project-local) and `narracode.md → Default failure signatures` (universal). The Reflexive agent reports findings keyed to signature names.

### 3.3 Outer-loop edits to the prompt itself

The Continual Harness Refiner rewrites $p$ — the system prompt — in light of observed failures. Narracode's `on_snapshot` step 7 already does the gentler version: "If a stylistic pattern in edit-observations is recurring, **recommend** an update to POETICS.md — do not write it unilaterally." The transferable refinement is the *grain*: per draft, not only per snapshot. A draft whose post-draft check identifies the same affect-naming pattern across three drafts should *propose* (never autonomously enact) a new POETICS Refusal.

**Proposed edit.** Add a tiny file `structural/refiner-notes.md` that the Reflexive agent appends to in Check mode whenever a failure signature recurs. The Initiator never reads it; only the prompter reads it; the prompter decides what becomes a Refusal.

### 3.4 Skill creation as project-local prompt micro-disciplines

Continual Harness's "skills" are reusable text-level behaviours plus executable routines. The literary analog is *project-local prose disciplines* discovered mid-composition: e.g., "in this project, sentences with future-perfect verbs always tighten the prose"; "this character only speaks in fragments inside her own apartment." These are skills the Compositional agent should remember and apply, but they are project-local and surface from the writing rather than being declared up front.

**Proposed edit.** Allow `POETICS.md → Discovered disciplines` to accumulate, distinct from the original *Commitments*. The prompter promotes a Reflexive-agent observation into a discipline by explicit consent.

### 3.5 The two-loop temporal separation, made first-class

Naming the two loops would clarify what is currently distributed across hook descriptions:

- **Inner loop.** Compositional pass. Reads the harness state, drafts.
- **Outer loop.** Reflexive / Structural / Initiator passes. Edit the harness state.

The hook framework already enacts this. Naming it as *two loops* would make the architectural intent legible to future contributors and to the model on re-reading. It is also the natural place to install the Affect module described below — as an inner-loop *resource* the Compositional agent consults, distinct from the outer-loop scans that audit how the Compositional agent used it.

## 4. The Affect/Psyche gap

The prompter's diagnosis is correct: `character-interiority.md` is a list of declared potentials (desire, shame, avoidance, contradiction, possible arcs, possible cathartic points), structured for *plot-affording* rather than for *emotionally fluid composition*. It tells the Compositional agent *what is available*, not *how an emotional system behaves*. Asked to write a character's inner state from such a list, the default model behaviour is to map list-items to clauses — to *render* desire, then shame, then contradiction, then a possible arc gesture — producing precisely the stiff, formal, predictable affective writing the prompter wants to avoid.

The fix is not more interiority data. The fix is a *different representational primitive* — one that encodes the *phenomenology* of emotional process rather than its content.

### 4.1 What a human emotional system actually does in story

Drawing on phenomenology (Stern's *affect attunement* and vitality contours, Damasio's somatic markers, contemporary affective neuroscience's interoceptive layer, narrative-psychology's account of double-voicedness, Bakhtin on heteroglossia inside a single consciousness), the relevant features are:

1. **Somatic precedence.** Affect arrives in the body before it arrives in cognition. The character notices a tightening in the chest before noticing the dread. Writing that names dread first is *temporally inverted* and reads as exposition.
2. **Mixed valence.** Real emotional states are usually two or more competing valences at once — relief threaded with grief, tenderness with revulsion, longing with embarrassment. Single-valence rendering is a clichéd reduction.
3. **Displacement.** The affect attaches to the wrong object — irritation at a kettle that is actually grief at a brother. The misattachment is the truth.
4. **Latency.** What the character *registers* is a small fraction of what is operative. Most of an emotional moment is below the threshold of awareness, and good prose acknowledges this by *implying* what the character is not yet able to see.
5. **Recursion.** Feeling about a feeling. Shame at feeling angry. Self-disgust at having needed comfort. Three-layer recursions are common; the model defaults to one layer.
6. **Temporal distortion.** Time slows, jumps, loops, telescopes. A two-second exchange can occupy a paragraph; a six-week stretch can occupy a clause. The clock-time / felt-time ratio is itself an affective signal.
7. **Pre-verbal and interstitial states.** Much of the most interesting emotional terrain has no name — the *almost*, the *just-before*, the *not-quite-yet-resolved*. Naming such a state ("she felt liminal") is the exact cliché to refuse.
8. **Vitality contours.** Stern's term: the *shape* of an emotion in time — its rise, plateau, lapse — which is often more identifying than its name. "Crescendoing-then-collapsing irritation" is a different state from "slow-building, sustained irritation."
9. **Double-voicedness.** Inside a single character there are competing voices — internalised parental voice, defended self, repressed desire, social mask. Bakhtinian polyphony inside a single consciousness.
10. **Reader-affect non-identity.** What the character feels is not what the reader feels. A character who feels nothing in a scene can produce devastation in a reader; a character weeping can produce nothing. This non-identity is the *workspace* of literary affect, and a representation that conflates the two will produce sentimental writing.

### 4.2 Proposed module: `structural/affect.md`

Replaces nothing. Sits alongside `character-interiority.md`, which keeps its current role as a list of declared potentials for plot-affording.

Structure per character:

```text
# Affect: <character name>

## Somatic vocabulary
  Specific bodily registers this character experiences emotion in.
  Avoid universal markers (heart racing, throat tight). Reach for the
  character-specific (a particular knuckle, the back of the soft palate,
  the rhythm of breath at a hairline). Three to seven entries.

## Vitality contours
  Shape-of-emotion descriptors. e.g. "fast-onset, slow-decay shame";
  "delayed-arrival grief that surfaces during physical work";
  "irritation that crescendos then snaps into amusement."

## Mixed-valence permissions
  Pairs / triads this character is permitted to hold simultaneously.
  e.g. "tenderness + revulsion (toward the mother)";
       "relief + dread (after the call)".
  Listing them makes them composable rather than novel each time.

## Displacements
  Recurring misattachments. e.g. "anger at objects when grief at people";
  "tidies the kitchen when she cannot bear what is being said."

## Recursive layers permitted
  How many layers of feeling-about-feeling are credible for this character.
  Some characters are one-layer; some are three; some recurse only with
  one other character present.

## Latencies
  What this character cannot yet see about themselves. Crucial: this
  is the territory the prose can imply but the character cannot name.
  The implication is the literary work.

## Voices
  Polyphony inside the character. Named internal voices, their tones,
  what triggers them. e.g. "the mother voice", "the apprentice voice",
  "the voice that decides the project is doomed."

## Pre-verbal / interstitial states
  States this character occupies that have no name in their vocabulary.
  Describe by approach: what they almost are, what they verge on,
  what they refuse to become. Resist labelling.

## Refused affective moves
  Project-local cliches to refuse for this character. e.g. "no naming
  the emotion in free indirect"; "no single-tear release";
  "no epiphany at threshold (doorways, windows, train stations)."

## Reader-affect target
  Distinct from the character's experience. What the prose intends to
  produce in the reader at the *scene* level, and where the intended
  non-identity between character-affect and reader-affect lies.
```

### 4.3 How the Compositional agent uses it

Before drafting (`pre_draft` extension): read `affect.md` for the focal character(s). Do **not** translate entries into clauses ("Vera felt the tightening at the back of the soft palate"). Instead, treat the module as *constraints on the move-space*:

- The somatic vocabulary is the set of bodily registers permitted to *appear* in this scene; the prose chooses which (or none) and never one not on the list.
- The vitality contour is the *shape* the affective arc of the scene should trace; the prose enacts the contour without naming it.
- The mixed-valence permission means the scene may hold both valences without resolving them; the Refused affective moves include "single-valence resolution."
- The latencies define what the prose may *imply* but the character may *not* think.
- The reader-affect target sets the non-identity gap the scene is to open.

### 4.4 Why this avoids the cliche failure mode

Cliche enters when the model maps named affect to default rendering grammar. The proposed module replaces the *named affect* primitive with *shape, valence-pair, somatic register, latency, and refusal* primitives — none of which has a default rendering grammar. The model is forced to invent prose because the inputs are not pre-mapped to outputs in its training distribution.

It also forces phenomenological precision because the entries themselves *must* be specific: a somatic vocabulary that lists "heart races" is unusable; one that lists "the slight numbness in the lower lip when she has been holding still too long" is usable. The act of populating `affect.md` is itself a literary act and resists templating.

### 4.5 How it interacts with the Reflexive agent

`post_draft_check` gains an *Affect* section keyed to the module:

- Did the draft enact the vitality contour, or describe it?
- Did mixed valences resolve prematurely?
- Did the somatic vocabulary stay specific or default?
- Did the prose name a latency the character should not yet see?
- Did the reader-affect target / character-affect gap open or collapse?

These are *named failure signatures* in the sense of §3.2. The Reflexive agent's job is to identify *which* failed, not to grade.

### 4.6 Population strategy

`affect.md` is *not* written by the Initiator. It is too premature; the entries would be generic. It is written *after the second or third draft*, by the Reflexive agent in *Discovery mode* — reading what the prose has actually been doing and naming the affective primitives that have surfaced. The prompter then edits. This delay mirrors the empirical observation (2026-05-14 notes) that the most useful structural files are the ones that capture what is *already happening* with specificity, rather than declaring in advance what should happen.

**New hook.** `on_affect_discovery` — Reflexive agent, after draft 2 or on prompter request, reads accumulated drafts and proposes `affect.md` entries per character. Prompter confirms or revises before the file becomes active.

## 5. Concrete edits to narracode.md

A minimal patch list, in order of priority.

1. **§ The folder structure.** Add `affect.md` to the structural file list, with the schema sketch from §4.2. Mark as *lazily created* — only by `on_affect_discovery`, not by `on_init`.
2. **§ The agent roles → Reflexive agent.** Add a fourth mode: *Discovery mode*. Used for `on_affect_discovery` and any future "name what has surfaced" passes. Writes proposals, not findings.
3. **§ Hooks → new `on_affect_discovery`.** Schema as §4.6.
4. **§ Hooks → `post_draft_check`.** Add Affect to the section list (alongside continuity, obligations, motifs, scene function, voice/default, reader-state) — but only checks against `affect.md` when that file exists.
5. **§ Hooks → `pre_draft`.** Action 2 extends to include `affect.md` if present. Action 3 (internal inference) explicitly includes the vitality contour and reader-affect target.
6. **§ narracode.md → new section: Default failure signatures.** Names the six signatures from §3.2 plus the five Affect signatures from §4.5. Project-specific signatures live in `POETICS.md → Refused signatures`.
7. **§ The folder structure → structural files description.** Each file gains an `## Archived` subsection. Structural agent may *demote* automatically; *delete* requires confirmation.
8. **§ Hooks → `on_snapshot` action 7.** Generalise: any signature recurring across three or more drafts is proposed (not enacted) as a candidate Refusal or Discovered discipline in `POETICS.md`.
9. **§ Naming the two loops.** A short architectural preamble names the *inner loop* (Compositional) and *outer loop* (Reflexive / Structural / Initiator) and identifies the existing hooks with each.
10. **§ The agent roles → Compositional agent.** Add a single sentence: when `affect.md` is present, treat its entries as constraints on the move-space, not as content to render.

## 6. What is *not* proposed, and why

- **No automatic Refiner running every $F$ drafts.** Refinement of the harness must remain prompter-initiated for literary work. The continual aspect of Continual Harness is wrong for prose; the silence after a draft (`post_draft`) is the prompter's silence too.
- **No PRM, no teacher relabeling, no co-learning loop.** The Seamless Edit Method is the only acceptable analog. Anything else introduces median collapse.
- **No skill-as-executable-code.** Literary skills are prose disciplines, not programs. Adding `run_code` would invite the harness to mechanise what should remain in the prose.
- **No sub-agent spawning at scale.** The four roles already constitute the necessary separation. More agents would dilute, not sharpen.
- **No replacement of `character-interiority.md`.** It does its job for plot-affording. `affect.md` does a different job. They coexist.

## 7. Open questions

- Does `affect.md` belong inside `structural/` or in its own top-level folder? Argument for separate: affect is not structural, it is phenomenological; the conflation is part of why current interiority writing flattens.
- Should *Reader-affect target* live in `affect.md` (per character) or in `reader-state.md` (per scene)? The 2026-05-14 observations note that `reader-state.md` was premature for solo voice work; the per-character placement may be more usable.
- Discovery mode versus the existing Drift mode: are they distinct enough to keep separate? Probably yes — Drift asks *what the piece is becoming*; Discovery asks *what affective primitives have surfaced*. Different objects.
- Vitality-contour notation: should there be a small controlled vocabulary, or only free-text? Free-text resists templating but is harder to audit. Suggest free-text with the constraint that no two characters share the same contour phrasing.

---

*End of report.*
