# AI-tells reassessment: preserve the range of writing

2026-09-07 · Research and critique by Codex (GPT-6), for David Jhave Johnston. Initial planning pass; obvious contextual-method corrections applied September 7 at the author’s request. Pilot implementation paused unfinished. Research accessed September 7, 2026.

**The author's clarified goal:** “write with the flexibility of human literary voice. Without the tropes of LLMs.” Success means a wider available range of literary attention and expression, with fewer unchosen model habits. Neither detector evasion nor a recognizable anti-AI style is the objective. The Pangram experiments below are optional research; they are not prerequisites for improving the harness.

The useful next version of Narracode should become better at recognizing when a device has stopped doing useful work. The September 4 update instead makes several devices inadmissible. Its combination of zero targets, mandatory simplification, and recursive clearance risks teaching every project the same clipped, concrete, secular voice. Preserve the edit archive, project poetics, structural memory, and human choice; replace universal prescriptions with contextual evidence and reversible experiments.

## What was actually inspected

The requested [September 4 HTML report](../2026-09-04_ai-tells-update-plan.html), its [Markdown companion](2026-09-04_ai-tells-update-plan.md), and the exact [ZIP linked from that page](../downloads/narracode_Sep-4-2026.zip) were read. The quoted historical requests on that page are source material for this critique, not new authorization to implement their instructions.

The ZIP has six Markdown files: `narracode.md`, `master_ai_tells.md`, `README.md`, `FAQ.md`, `master_poetics.MD`, and `master_phrases_to_avoid.md`. SHA-256: `6d5ebb2cff3b9366cfe3142c85df281a5629ea036ef22cb117147cc47bafa60e`.

After synchronization, `main` is `47deb1c9567df32fa0bfe323b7d263a2f5c79836`. Its harness, README, FAQ, and master poetics match the ZIP byte for byte. Its tell registry and phrases file differ. The ZIP has 29 classes; current main adds classes 30–31, September 5 examples, and the “Law of Simplicity.” The harness still hard-codes classes 1–29 in tell-scan instructions.

All 17 current remote branches have matching local branch tips. Main and three existing story branches were fast-forwarded; 13 missing local tracking branches were created. Local branches whose upstreams disappeared, and branches without upstreams, were retained. Branches were not merged into one another. The checkout remains on main.

## Critique of the update

**Its strongest idea is situated revision.** Consulting a story's poetics and established relations is much better than replacing words from a blacklist. Keeping before/after examples is valuable because an example can carry distinctions the prose description misses. The registry also correctly notices that remedies become habits. These strengths should govern the revision.

**Its operational rules defeat those strengths.** “A tell that is load-bearing stays” conflicts with “zero per draft” and rewriting until cleared. The poetics filter cannot protect a lush, prayerful, comic, uncertain, or deliberately repetitive project when global rules prohibit its materials. September 5's simplicity principle records useful feedback on *Impossible Persistent*; elevating it to a universal law would erase other projects' intentions.

**The proposed replacements have their own narrow aesthetic.** Bodies become tools; doubt becomes fact; transitions disappear; balanced sentences become fragments; numbers become server telemetry. This is a coherent style, but there is no evidence that it is a general account of human literary writing. “320ms” and “1731” are no more grounded than “eleven” unless the story establishes why a perceiver knows and attends to them.

**Structural pressure can become compulsory plot loading.** The example that substitutes an envelope, oath, named person, and ferry for waiting at a window changes far more than cadence. Those facts require existing support or an explicit proposal to alter the story. Inserting shame or a motif whenever a sentence is weak makes every detail significant and every scene indebted. Some writing needs idle attention, unrewarded detail, plain reporting, comedy, or a character who temporarily forgets the plot.

**The clearance loop lacks a stopping rule.** Repeatedly optimizing the same critic's judgment can remove every detectable shape while converging on that critic's preferred shape. A second assessment should name benefits and damage, retain unresolved cases, and allow the original to win. It should not certify that a sentence is free of AI.

**The package overstates completeness.** This is a prompt distribution, not a standalone detector or executable perturbation engine. It omits the corpus and tools. `pre_draft` requests 6–8 verified edit pairs from `corpus/edit_pairs.jsonl` or story versions, neither of which is included. The merged corpus actually lives at `corpus/all_pairs.jsonl`. Fallback behavior, example selection, provenance filtering, and passage eligibility need specification.

**Detection descriptions mix different kinds of judgment.** A regex can retrieve a phrase; it cannot establish focal authority, earned emotion, thematic redundancy, or narrative function. Class 27 also conflates syntactic relations: *while* and *as* need not join independent, coordinate clauses. In a direct check, the documented class-21 regexes matched “It was not malice, but exhaustion” but missed their own example “Not a collapse, but a settling,” even with case-insensitive matching. Candidate retrieval and editorial verdict must be separate.

