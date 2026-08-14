---
status: response to prompter question — not yet a build commitment
question: "physics for emotion, graph/GNN for plot, LLM for prose — critique or develop"
relates-to: plans/2026-05-24_continual-harness-evaluation-affect-module-report.md (§4, the Affect module — designed, implemented in the testing harness, never promoted)
---

# Physics, graphs, and the LLM: critique of a three-layer ensemble

*2026-08-14. Claude Opus 5, at jhave's request.*

---

## 0. tl;dr

The intuition is **two-thirds right and one-third a category error**, and its most useful
property is that it is a description of Narracode as it already exists rather than a
proposal for something new.

- **Physics for emotion — right, with a caveat about which physics.** A state vector with
  inertia and decay is exactly the thing LLMs cannot do and the thing literature needs:
  emotional persistence across a scene boundary. But "physics" has three grades, and only
  the first two are defensible. Grade three (force, momentum, conservation as literal
  claims) is decoration. If you cannot name what is conserved, say *dynamical system*.
- **Graph for plot — right. Graph *neural network* for plot — wrong.** These are two
  unrelated proposals sharing a word. The graph as an inspectable data structure is
  already `structural/graph.md` + `obligations.md` and it works. A GNN is a learned
  function over graphs; it needs thousands of labelled plot graphs you do not have, and
  the task it would perform — predict the next node — is the one task the LLM already
  does better, having read every novel. Keep the graph. Drop the neural. There is exactly
  one honest place for a learned graph model in this project and it is a **discriminator**,
  not a generator: §4, Experiment 3.
- **LLM for prose — right as a statement of division of labour, wrong if it implies a
  pipeline.** Physics → graph → prose is the architecture that has failed continuously
  from Talespin (1977) to Scheherazade (2013). The successful version inverts the arrow:
  draft first, *measure* the state afterwards, let the deltas be visible to the next pass.
  Instrument, not autopilot. Narracode's Structural agent already runs in this direction.
- **The real blocker is not architectural.** `plans/2026-05-24` designed an Affect module.
  `narracode_2026-05-29T0611_testing.md` implements it. It was never promoted to the live
  harness, and across 25 stories **no `affect.md` has ever been written**. The emotional
  layer has been sitting on the shelf for eighty-two days. Any physics is a refinement of
  a module that has not been tested once.

There is precedent for the exact three-layer stack — the closest is an art-therapy script
generator from June 2026 that chains emotion-trajectory planning → character scene
generation → emotion-controlled writing. Its domain is the reason it works, and the reason
it does not transfer: in therapy a *prescribed* emotional trajectory is the deliverable.
In literature a prescribed emotional trajectory is the failure mode. That difference is
the whole critique in one sentence.

---

## 1. The intuition is a description of what is already here

Restated against the current folder layout:

| Proposed layer | Already exists as | Currently represented as |
|---|---|---|
| Physics of character emotion | `character-interiority.md`, and the unpromoted `affect.md` | prose |
| Physics of reader emotion | `reader-state.md` | prose |
| Plot graph | `graph.md`, `obligations.md`, `scene-ledger.md` | prose |
| Prose generator | Compositional agent | LLM |

So the question is not *should we add a physics layer and a graph layer*. Both layers are
present. The question is narrower and much more answerable:

> **Which of these markdown files should stop being prose and start carrying numbers with
> update rules?**

That reframing matters because it makes the proposal cheap. Nothing here requires a new
model, a training run, or a rewrite. It requires deciding that three or four fields in
existing files are numeric, and that something recomputes them after every draft.

It also inherits the project's existing commitment, which the README states plainly: the
Compositional agent drafts "from the active pressures in the structural state, not from a
flat summary of the plot." **A physics layer is a way of making *pressure* numerically
explicit.** That is a far better framing of the intuition than a three-layer pipeline, and
it is continuous with the harness rather than parallel to it.

---

## 2. Where the intuition breaks

### 2.1 Three grades of "physics" — keep two, refuse one

