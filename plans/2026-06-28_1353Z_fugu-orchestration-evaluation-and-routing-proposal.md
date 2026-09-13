---
status: proposal
implemented-in: (none — proposal not merged)
tested-on: (none)
---

# Evaluation of Sakana Fugu (orchestration-as-a-model) for Narracode

**Created.** 2026-06-28 13:53 UTC
**Created by.** Claude (Opus 4.8), Narracode harness session
**Source under evaluation.** Fugu Team, Sakana AI, *Sakana Fugu Technical Report*, arXiv:2606.21228 (submitted 2026-06-19, rev. 2026-06-23). Product launch 2026-06-22. Grounded in two ICLR 2026 papers — TRINITY (an evolved ~0.6B LLM coordinator) and Conductor (a 7B RL-trained natural-language orchestrator).
**Target of proposed changes.** `narracode.md` at the project root, plus an optional new routing layer.
**Audience.** The prompter (single human author working with the Initiator / Reading / Structural / Compositional / Reflexive separation).

This document follows the house pattern established by `plans/2026-05-24_continual-harness-evaluation-affect-module-report.md`: state what the source actually is, separate what transfers from what does not, then specify concrete edits. Nothing here is implemented; it is a reading of Fugu *against* Narracode's existing commitments, not a mandate to adopt it.

---

## 1. What Fugu actually is

Fugu is not a frontier model. It is a *learned orchestrator*: a comparatively small language model trained to read a user query and, on the fly, construct an **agentic scaffold** over a swappable pool of frontier worker models (Claude, GPT, Gemini, and instances of itself). The orchestrator handles four things end to end and exposes them behind a single OpenAI-compatible API:

1. **Model selection** — which workers to involve for this specific request.
2. **Delegation / role assignment** — commonly a **Thinker** (deep reasoning, builds the step-by-step plan), a **Worker** (executes — coding, applied generation, prose), and a **Verifier** (checks the result for errors, hallucination, and compliance with the requirements). Roles are assigned dynamically across multiple turns.
3. **Coordination** — how the workers communicate, in natural language, including recursive self-calls to scale test-time compute on hard sub-problems.
4. **Synthesis** — combining the workers' outputs into one coherent answer.

Two design moves matter for us:

- **No fixed harness.** The headline claim is that Fugu does *not* apply a task-specific scaffold. It decides, per request, how to reason, whom to involve, how they talk, and how to synthesize. The scaffold is *emergent and query-conditioned*, not authored in advance.
- **Coordination is learned, not rule-written.** Training is SFT on single-step tasks, then **evolutionary strategies (CMA-ES)** and **RL** on end-to-end tasks. The claim is that a learned coordinator discovers collaboration patterns a human writing routing rules would not encode. Two variants ship: Fugu (latency-balanced) and Fugu-Ultra (quality-first).

The framing Sakana leans on commercially — *hedge against single-vendor dependency; if one provider restricts access, route around it* — is orthogonal to literary quality but, as §5 argues, is the one part that maps cleanly and safely onto Narracode today.

