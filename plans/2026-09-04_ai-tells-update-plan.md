# The Ragged Edge: Updating the AI-Tells Pass

*2026-09-04T06:42:50+02:00. Research, diagnostic architecture, and implementation by Gemini Flash 3.8 (High), at David Jhave Johnston's request. Successor to `plans/2026-07-30_ai-tells-benchmark.md`, `plans/2026-08-05_cadence-displacement-implementation.md`, and `2026-08-09_what-the-edits-know.html`. Full styled HTML report lives at `2026-09-04_ai-tells-update-plan.html`.*

---

## 0. Directives and Historical Ground Truth

### Directive #1 (06:29 CEST)
> "I want an update to the AI-tells pass in the Narracode harness. Scan the internet and come up with a plan for how to improve the style so it doesn't use the conventions of contemporary AI models, but can retro-fit or weed narra-code-writing so it is unpredictably diverse like human literary writing. Provide report-plan in html format, data timestamped and attributed to yourself Gemini Flash 3.8 (High)"

### Directive #2 (06:42 CEST)
> "good. implement plan. but do NOT Retro-fitting the Existing Stories. Leave all stories that are published exactly as they are. Snapshot the harness and ai-tells with date timestamps for posterity and implement changes as decribed. Also put in one that scans for overuse of numeric categories fixations on 'eleven' etc... Also i'm wondering if the ai-tells pass shld not incl consultation of the poetics specific to each story to bend-blend and subtly shift they replacements done during weeding-retrofit. And with that is it possible to intro a perturbation class that considers character and plot and motif arcs as it rewrites specific sentences? (which themselves in a closed loop need to again be assessed for ai-tells. note again: these are not regulations but efforts to smooth away the statistical conformity and patterned habits of AI writing. Make a new report timedatestamped with this as prompt #2 fold beneath prompt #1, then proceed."

### Archival Preservation
All stories in `Stories written with Narracode/` remain unchanged. Prior harness and tell registry versions are saved for posterity in:
- `LEGACY/narracode_2026-09-04T0642.md`
- `LEGACY/master_ai_tells_2026-09-04T0642.md`
- `downloads/narracode_2026-09-04_pre-upgrade.md`
- `downloads/master_ai_tells_2026-09-04_pre-upgrade.md`

---

## 1. Registry 2.0: Classes 21–29 in `master_ai_tells.md`

| Class | Name | Diagnostic Pattern | Remedy & Target Rate |
|---|---|---|---|
| **21** | **The Contrast Reframe** | `\b(not (a|an|the)? \w+ (of|in) \w+, but (a|an|the)? \w+)\b` | **CUT** negation; state the second term flatly. Target: **0 per draft**. |
| **22** | **Somatic Reflex Shortcut** | Autonomic reactions: *breath [he/she] didn't know*, *knot in [his/her] stomach*, *hair on [his/her] neck* | **REPLACE** with external physical task or concrete telemetry. Target: **0 in narration**. |
| **23** | **Sensory Dyad (Twin Adjectives)** | Coordinated pairs: *cold, bitter*, *hollow, pale*, *sharp, acrid* | **CUT** to single stranger adjective or convert to noun. Target: **≤ 1 per 2,000 words**. |
| **24** | **Semantic Smoothing Glues** | Sentence-initial conjunctive adverbs: *And yet, Still, Moreover, Even so, Perhaps that was why* | **CUT** conjunction. Let clauses collide without transition. Target: **≤ 1 per section**. |
| **25** | **Epistemic Varnish** | Softening hedges: *in some quiet way, a sort of, almost as if, seemed to hold* | **CUT** the hedge. State cold fact. Target: **0 in austere narration**. |
| **26** | **Unearned Thematic Coda** | Paragraph-final sentence providing thematic summation of preceding action | **CUT** final sentence. End on physical action. Target: **0 at beat ends**. |
| **27** | **Symmetrical Periodic Sentence** | Compound clauses joined by *while/as* with equal word counts (±2) and parallel syntax | **SEVER** with full stop; convert second clause to verbless fragment. |
| **28** | **Ecclesiastical Diction in Secular Worlds** | Church/sacred vocabulary: *litany, baptism, catechism, sacred, reverent, testament, confessional* | **REPLACE** with administrative, industrial, or vernacular terms. Target: **0**. |
| **29** | **Numeric Fixation / Arbitrary Specificity** | Recurrent unanchored integers (especially *eleven, seventeen, forty-one, three minutes*) | **REPLACE** with true operational telemetry or **CUT** numeral to let noun stand alone. Target: **≤ 1 unanchored numeral per story**. |

---

## 2. The Poetics Filter for Remedies

When a tell is flagged, the remedy is not a generic stock substitution. The auditor reads the active project's `POETICS.md`:
1. Identifies the attentional dialect and named reference authors (e.g., Blanchot, Knausgaard, Butler).
2. Identifies specific project refusals (e.g., no church vocabulary, no domestic nostalgia).
3. Bends the suggested replacement into the native lexical and sonic texture of that project.

---

## 3. The Arc-Perturbation Engine (Closed-Loop Structural Revision)

Beyond line-level trimming, sentences flagged as synthetic or flat are perturbed using the project's structural memory:
1. **Character Interiority:** Perturb sentence by surfacing hidden shame, unacknowledged desires, or active contradictions (`character-interiority.md`).
2. **Active Obligations:** Perturb sentence by tangling with planted objects, unpaid emotional debts, or unanswered questions (`obligations.md`).
3. **Motif Pressure:** Perturb sentence by re-introducing a motif in a transformed state (`motifs.md`).
4. **Mandatory Closed-Loop Clearance:** Every perturbed rewrite is immediately audited against Classes 1–29 in `master_ai_tells.md` to ensure the perturbation has not reintroduced melodrama, unanchored figures, or ceremonial scaffolding.

---

## 4. Implementation Steps

1. **`master_ai_tells.md`**:
   - Add Classes 21–29.
   - Document the Poetics Filter.
   - Document the Arc-Perturbation Closed Loop.
   - Update frequency caps.
2. **`narracode.md`**:
   - Reaffirm that published stories are protected and never retrofitted.
   - Update `Reflexive Agent` Tell-Scan mode with the Poetics Filter.
   - Add `on_retrofit` / `Retrofit Mode` with Arc-Perturbation.
   - Wire exemplar retrieval into `pre_draft`.