**Grade A — state space with dynamics.** A vector per character; scene events as impulses;
exponential return toward equilibrium. This is not a metaphor, it is the standard model in
affect research. The damped linear oscillator has been fitted to emotion-regulation data
since Chow et al.; its parameters index emotional lability and regulation speed. Ninety-day
diary studies of the affective circumplex find the expected restoring force — the farther
from equilibrium, the faster the return — but also find that affect never settles, waxing
and waning indefinitely. That second finding is the literary one: **equilibrium is
approached and never reached**, which is precisely the behaviour a novel needs and an LLM
refuses, because an LLM resolves.

**Grade B — potential landscape and attractors.** Basins, ridges, the energy required to
cross from one to another. Attested for media viewing specifically: emotional attractor
states during narrative consumption behave like a nonlinear system with basins. Useful
because it says something a list cannot: *this character has two basins, contempt and
dependency, and this scene must supply enough energy to cross the ridge, or it must
deliberately fail to.* A scene that moves a character between attractors is doing different
work from a scene that deepens one.

**Grade C — conservation, force, momentum as literal claims.** Nothing is conserved in a
novel. There is no Noether symmetry for grief. The moment the model asserts a conserved
quantity it is generating vocabulary, not predictions, and it becomes unfalsifiable — which
is a specific problem for *this* repo, whose current research direction (tells registry,
survival rate, human-corpus anchors) is entirely built on falsifiability. Grade C would be
the first unfalsifiable thing in `plans/`.

Grade A and B are cheap and testable. Grade C is where the idea goes to become an essay.

### 2.2 The graph / GNN conflation

Two different objects:

- **A graph.** Nodes, edges, attributes. State the LLM reads and writes. Inspectable by
  jhave. Already implemented in markdown. Its value is that it *externalises* continuity so
  the model does not have to hold it in context — which is Narracode's founding move.
- **A graph neural network.** A parameterised function mapping graphs to embeddings,
  trained by gradient descent. Its outputs are vectors, not plot. To use one you need a
  training set of plot graphs with labels, a loss, and a decoder back to language.

The literature that gets cited for "GNN plot generation" mostly does not do what the name
suggests. NGEP infers over event graphs with neural advisors. Narrative-graph work builds
event-centric temporal knowledge graphs from news, using a GNN for *event extraction* —
reading, not writing. The 2026 planning work (PLOTTER, "Planning Beyond Text") runs an
evaluate–plan–revise cycle over event and character graphs with typed edges (CAUSAL,
FORESHADOWING, SUSPENSE) — and the reasoning over the graph is done by an **LLM prompted
over an explicit graph**, not by a learned message-passing network. The field has drifted
from *learned graph functions* to *explicit graphs read by a language model*, which is the
architecture already in this repo.

Three concrete reasons a GNN is the wrong tool here:

1. **No training data.** Twenty-five stories. A GNN wants four orders of magnitude more.
2. **Wrong output type.** It produces embeddings; you need events with prose-level
   specificity. Decoding embeddings to plot reintroduces the realiser problem (§2.3).
3. **Dominated on its own task.** Link prediction over narrative events — "what plausibly
   follows?" — is the single thing a frontier LLM is best at, because that is a large part
   of what next-token prediction over fiction *is*.

The honest use of a learned model, and it is a good one, is in §4/Experiment 3: not
generating structure but **scoring** it, trained on the one dataset this project uniquely
owns — 1,234 human edits.

### 2.3 The pipeline error

The three-layer stack invites a pipeline: physics computes the emotional target, graph
computes the event sequence, LLM renders. This is the architecture of every symbolic story
generator, and it fails at the same joint every time. A planner produces a *correct*
sequence and the realiser produces *dead* prose — the two systems that most nearly worked
(Minstrel's case adaptation, Brutus's grammar-driven betrayal stories) worked by making the
realisation layer carry the literary intent, not the planner.