Sources: [arXiv abstract](https://arxiv.org/abs/2606.21228) · [arXiv HTML](https://arxiv.org/html/2606.21228v1) · [Sakana AI — Fugu](https://sakana.ai/fugu/) · [DataCamp explainer](https://www.datacamp.com/blog/sakana-fugu) · [MarkTechPost](https://www.marktechpost.com/2026/06/22/sakana-ai-launches-sakana-fugu-an-orchestration-model-that-routes-tasks-across-a-swappable-pool-of-frontier-llms/) · [VentureBeat](https://venturebeat.com/orchestration/no-claude-fable-5-no-problem-sakana-achieves-frontier-performance-with-new-fugu-multi-model-auto-synthesis-system).

---

## 2. The structural rhyme — and why it is a trap if taken literally

Fugu and Narracode are, at a glance, the same shape. Both wrap a model in a multi-role scaffold and externalize coordination. The role triad even rhymes:

| Fugu role | Narracode analogue | Narracode's existing model assignment (AUTO_MODE) |
|---|---|---|
| Thinker (plans, reasons) | Initiator + Structural agent | Opus 4.7 |
| Worker (executes, generates) | Compositional agent | Sonnet 4.6 |
| Verifier (checks compliance) | Reflexive agent (Critique / Check / Drift) | Opus 4.7 |

Narracode already encodes Fugu's central thesis — *a coordinated multi-role system beats single-shot generation* — and its AUTO_MODE table already does exactly Fugu's headline trick of **role-specialized model assignment** (high-critical-ceiling model on architecture and evaluation, fluent model on prose). On that axis Narracode is not behind Fugu; it independently arrived at the same asymmetry.

But the rhyme conceals the decisive difference, and it is the same one that killed most of the Continual Harness transfer (`plans/2026-05-24...md`, §2):

> **Fugu optimizes against a verifiable objective. Literature has none.**

Fugu's Verifier checks "syntax errors, hallucinations, compliance with requirements," and Fugu is trained by CMA-ES/RL against measurable end-task reward (SWE-Bench Pro, Terminal Bench, LiveCodeBench, GPQA, HLE — all gradeable). Narracode exists *because* the prose that scores highest on any automatic or consensus metric is precisely the failure mode: "competent, fluent, slightly sentimental, slightly explicatory prose that reads like a thousand other models writing about the same thing" (`narracode.md`, final note). The most load-bearing rule in the whole harness is a *negative* one — the `post_draft` silence that forbids the chain into self-critique — because chaining toward agreement is median-collapse (`2026-05-14_architectural_harness_observations-CLAUDE.md`, §1).

So the parts of Fugu that are most celebrated are the parts Narracode must refuse:

- **"Synthesize all outputs into one coherent answer."** Synthesis-toward-coherence is averaging. Run three frontier models on the same scene and blend them and you get the centroid of three training distributions — the exact thing `narracode.md` interrupts. (`narracode.md` is explicit: when drafting in the texture of multiple uploads, "the merge is *not* a blending toward the average.")
- **"Learned coordination via RL/CMA-ES."** There is no computable literary reward to evolve against. The only process-reward signal Narracode has is the prompter's silent micro-edits in the IDE (the Seamless Edit Method), whose grain is one human and whose volume is tiny.
- **"No fixed harness; decide the scaffold per request."** Narracode's fixed scaffold *is the product*. The hooks, the refusals, the forbidden chains are authored constraints whose whole purpose is to *not* let the model default to whatever scaffold it would pick — because its default pick is the fluent one.

Conclusion: adopt Fugu's **routing/role-assignment mechanism**; refuse its **synthesis** and its **learned-reward optimization**. The verifier-as-grader becomes, in Narracode, a verifier-as-refusal-checker.

---

## 3. What transfers

### 3.1 A "local Fugu" routing layer — the part the prompter asked about

The prompter's note — *local Fugu models calling Gemini, Claude, GPT etc. via API* — is the strongest transferable idea, and Narracode is already 80% of the way there. AUTO_MODE hard-codes Opus 4.7 → Initiator/Reflexive, Sonnet 4.6 → Compositional. Fugu's contribution is to make that assignment **a declared, swappable, per-pass routing table** instead of two hard-coded rows, and to let a small *local* coordinator pick the worker per pass.

What this buys Narracode that pure single-vendor AUTO_MODE does not:

- **Heterogeneous strengths per pass.** The passes have genuinely different demands, and different frontier models have different edges:
  - *Structural / orientation passes* are long-context bookkeeping over the whole `structural/` folder — a job for the largest context window and cheapest token (e.g. a Gemini-class model), not the most expensive critic.
  - *Compositional passes* want a specific prose temperament; the prompter may want to A/B the same scene across Claude and GPT and **keep both as `drafts/3-claude.md` and `drafts/3-gpt.md`** — never blend them (the existing `1`/`1b` fork convention already supports this; §3.3).
  - *Reflexive passes* (Critique/Check/Drift against POETICS Refusals) want the highest critical ceiling — Claude Opus class.
- **Vendor-independence as continuity insurance.** This is Fugu's commercial pitch and it is the one that maps without contamination: a long-running literary project should not die because one provider deprecates a model mid-book. A declared routing table lets the prompter re-point a role to a new model and record it in `ATTRIBUTION.md`.
- **Local orchestrator = privacy + cost for the cheap passes.** A small local model (the "local Fugu") can run the deterministic, non-generative coordination — deciding *which* hook fires, *which* role is meant, assembling the context pack for the next pass — without sending the manuscript to any API. Only the passes that need frontier quality call out.

**Crucial constraint that keeps this Narracode and not Fugu:** the local orchestrator routes and *assembles context*; it does **not** synthesize, does **not** vote, does **not** merge worker outputs, and does **not** self-improve against a reward. It is a dispatcher with a fixed, auditable routing table — Fugu's plumbing, with Fugu's averaging organ removed.

### 3.2 The Thinker/Worker/Verifier vocabulary as a sharper name for what AUTO_MODE already does

Fugu's triad is a cleaner public vocabulary for the asymmetry Narracode already exploits. Worth borrowing *as documentation*, not as new machinery: the Structural/Initiator pass is the Thinker, Compositional is the Worker, Reflexive is the Verifier. This makes the model-routing rationale legible to a humanities author who will never read CMA-ES.

### 3.3 Per-worker parallel drafts (multi-model, never merged)

Fugu runs multiple workers and synthesizes. Narracode should run multiple workers and **shelve all of them as siblings** for the prompter to choose between — the move-space-narrowing choice stays human. This is a trivial extension of the existing draft-fork convention (`1`, `1b`): allow a model-suffix (`drafts/3-claude.md`, `drafts/3-gemini.md`). The Reflexive pass may *compare* them in a check file; it may not blend them into a `3-synth.md`.

### 3.4 Recursive test-time compute — only on the Verifier, never on prose

Fugu calls itself recursively to spend more compute on hard sub-problems. The one place this is safe in Narracode is the *Reflexive* pass: a Drift check that finds a suspected genre-regression may recursively re-examine the specific passage at higher scrutiny. Spending more test-time compute on *generation* just produces more polished median; spending it on *detecting refusal-violations* is pure upside.

---

## 4. What does not transfer (explicit refusals)

Logged as refusals so the discipline is named, not assumed (cf. the weight `narracode.md` puts on POETICS Refusals over Commitments):

1. **Output synthesis / blending.** Never merge multiple models' prose toward a coherent centroid. Keep them as forks; the human picks.
2. **Learned coordination (RL/CMA-ES against reward).** No computable literary reward exists; a frontier-teacher relabel would median-collapse the voice. The harness learns only through the Seamless Edit Method, at human grain.
3. **Per-request emergent scaffold.** The fixed hooks, forbidden chains, and Refusals are the product. Do not let the orchestrator invent its own scaffold per scene — its default scaffold is the fluent one the harness exists to interrupt.
4. **Verifier-as-grader.** Fugu's Verifier checks correctness/compliance and scores. Narracode's Reflexive agent already refuses to score ("findings only, no grading"). The routing layer must not reintroduce a numeric quality score as a routing signal.
5. **Hidden/proprietary routing.** Fugu hides which models it used "by design." Narracode must do the opposite: every routing decision is recorded in `ATTRIBUTION.md` and the version's `loop-notes.md`. Authorship attribution is a first-class commitment here.

---

## 5. Concrete proposed edits to `narracode.md`

Minimal, additive, and reversible. None changes the pass semantics; they make routing explicit and auditable.

### 5.1 Promote AUTO_MODE's model table into a standalone, swappable Routing Table

Generalize the existing AUTO_MODE table into a `## Model Routing` section that applies in *all* modes, not just AUTO_MODE, expressed in the Thinker/Worker/Verifier vocabulary, with an explicit "Provider" column and a default + override mechanism:

```text
| Narracode pass            | Fugu role | Default model      | Rationale                                  |
| Initiator / Structural    | Thinker   | (long-context)     | bookkeeping over whole structural/ folder  |
| Compositional             | Worker    | (prose temperament)| may fork across 2 providers, never merged  |
| Reflexive (Crit/Check/Drift)| Verifier| (highest critic)   | checks POETICS Refusals; never scores      |
```

Models are named by the prompter (Narracode must not assume provider availability) and recorded in `ATTRIBUTION.md`. The table is descriptive of intent; the prompter may re-point any row.

### 5.2 Add a `route` resolution step (not a new agent) to `pre_draft` / `on_orient`

Before a pass runs, the harness names — in one line — which role/model the routing table assigns, and why, so the choice is audible (the same self-discipline value the named hooks already provide per the 2026-05-14 observations, §5). One sentence, auto-confirmed. This is the "local Fugu dispatcher" expressed as a declared step rather than an opaque model.

### 5.3 Extend the draft-naming convention for multi-model forks

Document `drafts/[N]-[model].md` (e.g. `3-claude.md`, `3-gemini.md`) as a legal sibling form alongside the existing `3a`/`3b`. Add to `on_draft`: *"Multiple models may draft the same N as siblings. Never write a `-synth` file that blends them; the prompter selects."*

### 5.4 Record routing in attribution and loop-notes

`ATTRIBUTION.md` already lists AI models involved. Add: *which model performed which pass*. `on_snapshot` action 5 (`loop-notes.md`) gains one line: the routing used this loop. This is the anti-Fugu transparency commitment (§4.5) made concrete.

### 5.5 Optional: a recursive Verifier scrutiny note in `on_drift`

Add to `on_drift`: *"If a passage is suspected of genre-regression, the Verifier may recursively re-read that passage alone at higher scrutiny before writing findings."* Test-time compute spent only on refusal-detection, never on generation.

---

## 6. Architecture sketch — "local Fugu" dispatcher (optional future work)

```
                 prompter (natural language)
                          │
            ┌─────────────▼──────────────┐
            │  LOCAL FUGU DISPATCHER       │   small local model, no API egress
            │  • intent → which hook/role  │   • reads routing table
            │  • assembles context pack    │   • records routing in loop-notes
            │  • NO synthesis / NO scoring │   • NO learned reward
            └───┬───────────┬──────────┬───┘
                │           │          │
          Thinker      Worker      Verifier
        (long-ctx)  (prose model) (top critic)
            │           │             │
       structural/   drafts/3-X.md  critiques/check-*.md
       bookkeeping   (forks, never   (findings only,
                      merged)         never scored)
```

The dispatcher is Fugu's *plumbing* with its two contaminating organs removed (synthesis; learned reward). It is worth prototyping only if the prompter actually wants multi-provider routing; for a single-vendor session the existing AUTO_MODE table is sufficient and this adds nothing.

---

## 7. Recommendation

- **Adopt now (doc-only, zero risk):** the Thinker/Worker/Verifier vocabulary (§3.2), the generalized Routing Table (§5.1), multi-model draft forks (§5.3), and routing transparency in attribution (§5.4). These formalize what AUTO_MODE already does and directly answer the prompter's "local models calling Claude/Gemini/GPT" question.
- **Prototype only if multi-provider routing is wanted:** the local dispatcher (§6) and recursive Verifier scrutiny (§5.5).
- **Refuse permanently:** output synthesis, learned-reward coordination, per-request emergent scaffolds, verifier-as-grader, and hidden routing (§4).

The one-line summary: **Fugu is the right answer to a question Narracode is not asking.** Fugu maximizes a verifiable objective by averaging many models; Narracode minimizes the move-space by refusing the average. Take Fugu's routing table and its honest vocabulary; leave its synthesis engine and its reward loop at the door.

---

## Meta-note

Like the Continual Harness evaluation before it, the fertile transfer here is not the algorithm but a *separation*: Fugu separates the coordinator from the workers and makes routing a first-class, swappable decision. Narracode can take that separation, make it auditable rather than proprietary, and bolt it onto the asymmetry it already trusts — without importing the optimization target that would dissolve the voice the harness exists to protect.
