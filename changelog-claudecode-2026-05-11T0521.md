# Narracode → Claude-Code-Style Agentic Harness

**Proposal date:** 2026-05-11
**Author:** Claude (Opus 4.7) on behalf of jhave
**Status:** Draft for discussion. Nothing implemented.

---

## 0. Premise of the proposal

Narracode is a *role-separated, prompter-sovereign* harness today. Its core discipline is:

- One pass per invocation. No chaining.
- The prompter drives the loop; the model performs the requested pass and stops.
- State is externalized to files so the critical pass can govern the generative pass.

Claude Code's agentic gains come from a different place than autonomy-over-decisions: they come from **agency-over-infrastructure** — tool grammar, hooks, todo ledgers, subagents, plan mode, permission gates, persistent memory, status surfaces. Those are largely *orthogonal* to creative authority and can be ported into Narracode without violating its discipline.

This proposal therefore separates two questions and only answers the first:

1. **What infrastructure can we borrow from Claude Code that makes the harness sharper, more legible, and more composable — without making the model a more autonomous author?** (Yes, lots.)
2. **Should we let the model take more authorial agency — chain passes, propose continuations unprompted, decide what comes next?** (Mostly no, with one or two narrow, opt-in exceptions.)

The guiding rule: *agency in the housekeeping; sovereignty in the writing.*

---

## 1. What's working today (do not break)

Before proposing changes, naming what must survive:

- **Separation of passes.** The five-role discipline (Initiator / Reading / Structural / Compositional / Reflexive) is the mechanism. It is *not* a stylistic choice.
- **Prompter sovereignty.** "The piece belongs to the prompter." The model does not anticipate, does not chain, does not please.
- **POETICS.md as commitments-and-refusals.** A first-class artifact, not a prompt fragment.
- **Externalized state.** `structural/`, `drafts/`, `versions/`, `critiques/` — files, not memory.
- **The Seamless Edit Method.** Diff-against-original, learn from manual edits, distill recurring observations into POETICS.
- **Lazy folder generation.** Only what's needed exists.
- **Single-file invocation.** `narracode.md` is the whole harness; you can drop it into any agent IDE.

Every proposal below is constrained by these.

---

## 2. The improvement plan

Twelve proposed additions, grouped. Each item names: **what**, **why**, **how it would feel**, **risk to discipline**, and **verdict** (recommend / consider / reject).

### Group A — Tool grammar and command surface

#### A1. Explicit "skills" / slash-command vocabulary

**What.** Define a small, named command surface that maps 1:1 to the existing roles, alongside the existing natural-language triggers. Not as replacement, as *aliases*.

```
/init <premise>         → Initiator
/read [target]          → Reading agent
/structure              → Structural agent
/draft [scene-name]     → Compositional agent
/critique [draft]       → Reflexive (critique mode)
/drift                  → Reflexive (drift mode)
/snapshot [descriptor]  → Versioning
/orient                 → "returning to the project" pass
/poetics-update         → propose a POETICS.md amendment
/expand [draft]         → Expansion agent (alternatives)
```

**Why.** Two reasons. (1) Power users — and other AI agents reading this harness — benefit from a discoverable, unambiguous surface. (2) These names become *the public API* if/when narracode becomes a real CLI tool, and stabilizing them now lets file-format and CLI evolve together.

**How it would feel.** Either trigger works. `"keep going"` and `/draft` both invoke the Compositional agent. The natural-language layer is the human surface; the slash layer is the programmatic surface.

**Risk.** Low. Pure addition; nothing forced.

**Verdict.** **Recommend.**

#### A2. A typed "request envelope" for every pass

**What.** Each invocation, regardless of trigger, gets parsed into a small structured object the model writes to `loop-notes.md` for that loop:

```yaml
loop: 7
trigger: "keep going, but slower this time"
resolved_pass: compositional
inputs_read: [POETICS.md, structural/*, drafts/6-the-saturation.md]
constraints_added: ["slower pacing per prompter cue"]
output: drafts/7-morning.md
```