In literature the arrow runs both ways. Sentences generate plot. A line of dialogue that
surprises you rewrites the character it came from, and that rewriting is often the reason
to keep writing. Any architecture in which the physics is *authoritative* converts writing
into constraint satisfaction — which is already logged in `TODO.md` under *Knowingly
deferred*: "At some constraint density prose becomes constraint-satisfaction. Worth finding
deliberately, in a throwaway." A prescriptive physics layer would find that floor by
accident instead of deliberately.

**The correct role is measurement.** Draft, then measure, then let the measurement be
visible to the next draft as a pressure rather than a target. This is exactly what the
Structural agent already does after every draft, and exactly what the two-loop preamble in
the testing harness formalises. The physics layer belongs in the **outer loop**, as a
ledger — never in the inner loop as a controller.

### 2.4 Whose emotion? Three vectors, routinely conflated

The intuition says "characters and the reader" as if those were one system with two
readouts. They are three systems:

| | Simulable? | Observable? | Governs |
|---|---|---|---|
| Character affect | yes | via the text | behaviour, dialogue, refusal |
| Textual affect (narrator, register, cadence) | partly | directly measurable | voice, distance |
| Reader affect | no | only through jhave's edits | whether any of it lands |

The classical affective-agent architectures — EMA, FAtiMA, the OCC lineage — simulate the
first column beautifully and produce **no narrative tension whatsoever**, because character
emotion is not narrative tension. A character who feels nothing can devastate; a weeping
character can produce nothing. The 2026-05-24 report already states this as item 10,
*reader-affect non-identity*, and calls the gap between them "the workspace of literary
affect."

The systems that actually generated felt suspense modelled the **reader's belief state**,
not the character's feelings: Suspenser and O'Neill's thesis work compute suspense from how
many solutions remain available to the protagonist *as the reader can see them*. That is a
model of the reader's epistemic position, not of anyone's emotion.

So if only one physics gets built, build it on **`reader-state.md`**, not on
`character-interiority.md`. That is the counterintuitive recommendation in this document
and the one with the most support behind it.

### 2.5 The sensor problem

A controller is only as good as its sensor, and the obvious sensor is bad at this scale.
Reagan et al. recovered six emotional arcs from 1,327 Gutenberg texts by running a lexical
happiness dictionary over long sliding windows and taking an SVD. It is a genuine result at
*book* scale and coarse resolution. It dissolves at the scale Narracode works at — the
scene, the paragraph, the withheld sentence — because lexical sentiment cannot see irony,
free indirect discourse, or an affect carried entirely by syntax. Building a scene-level
controller on lexical sentiment is building on a sensor whose noise exceeds its signal in
the band of interest.

Two usable sensors instead: an **LLM judge against a named rubric** (noisy, but it reads
context and can be given the failure-signature taxonomy already drafted in 2026-05-24 §3.2),
and — better, and unique to this project — **jhave's edits**, which are ground truth about
one reader.

### 2.6 Goodhart, arriving on schedule

The moment a suspense number exists, the harness will optimise it, and the prose will
become a thriller. This is not hypothetical: it is the same dynamic already recorded in
`master_ai_tells.md` under "Our own remedies are the next tells."

Mitigation, and it should be a rule rather than an intention: **the physics stays read-only
for a fixed number of stories.** It writes to critiques and to a log. It does not enter
`pre_draft`. Only after jhave has looked at the numbers across several finished pieces and
found them to mean something does any of it become a generation constraint.

### 2.7 The actual blocker

`plans/2026-05-24` §4 designed `affect.md`: somatic vocabulary, vitality contours,
mixed-valence permissions, displacements, recursive layers, latencies, internal voices,
pre-verbal states, refused moves, reader-affect target. The testing harness implements it
along with Discovery mode and the `on_affect_discovery` hook. Status has read `testing`
since May, "awaits story selection appropriate to the Affect module." The live
`narracode.md` contains no mention of affect. No story folder contains an `affect.md`.

**Eighty-two days, zero trials.** Any physics layer is a numeric refinement of that module.
Refining an untested module is the most expensive way to learn nothing.

