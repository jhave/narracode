---
status: evaluation — two changes implemented, three proposed
source: github.com/deepseek-ai/deepseek-harness (developer preview, MIT), read at depth-1 clone
target: narracode.md
companion-to: plans/2026-05-24_continual-harness-evaluation-affect-module-report.md (same genre)
---

# Evaluation of DeepSeek Harness (dsh) for Narracode

**Date.** 2026-08-14
**Source under evaluation.** `deepseek-ai/deepseek-harness` — an open-source agent harness, developer
preview, ~50 packages, built on [Cordis](https://github.com/cordiverse/cordis). Docs at
`deepseek.com/harness` are unreachable from this environment; this reads the repository directly.
**Audience.** The prompter.

---

## 1. What dsh actually is

An agent harness for software development whose organising claim is **everything is a plugin**:
the model adapter, the tool registry, the session log, and the agent loop itself are all
replaceable from configuration. "There is no privileged core to patch: you extend dsh by
mounting a plugin beside the others, and registrations are effects that unwind when their
plugin unloads."

Four ideas carry the architecture.

**Profiles and bundles.** A running instance is a plugin tree composed at boot from ordered
layers — bundles, then the profile's patch file, then the home-level patch, then any command-line
overlay. `dsh --dump-config` prints the tree the machine actually boots, and any row it prints can
be replaced.

**Turn and step.** A *step* is one model request plus the tools it calls. A *turn* is zero or more
steps: "it opens before its first input is claimed and closes once nothing is owed."

**Capability seams.** A seam is a swappable capability with **three** roles — a Service Definition
declaring the interface, a Service Provider implementing it, and a Consumer using it. The document
is explicit: "A package may combine roles, but **one role alone is not a seam**; adding a
capability means designing all three."

**The session log, and one hard invariant.** The append-only log is the source of the context the
model sees; everything else — fork, resume, transcripts, telemetry — derives from it. The rule is
stated flatly and enforced at runtime:

> **Model-visible means logged.** Anything that reaches a model request must be reconstructable
> from the log, and a runtime invariant asserts it.

---

## 2. Why most of it does not transfer

**The plugin architecture is the wrong shape for this project, and deliberately so.** dsh has
about fifty packages. `narracode.md` is one file of 510 lines that a writer can read in a sitting
and edit in a text editor. That is not a limitation Narracode is waiting to outgrow; it is the
property that makes the harness usable by someone who is not a programmer. A Cordis tree would
make Narracode more powerful and less available, and availability is the point — the whole
distribution model is "one file that unfolds into the system."

**Model adapters as config rows are irrelevant.** In dsh, swapping a model is a configuration
change. In Narracode the model is a *poetic* decision, recorded in `ATTRIBUTION.md` by exact
version because Fable 5 and Opus 5 write differently and the difference is the subject of ongoing
research. It is not a row to be patched; it is a credit.

**No analogue for sandboxes, LSP, terminals, subprocess confinement, credentials.** Roughly half
the repository is about executing untrusted code safely. Narracode executes nothing.

**Compaction is the one package to actively refuse.** dsh's `compaction` family summarises
context under token pressure. Its name resembles a Narracode need — structural memory does grow —
and adopting it would be a mistake, because Narracode's founding argument is that *summary is
where literary information dies*. The harness already says so: the Compositional agent drafts
"from the active pressures in the structural state, **not from a flat summary of the plot**." A
summarising layer between the structural files and the drafting pass would reintroduce precisely
the median collapse the architecture exists to interrupt. If structural memory must shrink, it
shrinks by *demotion to an archive section* (the CRUD proposal from the May report, still
deferred), never by summarisation.

That leaves four things, and the first is worth the whole exercise.

---

## 3. What transfers

### 3.1 "Model-visible means logged" — and Narracode currently cannot satisfy it

This is the strongest single idea in the repository and Narracode fails it today.

Ask a question the project will certainly want answered: *why did draft 5 of Vetch do what it
did?* Answering requires knowing what `POETICS.md`, `obligations.md`, `character-interiority.md`
and the rest said **at the moment that draft was composed**. Those files are mutable and are
overwritten by every Structural pass. The `versions/` snapshots cover some of it, but they fire at
snapshot moments, not at composition moments, and the two do not coincide.

So the harness's own state is not reconstructable at the point where it matters most. For twenty-six
stories, "what was the model looking at when it wrote this sentence" is unrecoverable.

This is not an abstract tidiness concern. It is directly load-bearing for two things already
committed to in `TODO.md`:

- **§A, the diff corpus.** The corpus pairs a machine draft with jhave's edit of it. But the
  supervision signal is *"given this context, the model produced this, and the human changed it
  to that."* Without the context term, the corpus teaches a model to imitate edits rather than to
  make different decisions from the same inputs.
- **Experiment 4, the survival predictor.** Predicting whether a span survives jhave's edit
  requires the features the span was generated under. Right now those features are gone.

**The Narracode-native form is small.** Not a session log — the harness has no runtime. A
**composition manifest**: when `pre_draft` fires, it already reads a specific, enumerated set of
files. Record which ones, and a short content hash of each, in one sidecar beside the draft. Nine
lines of plain text per draft. It makes the question answerable from that day forward, costs
nothing, and requires no new machinery.

**Implemented.** See §4.1.

### 3.2 The three-role seam — a diagnosis of the eighty-two days

> "One role alone is not a seam; adding a capability means designing all three."

Read that against what happened to the Affect module. It was designed on 24 May as a *schema* — a
Service Provider, in dsh's vocabulary. It had no Definition stating what contract it satisfied and,
critically, **no Consumer**: no pass was required to read it. It was created lazily, ignored until
confirmed, and optional in every hook that mentioned it.

It then sat unused for eighty-two days across twenty-six stories.

That is not a coincidence and it is not forgetfulness. It is the predictable behaviour of a
structural file that nothing is obliged to consult. dsh names the failure mode precisely, and the
rule generalises:

> **A structural file that no pass is required to read is not a module. It is a note.**

The corollary is a cheap gate on future additions: any new file in `structural/` must declare, at
the point of creation, which pass writes it and which pass **must** read it. If the second half is
empty, do not create the file — put the content in an existing one.

**Implemented.** See §4.2.

### 3.3 "The log records the attempt" — refusals are invisible

From the turn-flow documentation:

> "a rejected or empty first claim still closes a durable turn that spent no step, **so the log
> records the attempt**."

dsh treats a *refused* request as a durable fact worth keeping. Narracode does not. It records
drafts that were written. It does not record drafts that were declined — directions the Reflexive
agent argued against, continuations jhave rejected, scenes started and abandoned.

For software that is bookkeeping. For literature the refusals are arguably the more interesting
half of the record, and this project has said so in its own vocabulary: `POETICS.md` has a
**Refusals** section, and `master_ai_tells.md` is an entire registry of moves not to make. But
those are *declared* refusals, written in advance. The *enacted* ones — the moment a specific
direction was considered and put down — leave no trace at all.

Worth doing, but it needs jhave's judgement about what is worth the friction, so it is proposed
rather than implemented. A minimal version: when a direction is explicitly rejected in
conversation, one line appended to a `refusals.md` — what was proposed, and the reason it was put
down. Nothing more.

### 3.4 `--dump-config` — there is no way to see the effective poetics

dsh composes its behaviour from ordered layers and then provides one command to print what the
machine actually boots, because a layered system whose effective state cannot be inspected is a
system nobody can reason about.

Narracode is now layered in exactly this way and has no such command. On any given pass the
effective rule set is `narracode.md` plus `POETICS.md` commitments plus its Refusals plus its
Discovered disciplines plus the named failure signatures plus `master_ai_tells.md` plus the
project's accumulated `edit-observations`. Those accrete over a project's life. There is no way to
ask *what is actually constraining the next scene?*

Proposed: an `on_effective` orientation mode that assembles and prints the current constraint set
in layer order, with each rule tagged by where it came from. This becomes more valuable the longer
a project runs, which means the argument for it is strongest exactly where it has never been
tested. Proposed, not implemented — I would rather jhave decide whether it is a real need or a
tidy-looking one.

### 3.5 Turn / step — noted and declined

The distinction is elegant, and "closes once nothing is owed" is a lovely phrase for a system that
tracks obligations. But Narracode's inner/outer loop is human-paced: the prompter decides when a
pass happens. A finer-grained turn model would formalise a boundary the harness deliberately
leaves to a person. Recorded here so it is a decision rather than an oversight.

---

## 4. Edits made to `narracode.md`

### 4.1 Composition manifest

New `## The composition manifest` section, and a step added to `pre_draft`. Each draft gets a
sidecar `drafts/[N]-[short-name].context.md` recording which files were read, their sizes, and a
short hash, plus the mix level and the total obligation pressure at composition time.

The rule, stated in the harness in dsh's own terms: **what the Compositional agent saw is
recorded.** If a new input becomes model-visible, it goes in the manifest.

### 4.2 The seam gate on structural files

One paragraph added to `## Structural memory files`: every file declares its writer and its
required reader, and a file no pass must read does not get created. `affect.md` is named as the
worked example, because it is the case that produced the rule.

---

## 5. What is not proposed, and why

- **No plugin tree, no Cordis, no config layers.** §2. The single-file property is the
  distribution model.
- **No compaction.** §2, and it is the most important refusal here.
- **No runtime session log.** Narracode has no runtime. The manifest is the per-draft form of the
  same principle at roughly a thousandth of the cost.
- **No model-adapter abstraction.** Model identity is attribution, not configuration.
- **No subagent-provider seam.** The five roles are a literary separation, not a scheduling one.
  Making them swappable would invite substitution, and the whole argument is that *these five*
  are the right five.

---

## 6. Open questions

1. Should the manifest hash file *contents* or record the git blob SHA where one exists? The
   latter is free and exact inside a repository, the former works for uncommitted state. Currently
   a short content hash, which works in both cases and is verifiable by hand.
2. Is a manifest per draft too coarse? A long composition pass may read the structural state once
   and produce several sections. Probably fine; revisit if a draft's manifest is ever visibly stale.
3. Does the refusal log (§3.3) actually get written, or does it become the second `affect.md` — a
   file designed, implemented, and never used? By its own rule in §3.2 it currently has no required
   reader, which is a reason to be suspicious of it.
4. Is there a literary reading of *"closes once nothing is owed"*? It is the obligation ledger's
   sentence, arrived at independently, in a document about agent loops.

---

*End of report.*