**Why.** Today the loop is opaque after the fact. With a tiny envelope, you can grep the project's history and reconstruct the conversation that produced any draft.

**Risk.** Low; this is metadata, not behavior.

**Verdict.** **Recommend.**

### Group B — Memory layers

#### B1. Split context from commitments: introduce `CONTEXT.md`

**What.** POETICS.md is *commitments and refusals* — declarative, principled, slow-moving. But there is currently no place for the volatile facts the model needs to write well that *aren't* commitments: open threads, the prompter's mood today, dropped subplots, recently surfaced obsessions. Introduce `CONTEXT.md` (or `STATE.md`):

```
./
  POETICS.md       (slow: commitments, refusals, dialect)
  CONTEXT.md       (fast: pending decisions, open threads, today's pressure)
  ATTRIBUTION.md
  structural/
  drafts/
```

**Why.** Today this fast-moving context is either lost or smuggled into POETICS, which corrodes POETICS. Separating them keeps the slow file authoritative.

**Risk.** Adds a file. Mitigated by keeping it short (cap at ~50 lines) and lazily created.

**Verdict.** **Recommend.**

#### B2. Per-loop `loop-notes.md` upgraded to a real journal

**What.** Already exists per-snapshot in `versions/v[N]/loop-notes.md`. Upgrade its schema to: prompt verbatim → resolved pass → inputs read → outputs written → edit-observations summary → unresolved questions for next loop.

**Why.** It's already there. Currently underspecified. Making the schema explicit turns it into a ledger you can replay.

**Verdict.** **Recommend.**

#### B3. A project-level `MEMORY.md` index (optional, for long projects)

**What.** Borrowed directly from Claude Code's auto-memory pattern: an index of facts the model has accumulated about *this project specifically* — characters' established tics, refused phrasings the prompter pushed back on, register decisions the edit-observations have crystallized. Each entry one line; pointers to the heavier files.

**Why.** For projects that run long enough to exceed any single context window, this gives the model a consistent, compressed orientation surface.

**Risk.** Easy to write a memory layer that overlaps POETICS / CONTEXT / structural. Define the boundary upfront: MEMORY.md is *only* derived facts the model learned across loops, never editorial intent.

**Verdict.** **Consider** — useful for novella-length work; overkill for a short story.

### Group C — Subagents and parallel exploration

#### C1. Expansion agent (already named in README, missing from narracode.md) — formally specify it

**What.** README mentions an Expansion Agent ("generates alternative continuations that intentionally push beyond the boundaries of the uploads"). It is **not** present in `narracode.md`. Spec it in:

- Activated by `/expand [draft]` or "give me a divergent continuation."
- Reads POETICS, structural state, the named draft.
- Produces N alternatives in `drafts/[N]-alt-{a,b,c}-[short-name].md`.
- Writes a `drafts/[N]-alt-rationale.md` explaining how each alternative breaks from the dominant grain.
- Does not pick a winner. The prompter does.

**Why.** Closes a documented gap between README and narracode.md. Gives the prompter an explicit "show me the road not taken" lever.

**Verdict.** **Recommend.**

#### C2. Parallel-pass dispatch (Claude-Code subagent style)

**What.** When the prompter explicitly says "give me three", the model may dispatch the Compositional agent in parallel, each pass independent, results landed as `drafts/[N]-alt-*`. Claude Code's worktree pattern: isolated, then merged or discarded.

**Why.** This is one of Claude Code's biggest power-user wins. For a literary harness it lights up what should already be there: comparative drafting.

**Risk.** Cost. Parallel literary passes are expensive. Gate behind explicit prompter request.

**Verdict.** **Recommend** as opt-in, never automatic.

#### C3. A "second-reader" critique subagent