There is also a genuine tension between the two proposals that is worth naming rather than
papering over. The May design deliberately chose primitives *without default rendering
grammars* — shape, valence-pair, somatic register, latency, refusal — on the argument that
naming an affect invites the model to render the cliché attached to the name. **A number
is a name.** `valence: -0.6, arousal: 0.8` is exactly the kind of pre-mapped input the
module was built to avoid; the model knows what to do with that, and what it knows is
median.

The two designs converge on one point and it is the interesting one. The May module's
*vitality contour* — "fast-onset, slow-decay shame", Stern's shape-of-emotion-in-time — is
the physics intuition arriving from phenomenology instead of from dynamics. Fast onset and
slow decay *is* an impulse response with a time constant. The disagreement is not about
whether emotion has dynamics. It is about whether writing the time constant as a number
helps the prose or harms it.

That is an empirical question, it is cheap to answer, and it should be answered before
anything else in this document is built.

---

## 3. Precedent: has anyone combined different AI structures to make literature?

Yes — continuously, and it has been the norm rather than the exception. The useful finding
is not *whether* but *which combinations survived*.

### 3.1 Symbolic era: the planner-plus-realiser stack (1977–2000)

Talespin (Meehan) ran a goal-directed planner over character goals and realised the trace as
English. Minstrel (Turner) used case-based reasoning with explicit creativity heuristics —
transform-recall-adapt — and is the closest early system to a genuine ensemble, because the
adaptation heuristics did literary work that the planner could not. Brutus (Bringsjord &
Ferrucci) was explicitly hybrid: logic-based story structure plus literary augmented grammars
tuned for a single theme, betrayal. Brutus is worth reading precisely because its authors
were candid that the interestingness lived in the grammars, not the logic.

The shared failure: correct plots, dead sentences. Every one of these systems would have
been improved more by a better realiser than by a better planner — which is the historical
argument for the LLM doing prose, and against it doing only prose.

### 3.2 Emotion engines: complete, and insufficient

EMA (Gratch & Marsella) models appraisal with both fast reactive and slow deliberative
dynamics. FAtiMA (Dias et al.) builds on OCC and integrates planning into an affective agent
architecture; FAtiMA Modular generalises the appraisal framework, and the FAtiMA Toolkit ships
role-play characters with socioemotional decision-making. CHARET tracks character emotion in
stories specifically. Broad reviews of the field exist (*Computational Emotion Models: A
Thematic Review*; the Frontiers overview of artificial-emotion approaches).

Verdict for Narracode: this is the most mature body of work touching the intuition, and it is
aimed one column to the left of where the literary value is (§2.4). Mine it for the *update
rules* — appraisal variables, decay, mood-versus-emotion timescales — not for the architecture.

### 3.3 Reader models and formal suspense

The strongest formal result is not from AI at all. Ely, Frankel & Kamenica (*Suspense and
Surprise*, JPE 2015) define both quantities over a Bayesian observer's belief path:
**suspense** in a period is the variance of the next period's beliefs; **surprise** is the
distance between the current belief and the last. They solve for optimal information release
and apply it to, among other things, the design of mystery novels.

This matters more than anything else cited here, because it is a physics of the reader that is
(a) formal, (b) computable from a small hand-maintained state, and (c) about *belief* rather
than *sentiment* — so it sidesteps the sensor problem in §2.5 entirely. On the AI side,
Suspenser and O'Neill & Riedl's thesis reach a compatible model from planning: suspense rises
as the protagonist's remaining solution paths narrow. Scheherazade (Li & Riedl) learns plot
graphs from crowdsourced examples with precedence and mutual-exclusion constraints — the
lineage in which "plot graph" is a symbolic object with typed edges, which is the sense worth
keeping.

### 3.4 LLM-era hybrids

- **Dramatron** (Mirowski et al.) — hierarchical prompt chaining for screenplays: title,
  characters, beats, dialogue. Structure lives *outside* the model. Evaluated with industry
  professionals rather than by automatic metric, which is the right evaluation posture for
  this repo too.