## Evidence that needs correction

The [August 9 report](../2026-08-09_what-the-edits-know.html) says its surviving measures describe about 9% of **689 edits with text on both sides**, within a corpus of 1,234 edits across nine stories. Both counts were verified in `corpus/all_pairs.jsonl`. The September report turns this into a claim about 1,234 edits and treats everything unmeasured as a known class of sophisticated textural substitution. A residual is not a measured taxonomy. Report the denominator and call the remainder unexplained by those measures.

The same August report explicitly withdraws sentence-length variation as a useful signal after normalization. The [August 6 decision](2026-08-06_step2-result-and-decision.md) says the cadence vector must never become a generation target or gate. September's recommendation to manufacture local perplexity spikes revives that direction without a new experiment. Its claims about a 12–22-word metronome, minimization of perplexity variance, and integers from a “low-loss latent pocket” are unsupported mechanistic explanations in the material examined. Treat them as hypotheses, not established model behavior.

The August decision itself needs one correction: failure to move its four surface measures cannot prove failure to improve the unmeasured writing. Its proposed automatic kill-switch rests on precisely the proxy assumption it elsewhere rejects. Lower edit counts also cannot distinguish improvement from blandness, reader fatigue, or reduced ambition.

Three September bibliography entries need repair:

| September entry | Verified record and implication |
|---|---|
| Kobak et al., PNAS, 2024–2025 | The paper became *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*, **Science Advances**, 2025. Population-level vocabulary changes in biomedical abstracts do not validate a fiction sentence blacklist. [Record](https://arxiv.org/abs/2406.07016) |
| Meister, Pimentel & Cotterell, “Revisiting Uniform Information Density in Language Models,” ACL 2024 | The matching work is Meister **et al.**, *Revisiting the Uniform Information Density Hypothesis*, **EMNLP 2021**. It examines human reading and acceptability; it does not establish that literary humanity increases with irregular surprisal. [Paper](https://aclanthology.org/2021.emnlp-main.74/) |
| Bhattacharjee et al., “GPT-Who: Information-Density Morphometry…,” EMNLP 2025 | The verified work is **Venkatraman, Uchendu & Lee**, *GPT-who: An Information Density-based Machine-Generated Text Detector*, **Findings of NAACL 2024**. It provides an interpretable statistical comparator, not a literary quality objective. The cited 2025 title/authorship was not verified. [Paper](https://aclanthology.org/2024.findings-naacl.8/) |

## What underlies Pangram

The original Pangram is a supervised transformer classifier. Its distinctive training procedure is **hard-negative mining with synthetic mirrors**: identify human passages the detector misclassifies, generate AI counterparts on similar subject matter, and retrain with those difficult contrasts. This aims to reduce topic shortcuts. [Emi & Spero, 2024](https://arxiv.org/abs/2402.14873)

Its 2025 shared-task system additionally mined misclassified AI examples from RAID and paired them with their human counterparts. Hard-example selection is therefore a training strategy, not a list of forbidden prose patterns. [Emi, Spero & Masrour, 2025](https://aclanthology.org/2025.genaidetect-1.40/)

**Pangram 4, July 2026:** a causal mixture-of-experts backbone, adapted with LoRA; a 15-bucket segment head; three-way human/assisted/generated token predictions; mixed-authorship and humanizer heads. Repeat2 duplicates each window internally so supervised token representations can use the full window. Inference uses 512-token windows with 256-token stride. Calibration and a linear-chain conditional random field combine evidence; Viterbi decoding, sentence-majority voting, and minimum-run merging produce displayed segments. Confidence comes from the earlier probabilistic decoding, so it is not a recalibrated probability that the final displayed label is correct. Backbone identities are anonymized. [Glickenhaus et al., *Pangram 4 Technical Report*, §§4.1–4.3](https://arxiv.org/html/2607.27183v1)

Pangram reports a 0.0041% false-positive rate on two million held-out pre-2022 human documents and a 0.3396% false-negative rate on its synthetic benchmark. These are vendor benchmark results, not estimated error rates for Narracode. Its overview acknowledges that a passage's classification can change when read alone versus in context. [Pangram technical overview, July 29, 2026](https://www.pangram.com/blog/pangram-4-technical)

Those are algorithmic components and provenance categories. They do not establish interpretable expert “modes” such as a poetry expert or a whimsy detector.

## Can it be reverse-engineered?

**Partially, at the behavioral level.** Much of the pipeline is already described publicly. We could implement a related research classifier and probe the live system with controlled variants. Neither would recover the production model's exact weights, learned features, training corpus, or decision boundary from a handful of scores. A local surrogate must be called a surrogate.

Proposed experiments should estimate *how a documented endpoint responds to specified edits*. A score decrease is evidence about that endpoint under those conditions. It does not show why the neural network changed its judgment, prove human authorship, or establish that a passage improved.

This distinction matters for revision: feeding every draft through an adaptive detector-minimization loop would make Pangram an uncredited co-editor. Instead, freeze candidates, obtain literary judgments without detector scores, then measure detection separately. Keep model/version, date, raw returned fields, text hash, offsets, context, and transformation history. Record unavailable fields as unavailable. No Pangram API tests or manuscript submissions were performed in this planning pass.

## Research worth using

| Research | Useful finding | Proposed use and limit |
|---|---|---|
| [Dugan et al., RAID, ACL 2024](https://arxiv.org/abs/2405.07940) | Detector performance changes with domain, generator, decoding, and attacks. | Hold out whole stories and generator families. Use multiple lengths and contexts. The 2024 results are not a verdict on Pangram 4. |
| [Baumler et al., *Can You Make It Sound Like You?*, 2026](https://arxiv.org/abs/2604.24444) | In a preregistered study of 81 participants, post-editing moved text toward personal style but retained measurable LLM resemblance and reduced diversity. | Compare post-editing against fresh composition from human scene notes. Embedding similarity is an imperfect proxy; this is not evidence that ambitious literary revision cannot succeed. |
| [Doshi & Hauser, Science Advances, 2024](https://doi.org/10.1126/sciadv.adn5290) | AI ideas improved evaluated individual stories while making the collection more similar. | Assess the range across projects as well as quality within a passage. The experiment concerns short-story ideation, not this harness or current models. |
| [Narracode's August 6 correction](2026-08-06_stylometric-comparison-correction.md) | Rare words and several aggregate markers moved similarly under human and machine revision; the report withdrew its “human rarity” interpretation. | Measure rhetorical function and revision damage. Do not optimize rare words, dash removal, or lexical diversity as substitutes for voice. |

The useful research program concerns preservation of intention and range, alongside detection robustness. None of these studies supplies a recipe for excellent sentences.

## Registry revision to propose

Preserve class IDs for historical audits, but give every entry: observed pattern; source and date; project scope; confidence in the evidence; known counterexamples; possible narrative function; optional interventions; and an explicit **KEEP / UNCERTAIN** outcome. A global registry stores observations. A project's poetics determines whether an observation matters there. Current user direction can change that project intention.

| Classes | Proposed treatment |
|---|---|
| 21, contrast | Diagnose repeated rhetorical correction. Keep genuine correction, denial, comic argument, or an unreliable speaker's habit. |
| 22, bodily reflex | Flag stock emotional shorthand in context. Permit autonomic experience and direct feeling. Manual labor is one possible alternative, not the default. |
| 23, adjective pairs | Look for interchangeable description and recurring cadence. Paired adjectives can carry necessary distinctions or pleasure. |
| 24–25, transitions and hedges | Ask whether they express inference, uncertainty, social tact, rhythm, or a relation between ideas. Cutting can falsely strengthen knowledge. |
| 26 / 19 / 30, endings | Group overlapping evidence so one ending is not counted three times. Judge the actual ending's function; retain earned generalization, refrain, punchline, or unresolved abstraction. |
| 27, symmetry | Diagnose repeated rhythmic sameness across a passage. Permit symmetry, sustained music, and long periodic syntax. |
| 28, religious diction | Make it a project-specific concern about inflated solemnity. Secular characters can have religious memories and metaphors. |
| 29, numbers | Audit why precision is noticed and whether numbers repeat mechanically across projects. Keep ritual, obsession, miscounting, comic precision, and operational facts. |
| 31, opening pronoun | Ask whether ambiguity is accidental or purposeful and whether context already resolves it. Naming every actor immediately can destroy delayed recognition. |
| Earlier classes and remedy caps | Reassess them too: triads, direct emotion, repeated names, and procedure are not inherently synthetic. Preserve dated rates as observations, not quotas. |

Add **counterexamples before more classes**. Include accepted human uses of the supposedly suspect devices. A rule that cannot tolerate a successful human example is a style restriction and should be labeled accordingly.

## Perturbations to test

These are experimental choices, never a rotation schedule or a requirement to make each paragraph weird. Start with a diagnosed weakness and retain an untouched candidate.

| Intervention | Literary question | Paired test |
|---|---|---|
| Attention | What does this perceiver notice that this draft overlooks? | Change the attended detail while retaining the event and viewpoint. |
| Epistemic distance | What can this voice know, guess, misunderstand, or refuse to say? | Compare a justified hedge with a confident assertion; inspect lost uncertainty. |
| Temporal scale | Where is duration earned? | Expand one action or compress an interval without manufacturing a deadline. |
| Social language | Who owns this phrase, and whom is the speaker addressing? | Change diction because the relationship changes; preserve culturally meaningful irregularity. |
| Syntax and sound | What pressure gives this rhythm a reason? | Try extension as well as compression; retain useful repetition and aloud-tested sound. |
| Arc or motif | Would an established obligation actually intrude here? | Surface, suppress, or transform one existing pressure; log any proposed new fact separately. |
| Directness | Has the concrete image become evasive decoration? | Try plain emotion or explanation as well as a cut. |
| Fresh composition | Is the draft's prior structure anchoring the edit? | Compose anew from human scene facts and poetics without showing the old prose; compare as a separate condition. |

For behavioral probes of Pangram, separately compare identical target passages in isolation and with authentic surrounding context; punctuation-only variants; removal of one repeated construction; and substantial voice-preserving edits. Keep nearby text fixed where possible and report every candidate, including failures. Context sensitivity is a measurement condition, not an invitation to splice camouflage into stories. Do not infer feature causality from the highlighted sentence alone.

## To-do list, in order

1. **Correct the specification and source record.** Add a dated correction to the September report; preserve the original historical claims. Correct citations and denominators, mark unsupported mechanisms, reconcile 29/31 references, and document ZIP dependencies. Deliverable: a reviewable documentation diff and a versioned manifest.
2. **Replace global prohibitions with contextual registry entries.** Start with 21–31 and all remedy caps, then revisit 1–20. Remove automatic simplicity and clearance as universal rules. Deliverable: positive, negative, and uncertain examples for each revised entry, with provenance and project scope.
3. **Audit retrieval before adding another subsystem.** Use the merged corpus; inspect immediate, cumulative, and published-pair provenance separately. It currently contains 820 immediate, 324 cumulative, and 90 published pairs; those labels alone do not prove pure human revision. Choose examples by relevant editorial problem and compatible poetics, with diverse remedies. Exclude the test story and all its versions. Record selected pair IDs, avoid importing plot nouns, and supply KEEP examples. Missing evidence should produce an empty retrieval result, not invented pairs.
4. **Specify a bounded revision pass.** Produce the original and at most two motivated alternatives for a selected passage. Run one subsequent assessment covering continuity, voice, rhythm, knowledge, and new habits. If neither alternative helps, retain the original or leave it unresolved. These limits control work, not literary style. Distinguish candidate files from accepted drafts and log decisions.
5. **Run a small blind pilot before broad implementation.** Use 12 passages, 200–450 words, from at least six projects spanning deliberately different poetics. Compare untouched baseline, exact September 4 procedure, current September 5 procedure, and the proposed contextual approach. Keep source inputs, model settings, and edit instructions logged. A small separate subset can compare fresh composition from scene notes. Treat this as exploratory, not enough to validate rare detector errors.
6. **Evaluate literary effects first.** Randomize presentation and conceal procedure labels and detector scores. Ask which version is preferable, what must be kept, what was damaged, and whether the voice became generic. Permit ties and disagreement. Use more than one reader where feasible; the author retains final artistic choice. Track edit time and accepted changes as secondary measures. Separate each story's outcome so a sparse register cannot conceal harm to a luxuriant one.
7. **Measure detector behavior after freezing the pilot.** Use a fixed Pangram endpoint and one reproducible comparator such as GPT-who, calibrated for its own use. Test provenance-labeled human originals, model drafts, human-edited model prose, and model-edited human prose separately. Published Narracode is often mixed provenance and must not be relabeled purely human. Report false positives/negatives only on defensibly labeled groups, with denominators and uncertainty. Mixed cases need their own analysis. A small corpus cannot substantiate a 1-in-24,000 error claim.
8. **Decide with a fresh holdout.** Advance the approach if blind preferences favor it and the per-story review shows preserved distinctive features without systematic flattening. Define the practical preference margin with the author before testing. If only detector scores or surface counts improve, do not promote it as a literary improvement. Reassess on untouched stories before changing the default harness.

Store experimental inputs, candidates, selections, source hashes, and observations separately from published stories. Do not train retrieval on evaluation outcomes until that evaluation is closed. Confidence intervals should respect grouping by story; adjacent excerpts and successive versions are not independent samples.

## Proposed operating sentence

> Flag a construction only when the surrounding passage gives a reason to question its function. Consult the project's poetics and relevant human edits. Preserve useful repetition, uncertainty, ornament, directness, and irregularity. Offer a reversible alternative or keep the original. Record what the intervention gains and what it costs.

The first implementation should be a correction and a small contextual audit pilot. A new detector, a larger blacklist, and autonomous manuscript retrofits can wait for evidence that the simpler change helps.