**What.** When critique mode runs, optionally spawn a *second*, independent reflexive pass that does not see the first critique's output, then collate. Two voices on the same draft.

**Why.** Mirrors Claude Code's "independent code review" pattern. Critique is exactly the place where independence matters most — a single critique pass tends to converge on whatever frame it picked first.

**Risk.** Cost; some redundancy. Make it opt-in via `/critique --double`.

**Verdict.** **Consider.**

### Group D — Hooks and automation

#### D1. Declare an explicit hook surface

**What.** Today the harness implies several "automatic" behaviors (autonomous snapshotting, edit-observation diffing, structural-update-before-draft). Make these explicit as **named hooks** with declared trigger / pre-condition / action:

```
hooks:
  pre_draft:    [run_structural_sync]
  post_draft:   [offer_critique_or_continue]
  on_edit:      [diff_vs_original, append_to_edit_observations]
  on_snapshot:  [write_loop_notes, copy_drafts_critiques_structural_poetics]
  on_orient:    [read_poetics, latest_loop_notes, latest_draft, latest_critiques]
```

**Why.** Right now these are scattered across the prose of `narracode.md` and easy to forget. As a declared surface they're auditable, overridable, and one day implementable as actual settings.json hooks when the CLI lands.

**Risk.** None — pure restatement of existing implicit behavior.

**Verdict.** **Strongly recommend.** This may be the single highest-leverage change.

#### D2. A pre-pass "plan mode" (Claude-Code-style)

**What.** Before any draft pass, an optional one-paragraph plan: *what this scene will do, what stays out, where it ends.* The prompter accepts or revises the plan, then the draft proceeds. Closely modeled on Claude Code's plan mode.

**Why.** Drafts that get long re-rolled rounds of edits often suffer from misaligned scene-scope, not misaligned style. A 60-second plan exchange catches that early.

**Risk.** Adds friction. Make it `/draft --plan` opt-in, not default.

**Verdict.** **Recommend** as opt-in.

### Group E — Permission and verification

#### E1. Permission gates on irreversible actions

**What.** Borrowed from Claude Code's `executing actions with care` doctrine. Define which actions are *automatic* vs *prompter-confirmed*:

- Automatic (no confirmation): drafting a new file, writing structural updates, writing critiques, snapshotting, writing edit-observations.
- Confirm first: overwriting an existing draft, modifying POETICS.md, deleting versions, renaming the project, modifying ATTRIBUTION.md.

**Why.** narracode.md says "You do not silently overwrite drafts — every draft is a new file or an explicit iteration." Strengthen this from *prose* to *protocol*.

**Verdict.** **Recommend.**

#### E2. Self-verification pass on drafts (carefully)

**What.** After a Compositional pass, the model performs a *narrow* self-check: did this draft (a) read the named inputs, (b) honor declared refusals, (c) advance the structural state? It writes a one-line `drafts/[N]-checks.md`. **It does not self-critique style.**

**Why.** Catches the cheap failures (forgot to read POETICS.md, named a refused element). Leaves real critique to the Reflexive pass.

**Risk.** Slippery slope toward chained passes. Mitigate by *strictly* limiting checks to mechanical compliance — no aesthetic judgment.

**Verdict.** **Consider, with strict scope.**

### Group F — Status surface

#### F1. A live `STATUS.md` at project root

**What.** A short, auto-regenerated file at project root showing: current loop number, last action taken, pending prompter decision, draft count, last snapshot, last edit-observation. Always under 30 lines. Overwritten every loop — it is *not* history, it is the dashboard.

**Why.** Cold-resumption today means reading POETICS + latest loop-notes + latest draft + latest critique. STATUS.md collapses this into a one-screen orient.

**Verdict.** **Recommend.**

#### F2. An updated `build_site.py` that surfaces all of the above

**What.** The existing `build_site.py` produces a beautiful index. Extend it so each story page also surfaces: current STATUS, the loop journal, expansion alternatives, drift critiques. So the public artifact mirrors the working artifact.