- **Agents' Room** (Huot et al., arXiv:2410.02603) — decomposes narrative writing into
  narrative-theory-derived subtasks handled by specialised agents; expert evaluators prefer
  its output to baselines. This is the strongest published evidence for the *role separation*
  Narracode already implements.
- **Generative Agents** (Park et al., arXiv:2304.03442) — memory stream, reflection, planning.
  A symbolic memory scaffold around an LLM producing emergent social behaviour. The nearest
  precedent for "structure external to the model, written and read by the model."
- **NGEP** (arXiv:2210.10602) — event-graph inference with neural advisors, reporting gains
  over neural event planning.
- **PLOTTER / Planning Beyond Text** (arXiv:2604.21253) — evaluate-plan-revise over event and
  character graphs with CAUSAL / FORESHADOWING / SUSPENSE edges. The typed-edge vocabulary is
  directly liftable into `graph.md` and `obligations.md`.
- **STORYTELLER** (arXiv:2506.02347), **GraphStory** (arXiv:2606.16102), **Co-DIRECT**,
  **Plug-and-Play Dramaturge** (arXiv:2510.05188) — plot-planning and multi-agent refinement
  frameworks in the same family.
- **CHAE** (arXiv:2210.05221) — fine-grained control over characters, actions and emotions.
  **ViNTER** (arXiv:2202.07305) — emotion-arc-aware generation, where the arc is a coarse
  token sequence ("joy → fear → surprise"). **All Stories Are One Story** (arXiv:2508.02132)
  — emotional arcs as a control signal for procedural level generation.
- **Steering Emotional Dynamics for Art Therapy** (arXiv:2606.16481) — **the closest published
  neighbour to the exact intuition**: an emotion-trajectory planning module that macro-plans an
  outline conforming to a specified emotional arc, a character-driven scene generation module,
  and an emotion-controlled script-writing module producing fine-grained control parameters.
  Physics layer → character/graph layer → prose layer, hierarchically guided LLM agents
  throughout. Read it first, and read it as a limit case: in art therapy the emotional
  trajectory is *prescribed by the clinical goal*, which is why the pipeline direction works
  there. Under the same architecture, a novel becomes a mood-delivery device.
- Surveys for orientation: *Computational Storytelling and Emotions* (arXiv:2205.10967),
  *Narrative Theory-Driven LLM Methods for Automatic Story Generation* (arXiv:2602.15851).

### 3.5 Dynamical systems meeting literary theory directly

Federico Pianzola, *Dynamical systems, literary theory, and the computational modelling of
narrative* (Interdisciplinary Science Reviews / SAGE, 2024) argues narrative is usefully
described as a complex system, with the payoff in describing interpretative and affective
processes in reading — and proposes that transformer models can be treated as artificial
systems simulating a (disembodied) reading process, which is what makes narrative-as-complex-
system computationally modellable. This is the theoretical citation for the entire intuition
and the first thing to read.

Adjacent empirical work: *Modeling narrative structure and dynamics with networks, sentiment
analysis, and topic modeling* (PLOS One 2019); *Relational arcs as narrative structure*
(Computational Humanities Research), which treats character-relationship trajectories as the
structural unit — closer to `graph.md` than any of the plot-graph AI work.

### 3.6 The pattern

Across fifty years, one regularity holds:

> **Structure external to the model wins. Structure learned inside a second network does not.**

Every surviving hybrid — Façade's beat sequencer, Scheherazade's plot graph, Dramatron's
hierarchy, Generative Agents' memory stream, PLOTTER's event graph, and Narracode's
`structural/` folder — keeps its symbolic state in an inspectable external store that the
neural component reads and writes. The systems that tried to learn narrative structure into
network weights produced embeddings and lost the plot, literally.

A second regularity, and the direct answer to the question as asked: the successful ensembles
are **heterogeneous in representation** (graphs, numbers, text, constraints) and
**homogeneous in engine** (one LLM playing several strictly separated roles). Ensembles of
different *model families* are rare in literary generation, and the reason is interface cost —
every seam between families needs a translation layer, and the translation is where the
literary information dies. Narracode is already on the winning side of both regularities. The
intuition, read strictly, proposes moving to the losing side of the second one.

---

## 4. If it gets built: four experiments, cheapest first

Each is stated with what would falsify it. None requires training a model except the last.

### Experiment 0 — Promote and use the Affect module. *(prerequisite, no new work)*

Promote the May-29 testing harness or port the Affect sections into live `narracode.md`. Run
`on_affect_discovery` on the next story after draft 2. Populate one `affect.md`. Read the
prose beside it.

*Falsifies:* everything downstream. If the phenomenological primitives already fix the
emotional flatness, the numeric layer is unnecessary. If they do not, you learn where they
fail before you quantify the wrong thing.

### Experiment 1 — Obligation decay. *(a weekend, no ML, pure bookkeeping)*

Give each entry in `obligations.md` four fields: `planted` (scene), `last-touched` (scene),
`salience` (0–1), `half-life` (in scenes). Each mention is an impulse resetting salience to 1;
otherwise it decays exponentially. The Structural agent updates them post-draft — it is already
reading the draft for exactly this.

Then compute one scalar per scene: total live obligation pressure. Plot it across three
*finished, published* stories.

*Falsifies:* if the curves are indistinguishable between the pieces jhave rates highly and the
ones he does not, the physics has no purchase on this project and the enquiry stops here for
the price of a weekend. If the curves separate, there is a real signal and everything after is
worth doing.

### Experiment 2 — The reader-belief ledger, and formal suspense.

Restructure `reader-state.md` as a set of **open questions with probabilities**: *Is the sister
lying? P ≈ 0.6.* The Reflexive agent re-estimates after each scene. Then, straight from Ely,
Frankel & Kamenica: **suspense** = variance of the next scene's beliefs; **surprise** = distance
the belief moved.

Two numbers per scene, both with real definitions, neither depending on a sentiment classifier.

*Falsifies, and this is the good part —* the prediction is checkable against a corpus that
already exists in the TODO: **scenes jhave edits most heavily are scenes where surprise is near
zero.** If the diff corpus (TODO §A) shows no relationship between measured surprise and edit
density, the reader-physics does not describe this reader.

### Experiment 3 — Character dynamics, A/B tested.

Each character carries a small state — the vitality contour from `affect.md` expressed as onset
and decay constants, plus standing pressures with their own time constants. Scene events are
impulses; between scenes, decay. The Compositional agent receives the *current* state as a
constraint on default behaviour, in the move-space sense the May module insists on — never as
content to render.

*Falsifies:* write the same three-scene sequence twice, once with the state vector and once
without, and have jhave blind-rank them. This is the cheapest true A/B in the whole stack and
the one most likely to show a visible difference, because the specific LLM failure it targets —
emotional amnesia across a scene boundary, premature resolution — is well-attested and
currently unaddressed.

*This is also where the disagreement in §2.7 gets settled empirically*: does a number help, or
does it re-import the rendering grammar the phenomenological primitives were built to refuse?

### Experiment 4 — The only learned model worth training. *(only if 0–3 pay off)*

Not a plot generator. A **survival predictor**: given a span and its structural context, the
probability that it survives jhave's edit. Training data is the diff corpus in TODO §A —
1,234 edits, paired supervision, confound removed. This is a model of one reader, which is far
more useful to this project than a model of readers in general, and it computes a metric the
TODO already commits to.

This is also the one place graph structure genuinely earns its keep, as *features* rather than
as an architecture: distance in the obligation graph from this span to the nearest live
obligation, motif recurrence count, scenes elapsed since the relevant relation last changed. If
those features predict survival better than surface features alone, the graph is doing real
work and you will have proved it. If not, you have learned that too, cheaply.

Note the role: **critic, not generator.** It scores; it never writes. That is the ensemble
position the precedents support.

---

## 5. What not to build

- **A plot planner that emits an outline for the LLM to fill.** Fifty years of dead prose.
  Narracode's design already refuses it in the Compositional agent's specification.