**Verdict.** **Recommend** (small, follows from F1).

### Group G — Toward a real CLI / MCP server (the README's stated future)

#### G1. Specify a thin CLI shape now, even if not built yet

**What.** Sketch the command surface that a real `narracode` CLI would have. Example:

```
narracode init <title> --premise=<...>
narracode draft [scene]
narracode critique [draft]
narracode snapshot [descriptor]
narracode orient
narracode expand [draft] --n=3
```

Map 1:1 to the slash commands in A1. The shape is the contract.

**Verdict.** **Recommend** as a non-binding sketch in `narracode.md` so future implementations have a target. **Do not build the CLI yet.**

#### G2. An MCP server contract sketch

**What.** Sketch what narracode looks like as an MCP server exposing the same tools (`narracode__draft`, `narracode__critique`, etc.) so Claude Code, Cursor, etc. can drive it natively without re-reading `narracode.md` every session. Sketch only — no implementation.

**Verdict.** **Consider.**

---

## 3. What this proposal *does not* do

Restating the boundary, since the user asked for "more agentic" and the temptation is to push past it:

- **Does not let the model chain passes.** No auto-critique-after-draft, no auto-draft-after-snapshot. Every pass remains prompter-initiated.
- **Does not give the model authorship.** It does not propose plot, pick alternatives, or revise its own prose unbidden.
- **Does not interpret prompter hesitation as license.** narracode.md's existing rule stands.
- **Does not introduce coherence as a virtue.** Where the prompter chose breakage, breakage continues.
- **Does not collapse the role separation.** All twelve additions sit *above* or *beside* the role machinery, never inside it.

The only proposed *behavioral* expansions of model agency are:
1. Parallel dispatch on explicit request (C1, C2)
2. Optional plan exchange before drafting (D2)
3. Mechanical-only self-checks (E2)

All opt-in. All bounded.

---

## 4. Suggested implementation sequence

If the plan is accepted (in whole or part), a sane sequence:

| Phase | Items | Effort | Reversible? |
|-------|-------|--------|-------------|
| **1. Restate** | D1 (declare hook surface), A1 (slash aliases), F1 (STATUS.md) | Edit `narracode.md` only | Trivially |
| **2. Extend memory** | B1 (CONTEXT.md), B2 (loop-notes schema) | Edit `narracode.md` + new file conventions | Yes |
| **3. Spec missing roles** | C1 (Expansion agent spec) | Edit `narracode.md` | Yes |
| **4. Add gates** | E1 (permission gates), E2 (self-checks) | Edit `narracode.md` | Yes |
| **5. Opt-in agency** | C2 (parallel dispatch), C3 (double critique), D2 (plan mode) | Edit `narracode.md` | Yes |
| **6. Site surface** | F2 (build_site.py extension) | Edit Python, no harness change | Yes |
| **7. Future-proofing** | G1 (CLI sketch), G2 (MCP sketch), B3 (MEMORY.md) | Edit `narracode.md` | Yes |

Phases 1–4 are tighten-the-existing-screws. Phases 5–7 are net-new capability.

---

## 5. Open questions for jhave

Before any of this gets implemented, four decisions worth making explicit:

1. **Stance on parallel drafting (C2).** It's expensive and changes the rhythm of writing with the harness. Endorse, gate, or refuse?
2. **Stance on plan mode (D2).** Some writers find pre-plans poison the actual draft. Endorse, gate, or refuse?
3. **MEMORY.md (B3).** Useful for novella-length, overkill for shorts. Defer until a long project demands it, or include now as a documented option?
4. **Real CLI (G1, G2).** README says "future iterations will implement a real CLI tool." Is that still the trajectory, or is the markdown harness the intended permanent form?

---

*End of proposal. Awaiting jhave's selections before any edit to `narracode.md` or other artifacts.*