- **A GNN that generates plot.** No data, wrong output type, dominated by the LLM on its own
  task (§2.2).
- **A sentiment-driven controller at scene scale.** The sensor cannot see irony (§2.5).
- **Any physics in `pre_draft` before it has been read-only for several complete stories**
  (§2.6).
- **A second model family in the generation path.** Interface cost exceeds benefit; the seam is
  where the literary information dies (§3.6).
- **Grade-C physics vocabulary in the harness prose.** If nothing is conserved, do not say
  conservation. `narracode.md` is read by the model, and metaphor in the harness becomes
  metaphor in the output.

---

## 6. Open questions

1. Does a numeric vitality contour help the prose or trigger the rendering grammar the May
   module was built to refuse? *(Experiment 3 settles it. Nothing else here matters until it
   is settled.)*
2. Should the reader-belief ledger be per-question probabilities, or ordinal bands? Numbers
   invite false precision from a model that will happily emit `P = 0.63`; bands
   (`unlikely / open / probably / assumed`) may carry the same information with less
   fabrication. Suspense-as-variance survives either.
3. Half-life of an obligation: is it a property of the obligation, of the reader, or of the
   project's poetics? Experiment 1 can distinguish these if half-lives are fitted per story
   rather than assumed.
4. Does the physics belong in `structural/` or beside it? The 2026-05-24 report asked the same
   question of `affect.md` and left it open: affect is phenomenological, not structural, and
   the conflation may be part of why interiority writing flattens.
5. Is there a literary observable for which the *attractor* framing (Grade B) pays rent that
   the *oscillator* framing (Grade A) does not? Candidate: characters who cannot change until
   a scene supplies enough energy — the "sudden reversal that reads as earned" problem.

---

## 7. Recommendation

Do Experiment 0 now; it is already built and it costs nothing but a promotion and one story.
Do Experiment 1 next, because it is a weekend and it can kill the entire idea for that price.
Then Experiment 2, because formal suspense over a belief ledger is the strongest and
best-founded piece of this proposal and it is checkable against a corpus the project has
already committed to building. Hold Experiments 3 and 4 until the first two have said
something.

And drop the graph neural network. Keep the graph, type its edges — CAUSAL, FORESHADOWING,
SUSPENSE, from the 2026 planning work — and let the LLM reason over it, which is what the
field converged on and what this repo already does.

---

## Sources

**Emotion dynamics as a dynamical system**
- [Emotion as a Thermostat: Representing Emotion Regulation Using a Damped Oscillator Model](https://www.semanticscholar.org/paper/Emotion-as-a-thermostat:-representing-emotion-using-Chow-Ram/0783cf4e3d8e6a7bc8045c72639eec2be358a41b) — Chow, Ram et al.
- [A dynamical systems interpretation of a dimensional model of emotion](https://pubmed.ncbi.nlm.nih.gov/11321635/)
- [Emotional Valence as A Control Variable in A Generic Valence-Arousal-Dominance Dynamical System](https://link.springer.com/article/10.1007/s42761-026-00383-8) — *Affective Science*, 2026
- [A Nonlinear Dynamical Systems Approach to Emotional Attractor States during Media Viewing](https://www.researchgate.net/publication/353587982_A_Nonlinear_Dynamical_Systems_Approach_to_Emotional_Attractor_States_during_Media_Viewing)

**Narrative as a complex/dynamical system**
- [Dynamical systems, literary theory, and the computational modelling of narrative](https://journals.sagepub.com/doi/abs/10.1177/03080188241257167) — Pianzola, 2024
- [The emotional arcs of stories are dominated by six basic shapes](https://arxiv.org/abs/1606.07772) — Reagan et al., 2016
- [Modeling narrative structure and dynamics with networks, sentiment analysis, and topic modeling](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0226025) — PLOS One, 2019
- [Relational arcs as narrative structure](https://www.cambridge.org/core/journals/computational-humanities-research/article/relational-arcs-as-narrative-structure-dynamics-distribution-and-diachronic-change-in-fiction/37947D31A93A7FA276BC3E6BA67C5DFD)

**Reader models, suspense, surprise**
- [Suspense and Surprise](http://www.journals.uchicago.edu/doi/pdfplus/10.1086/677350) — Ely, Frankel & Kamenica, *JPE* 2015
- [A Computational Model of Suspense for the Augmentation of Intelligent Story Generation](https://faculty.cc.gatech.edu/~riedl/pubs/oneill-thesis.pdf) — O'Neill
- [A Computational Model of Narrative Generation for Suspense](https://cdn.aaai.org/Workshops/2006/WS-06-04/WS06-04-003.pdf)

**Plot graphs and symbolic structure**
- [Story Generation with Crowdsourced Plot Graphs](https://faculty.cc.gatech.edu/~riedl/pubs/aaai13.pdf) — Li & Riedl
- [Scheherazade: Crowd-Powered Interactive Narrative Generation](https://faculty.cc.gatech.edu/~riedl/pubs/aaai15.pdf)
- [An Introduction to AI Story Generation](https://mark-riedl.medium.com/an-introduction-to-ai-story-generation-7f99a450f615) — Riedl, historical overview
- [NGEP: A Graph-based Event Planning Framework for Story Generation](https://arxiv.org/pdf/2210.10602)
- [Planning Beyond Text: Graph-based Reasoning for Complex Narrative Generation](https://arxiv.org/html/2604.21253) — PLOTTER
- [Narrative Graph: Telling Evolving Stories Based on Event-centric Temporal Knowledge Graph](https://pmc.ncbi.nlm.nih.gov/articles/PMC10126530/)
- [GraphStory: Collaborative Story Writing through Event-Based Narrative Editing](https://arxiv.org/html/2606.16102)

**Computational emotion architectures**
- [FAtiMA Modular: Towards an Agent Architecture with a Generic Appraisal Framework](https://link.springer.com/chapter/10.1007/978-3-319-12973-0_3)
- [Computational Emotion Models: A Thematic Review](https://link.springer.com/article/10.1007/s12369-020-00713-1)
- [Computational Approaches to Modeling Artificial Emotion](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00021/full)
- [CHARET: Character-centered Approach to Emotion Tracking in Stories](https://arxiv.org/pdf/2102.07537)

**LLM-era ensembles and hierarchical generation**
- [Steering Emotional Dynamics for Art Therapy: Controllable Narrative Script Generation through Hierarchically Guided LLM Agents](https://arxiv.org/pdf/2606.16481) — closest neighbour to the intuition
- [Agents' Room: Narrative Generation through Multi-step Collaboration](https://arxiv.org/pdf/2410.02603) — Huot et al.
- [Co-Writing Screenplays and Theatre Scripts with Language Models](https://dl.acm.org/doi/fullHtml/10.1145/3544548.3581225) — Dramatron
- [Generative Agents: Interactive Simulacra of Human Behavior](https://dl.acm.org/doi/abs/10.1145/3586183.3606763) — Park et al.
- [STORYTELLER: An Enhanced Plot-Planning Framework](https://arxiv.org/pdf/2506.02347)
- [Plug-and-Play Dramaturge](https://arxiv.org/html/2510.05188v3)
- [CHAE: Fine-Grained Controllable Story Generation with Characters, Actions and Emotions](https://arxiv.org/pdf/2210.05221)
- [ViNTER: Image Narrative Generation with Emotion-Arc-Aware Transformer](https://arxiv.org/pdf/2202.07305)
- [All Stories Are One Story: Emotional Arc Guided Procedural Game Level Generation](https://arxiv.org/abs/2508.02132)

**Surveys**
- [Computational Storytelling and Emotions: A Survey](https://arxiv.org/pdf/2205.10967)
- [Narrative Theory-Driven LLM Methods for Automatic Story Generation and Understanding: A Survey](https://arxiv.org/pdf/2602.15851)
- [Integrating Cognitive, Symbolic, and Neural Approaches to Story Generation: METATRON](https://www.mdpi.com/2227-7390/13/23/3885)

---

*End of report.*
