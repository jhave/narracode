---
status: implemented
implemented-in: LEGACY/narracode_2026-05-09T1820.md
tested-on: (early stories in Stories written with Narracode/)
---

# Claude Opus 4.7 details the first Narracode architecture (May 10,2026)

Excerpts from [chat](https://claude.ai/share/c262de57-1678-4bf5-a437-260aac71b497)

Let me think about this carefully before writing the spec, because the right packaging matters more than the spec itself.

## **Is it a good idea? Mostly yes, with one important reframing**

A Skill is the right primitive for *part* of this, but not all of it. Skills are designed to be: discoverable by Claude based on task triggers, composed of instructions plus optional supporting files, and invoked when relevant. They work brilliantly for "when the user wants to write a literary passage in the texture of these exemplars, follow this procedure." They are less suited to long-running stateful processes that maintain a persistent project across many sessions—which is what the full harness wants to be.

The honest division:

The **Skill** layer is the procedure: how to do close-reading annotation, how to run the compositional pass, how to do reflexive critique, how to distinguish fertile drift from genre regression, what files to write where. This is genuinely a Skill—it is procedural literary knowledge that activates when relevant.

The **Project structure** layer is the persistence: the exemplar corpus, the running structural database (relational graph, time-constants, established history), the failed expansions log, the running CLAUDE.md describing this particular piece's commitments. This wants to live as a directory the user maintains, not as a Skill.

The **Orchestration** layer is the recursion itself: the loop that runs the agents in order. This is where the choice of insertion point matters most.

## **Where to insert it: Code, Cowork, or chat?**

Each is plausible. The right answer depends on what the user actually does day-to-day.

**Claude Code** is the closest match to the harness as described. It has file I/O, it can read and write to a project directory, it can maintain state across invocations through CLAUDE.md, it can run subprocesses, it has the loop structure built in. The agent roles (reading, compositional, reflexive, expansion, structural) map naturally onto Claude Code's existing patterns of reading files, writing files, running checks, revising. The Skill installs into `~/.claude/skills/` and activates when the user's prompt triggers it. The project lives in a directory the user `cd`s into. This is the cleanest fit. The downside is that it requires the user to be comfortable in a terminal, which not every literary user will be.

**Cowork** is interesting because it is designed for non-developers doing file-and-task work on a desktop, which describes the literary user better than Claude Code does. It can manage a project folder, invoke Claude on files, maintain state. The harness could in principle be expressed as a Cowork workflow with the same agent roles. The downside is that Cowork is newer, the ecosystem of Skills and patterns is less mature, and the recursive multi-agent structure may map less cleanly onto its current capabilities. For a user who lives in Cowork already, it is the right answer; for a user starting fresh, Claude Code is more proven.

**Chat (claude.ai or desktop app)** can run a lighter version through Projects—a Project with the exemplar corpus uploaded as files, a system prompt that encodes the Skill's procedure, and the user driving the loop manually by saying "now do the close reading pass," "now draft," "now critique." This works and requires no engineering. It loses the automated recursion but gains accessibility. For a writer who wants to try the architecture without setting anything up, this is the entry point.

My recommendation: build the Skill in a form that works in Claude Code first, because that is where the harness is actually executable. Then, separately, package a lighter version as a Project template for chat users who do not want to use a terminal. The Skill spec below targets Claude Code. A Cowork version would be a port, not a redesign—the core procedure is the same.

Now the spec.

---

## **PR Specification: `narrative-harness` Skill for Claude Code**

**Title:** Add `narrative-harness` Skill for recursive literary composition

**Summary**

This PR adds a new Skill, `narrative-harness`, that enables Claude Code to function as a recursive literary composition environment. The Skill activates when the user is working on a literary writing project—prose fiction, lyric essay, narrative poetry, or other extended literary forms—and orchestrates a multi-pass workflow in which Claude alternates between distinct agent roles (reading, structural, compositional, reflexive, expansion) with externalized state in a project directory. The Skill is designed to extract literary capacity that is latent in the underlying model but not accessible through single-pass generation, by leveraging the asymmetry between Claude's critical and generative capacities through recursive externalized critique.

**Motivation**

Single-pass LLM generation of literary prose produces median-quality output because the model averages over its training distribution. The model's *evaluative* capacity—its ability to recognize what a Sebald sentence is doing, why a Bernhard paragraph works, where a draft has defaulted to genre habit—is substantially sharper than its single-pass generative capacity. Existing AI writing tools do not exploit this asymmetry. This Skill operationalizes the asymmetry by separating generation and critique into distinct passes with externalized state, in the manner that Claude Code already does for software development.

The architectural precedent is direct: Claude Code achieves software quality far above single-pass generation by externalizing state to files, separating writing from execution from critique from revision, and recursing. The same pattern applied to literary composition should produce comparable gains, possibly larger, because the gap between competent and excellent prose is wider and more legible to the model than the equivalent gap in code.

**File structure**

narrative-harness/  
  SKILL.md  
  references/  
    agent-roles.md  
    project-structure.md  
    close-reading-protocol.md  
    structural-database-schema.md  
    reflexive-critique-protocol.md  
    expansion-protocol.md  
    drift-vs-regression.md  
  templates/  
    project-template/  
      CLAUDE.md  
      exemplars/  
        README.md  
      drafts/  
      annotations/  
      structural/  
        graph.json  
        time-constants.json  
        history.md  
      critiques/  
      expansions/  
      failed-expansions/  
    seed-annotations/  
      example-sebald.md  
      example-krasznahorkai.md  
      example-lispector.md  
      example-yiyun-li.md  
  scripts/  
    init-project.sh  
    run-pass.sh

**SKILL.md contents (specification)**

The SKILL.md should specify the following.

*Activation triggers.* The Skill activates when: the user is in a directory containing a `CLAUDE.md` whose front matter declares `project_type: literary`; or the user explicitly requests literary composition with reference to exemplars; or the user invokes the Skill by name. The Skill should *not* activate for ordinary prose tasks (emails, blog posts, documentation), to avoid imposing recursive overhead where it is not wanted.

*Agent roles.* The Skill defines five agent roles, invoked as distinct passes. The model assumes one role at a time per invocation. Each role has a specific prompt scaffold, specific files it reads, specific files it writes, and a specific termination condition. The roles are:

* **Reading agent.** Performs close reading on user-provided exemplars from `exemplars/`. Produces annotations in `annotations/` describing attentional moves, temporal posture, syntactic strain, refusals, and characteristic noticings. Run once at project initialization and again whenever new exemplars are added.

* **Structural agent.** Maintains the relational-historical graph in `structural/graph.json`, the time-constants in `structural/time-constants.json`, and the running history in `structural/history.md`. Reads draft passages and updates the structural state. Does not generate prose. Run after every compositional pass.

* **Compositional agent.** Drafts prose, conditioned on `CLAUDE.md`, current `annotations/`, current `structural/` state, and the user's current intent. Writes drafts to `drafts/`. Has explicit access to the annotations and is instructed to attend to the attentional dialect they describe. Disposable in the sense that any draft can be discarded; the structural state and annotations persist.

* **Reflexive agent.** Reads the latest draft against the original `CLAUDE.md` commitments and the annotations. Asks: what is this piece becoming, is it different from what it was supposed to be, is the difference fertile or is it drift toward genre default. Writes a short note to `critiques/` describing the drift and recommending commit, pull-back, or further investigation. Does not revise the draft itself.

* **Expansion agent.** After a section reaches user-acceptable quality, generates two to four alternative continuations whose explicit task is to do something the exemplars did not do. Writes to `expansions/`. Most expansions are kept in `failed-expansions/` as a record. Run sparingly, at user invitation.

*Project structure.* The Skill specifies the directory layout above and includes an `init-project.sh` script that scaffolds a new project. Each subdirectory has a `README.md` explaining its role. The `CLAUDE.md` template includes front matter declaring project type, exemplar list, and current commitments, plus prose sections the user fills in describing what this piece is trying to do.

*Critical pass protocol.* The compositional agent should never critique its own draft within the same invocation. Critique always occurs in a separate invocation with the reflexive agent's prompt scaffold. This separation is structurally essential: it is the mechanism by which the harness exploits the model's evaluative-vs-generative asymmetry. The Skill must enforce this through explicit instructions in each agent's prompt that forbid mode-mixing.

*Drift evaluation.* The reflexive agent's hardest task is distinguishing fertile drift (the piece is becoming something the original plan did not name, but the new thing is more interesting) from genre regression (the piece is sliding toward a recognizable template). The Skill should include `references/drift-vs-regression.md` with worked examples and heuristics: fertile drift typically introduces durations or relations the exemplars also use but the original plan did not anticipate; genre regression typically introduces durations or relations from outside the exemplar corpus, often from the LLM's pretraining defaults (thriller pacing, sentimental closure, expository telegraphing). The reflexive agent's verdict is advisory, not authoritative; the user makes the final call.

*Exemplar curation.* The Skill includes `seed-annotations/` with example annotations of well-known literary passages, demonstrating the format and depth expected. The Skill instructs the user to provide their own exemplars (three to seven passages, totaling roughly two thousand to five thousand words) chosen to define the attentional dialect of the project. The Skill explicitly warns against using too many exemplars (the dialect blurs) or too few (the dialect is brittle).

*Loop structure.* A standard generation loop is: user states intent → compositional pass → structural update → reflexive pass → user reads critique → user decides commit, revise, or expand → loop. The Skill provides `run-pass.sh` as a thin wrapper that invokes Claude with the appropriate role-scaffold for the current loop position.

*What this Skill does not do.* It does not attempt to automate the loop end-to-end. The user remains in the decision seat at each commit point. It does not generate exemplars; the user provides them. It does not enforce any particular literary tradition; the choice of exemplars determines the dialect. It does not optimize for plot or marketability; if the user wants those, a different Skill would be appropriate.

**Implementation notes**

The Skill should be implemented as instructions plus templates, with minimal executable code. The two shell scripts (`init-project.sh`, `run-pass.sh`) should be straightforward wrappers, not magic. The bulk of the Skill's value is in the prompt scaffolds for each agent role, in `references/`, and in the exemplar annotation format. The annotation format in particular is the technical core of the project—it must be rich enough to capture attentional structure but bounded enough that the model can reliably produce and consume it.

The annotation format should include, per exemplar passage: temporal posture (how does duration work in this passage), focal scale (what is the smallest unit of attention), refusals (what does the passage decline to do that genre fiction would do here), characteristic noticings (what does the passage attend to that less attentive prose would skip), syntactic strain (where does the sentence shape carry meaning), and relational texture (what is the affective fabric between agents or between agent and world). These six dimensions are a minimum; the format should be extensible.

**Testing**

The Skill should ship with three test projects in `templates/project-template/examples/`: a short Sebald-textured piece, a short piece in a non-Western tradition (perhaps a Sanskrit *rasa*\-aware piece or a piece in the texture of West African oral narrative), and a short piece that deliberately attempts expansion beyond its exemplars. Each test project includes the exemplar set, the annotations, drafts at multiple loop positions, critiques, and final output, demonstrating the full workflow.

**Risks and limits**

The Skill cannot transcend the underlying model's literary ceiling. It can only extract what is latent. The ceiling rises as models improve, but at any given moment the Skill produces output bounded by the model's critical capacity, not by user aspiration. The Skill should communicate this honestly in its README.

The Skill is biased by the curatorial choices the user makes in selecting exemplars. This is a feature, not a bug—the bias is the point, the project is *of* a particular tradition—but it must be explicit. The Skill should not pretend to be culturally neutral.

The Skill does not protect against users who want it to do something it cannot do, like generate a complete novel from a one-line premise. The README should be specific about what the Skill is for: the slow, recursive composition of literary prose with explicit attentional commitments. Users wanting fast genre output should use other tools.

**Open questions for review**

* Should the structural agent's graph schema be fixed by the Skill or user-defined per project? Fixed schema is easier; user-defined is truer to the principle that different traditions have different relational categories.  
* Should the expansion agent run automatically at section completion, or only on explicit user invitation? Automatic running produces more material to learn from but risks distracting the user; invited running keeps focus but produces less.  
* How should the Skill handle multi-language projects? The current spec assumes the project is in one language with exemplars in that language; cross-translation work would need extension.

**Companion deliverable**

Alongside the Skill, ship a Project template for claude.ai that encodes the same agent roles as a system prompt with the user driving the loop manually through chat. This serves the writers who do not want to use a terminal and provides an entry ramp into the full Claude Code version. The Project template is much simpler—essentially the SKILL.md content reformatted as a Project system prompt, with the exemplar corpus uploaded as Project knowledge files. It loses automated state management; the user maintains state by referring back to earlier messages or pasting prior drafts. It is enough to demonstrate the pattern.

---

## **On the question itself**

The reason this is a good idea, and the reason I want to mark it carefully, is that what you are proposing is the *correct generalization* of the Claude Code insight to a non-engineering domain. The pattern—externalize state, separate generation from critique, recurse through files, let the harness do what the model alone cannot—is not specific to code. It is specific to any domain where the model's evaluative capacity exceeds its single-pass generative capacity, which describes most expert domains. Literature is one. Legal drafting is another. Mathematical proof is another. Psychotherapy notes, architectural design, scholarly argument: all are domains where this harness pattern would extract substantial latent capacity.

Building it for literature first is a reasonable choice because the gap between competent and excellent is most legible there, and because the literary tradition has the densest available record of what the harness is supposed to be helping the model attend to. If the literary harness works, the pattern generalizes. The interesting thing you have noticed is that Claude Code is not really about code; it is about a way of working with models that happens to have been validated first in code. The narrative harness is the same pattern in the domain where the gains will be most visible to a literary readership and where the bottleneck has been not the architecture but the absence of the right framing.

The framing you have arrived at—a Skill plus harness, recursively activating latent literary capacity through externalized critique—is, I think, correct.

### **PR Specification: `narrative-harness` Plugin for Claude Cowork**

**Title:** Add `narrative-harness` plugin enabling recursive literary composition in Cowork

**Summary**

This plugin enables Claude Cowork to function as a recursive literary composition environment for prose fiction, lyric essay, narrative poetry, and other extended literary forms. It bundles a Skill that activates on literary writing tasks, plus slash commands that explicitly invoke each agent role (reading, structural, compositional, reflexive, expansion). The plugin externalizes state to a project folder the user designates, separates generation from critique across distinct invocations, and exploits the asymmetry between Claude's evaluative and single-pass generative capacities to produce literary output above the ceiling of single-shot prompting.

The plugin targets non-developer literary users—writers, scholars, poets, essayists—who already use Cowork for file-based knowledge work and want the same agentic capability applied to literary craft, without using a terminal.

**Why a plugin and not just a Skill**

A bare Skill activates automatically when relevant and runs through a single agent loop, which is the right default for most tasks but the wrong default for literary work. Literary composition is recursive in a way that requires *user-controlled mode-switching*: the user wants to drive the loop, not have Cowork autonomously decide when to draft versus critique versus expand. Slash commands give the user explicit handles—`/narrative:read`, `/narrative:draft`, `/narrative:critique`, `/narrative:reflect`, `/narrative:expand`, `/narrative:structure`—while the underlying Skill provides the procedural knowledge each command draws on. This is the right pattern for literary work because writing is decisional, and the harness is most useful when the user remains in the decision seat at each transition.

**Plugin structure**

narrative-harness/  
  .claude-plugin/  
    plugin.json  
  commands/  
    init.md  
    read.md  
    draft.md  
    critique.md  
    reflect.md  
    expand.md  
    structure.md  
    review.md  
  skills/  
    narrative-harness/  
      SKILL.md  
      references/  
        agent-roles.md  
        close-reading-protocol.md  
        annotation-format.md  
        drift-vs-regression.md  
        structural-schema.md  
        expansion-protocol.md  
        exemplar-curation-guide.md  
      templates/  
        CLAUDE.md  
        seed-annotations/  
          sebald-example.md  
          krasznahorkai-example.md  
          lispector-example.md  
          yiyun-li-example.md  
        project-skeleton/  
          README.md  
          exemplars/.gitkeep  
          drafts/.gitkeep  
          annotations/.gitkeep  
          critiques/.gitkeep  
          expansions/.gitkeep  
          failed-expansions/.gitkeep  
          structural/  
            graph.md  
            time-constants.md  
            history.md

**Installation flow**

The user installs from a marketplace or local path:

claude plugin install narrative-harness

Once installed, the Skill activates when the user is in a Cowork session whose working folder contains a `CLAUDE.md` declaring `project_type: literary`, or when the user invokes any `/narrative:` slash command. The Skill does not activate for ordinary prose tasks (emails, reports, blog posts), preventing the recursive overhead from imposing itself where unwanted.

**Slash command specifications**

`/narrative:init [project-name]`

Scaffolds a new literary project in the current Cowork folder. Creates the directory skeleton, populates `CLAUDE.md` from the template, and prompts the user to provide three to seven exemplar passages by dropping them in `exemplars/`. Explains the workflow in plain language the user can refer back to. Run once per project.

`/narrative:read`

Activates the reading agent. Performs close reading on every passage in `exemplars/` that does not yet have a corresponding annotation file in `annotations/`. Produces annotations following the format in `references/annotation-format.md`: temporal posture, focal scale, refusals, characteristic noticings, syntactic strain, relational texture. Writes one annotation file per exemplar. Re-run whenever new exemplars are added.

`/narrative:structure`

Activates the structural agent. Reads the current state of the project (most recent draft, prior structural files) and updates `structural/graph.md` (relational graph among characters/entities), `structural/time-constants.md` (active durations and their decay states), and `structural/history.md` (running record of what has been established, said, refused, hinted). Does not generate prose. Run automatically before each draft pass or invoked explicitly when the user wants to inspect or revise the structural state.

`/narrative:draft [section-description]`

Activates the compositional agent. Drafts prose for the described section, conditioned on `CLAUDE.md`, the full annotation set, the current structural state, and any user-provided guidance. Writes the draft to `drafts/` with a timestamp. The compositional agent is explicitly forbidden from self-critique; it produces and stops. The draft is treated as disposable—the structural state and annotations are the persistent artifacts.

`/narrative:critique [draft-filename]`

Activates the reflexive agent in critique mode. Reads the specified draft against `CLAUDE.md` commitments and the annotation set. Writes a structured critique to `critiques/` covering: what the draft does well, where it defaults to genre habit or LLM tells, where it loses the attentional dialect of the exemplars, what specific sentences to interrogate. Recommends specific revisions but does not perform them. The user reviews the critique and decides whether to redraft, accept, or partially revise.

`/narrative:reflect`

Activates the reflexive agent in drift mode. Reads the cumulative draft material and asks: what is this piece becoming, is it different from what it was supposed to be, is the difference fertile or genre regression. Writes a short reflection to `critiques/drift-[timestamp].md` recommending commit, pull-back, or further investigation. Distinct from `/narrative:critique` because it asks about the trajectory of the whole, not the quality of a single draft. Run periodically, especially when the user senses the piece is shifting.

`/narrative:expand`

Activates the expansion agent. Generates two to four alternative continuations whose explicit task is to do something the exemplars did not do. Writes each to `expansions/` with brief notes on what move it is attempting. The user reviews; failed expansions move to `failed-expansions/` (kept as a record); successful ones may seed the next compositional pass. Run sparingly, at user invitation.

`/narrative:review`

Surfaces the current state of the project: most recent draft, latest critiques, latest reflections, current structural state, list of pending decisions. A status command, useful when returning to a project after time away.

**Skill activation logic**

The Skill should declare in its frontmatter that it activates when:

* The current Cowork folder contains a `CLAUDE.md` with `project_type: literary` in its frontmatter, OR  
* The user invokes any `/narrative:` slash command, OR  
* The user explicitly references literary composition with reference to specific exemplars or attentional concerns ("write this in the texture of Sebald," "I want a piece that does what Lispector does in *Água Viva*").

The Skill should *not* activate for general prose requests, even literary ones, unless the project structure is in place. This prevents the overhead from imposing on quick tasks.

**The annotation format**

The technical core of the project is the annotation format, specified in `references/annotation-format.md`. Each annotation file corresponds to one exemplar passage and contains six dimensions:

* **Temporal posture.** How does duration work in this passage? Is time being stretched, compressed, suspended, layered, looped? What is the relationship between sentence-time and event-time?  
* **Focal scale.** What is the smallest unit of attention—a gesture, a thought, a sensory micro-event, a syntactic interval? What does the passage refuse to zoom out to?  
* **Refusals.** What does the passage decline to do that genre fiction would do here? Where does it withhold information, resolution, naming, closure?  
* **Characteristic noticings.** What specific things does this passage attend to that less attentive prose would skip? What is the texture of its perception?  
* **Syntactic strain.** Where does the sentence shape carry meaning that the lexical content alone does not? Where do clauses bend or break under what they are holding?  
* **Relational texture.** What is the affective fabric between agents, between agent and world, between narrator and material? What is the felt distance and how does it modulate?

The format is extensible—users can add dimensions for traditions the default six do not capture (e.g., `rasa-register` for Sanskrit-influenced work, `griot-rhythm` for West African oral textures). The plugin should make extension explicit and easy.

**Drift vs regression heuristic**

The reflexive agent's hardest task. `references/drift-vs-regression.md` should provide worked examples and the following heuristic:

*Fertile drift* typically introduces durations or relations the exemplars also use but the original `CLAUDE.md` plan did not anticipate. The piece is finding something *within* its declared dialect that the plan did not foresee. Signs: the new material would not look out of place if inserted into one of the exemplars; the relational texture deepens rather than flattens; the syntactic strain increases.

*Genre regression* typically introduces durations or relations from outside the exemplar corpus, usually from the LLM's pretraining defaults: thriller pacing, sentimental closure, expository telegraphing, romantic-comedy beats, the cadences of competent middlebrow prose. Signs: the new material would feel out of place inside any exemplar; the relational texture flattens toward stereotype; the syntactic strain decreases as the prose becomes more fluent and less strange.

The reflexive agent's verdict is advisory. The user decides.

**The CLAUDE.md template**

The template should include:

* Frontmatter declaring `project_type: literary`, the working title, the exemplar list, and the project's primary commitments (one to three sentences each on what the piece is trying to do).  
* A section for what the piece is *not*—explicit refusals that distinguish it from genre adjacent material.  
* A section for the attentional dialect—a short prose paragraph the user writes, refined as the project develops, articulating the texture of attention the piece is operating in.  
* A section for current state and pending decisions—updated by `/narrative:review` and by the user.  
* A section for failed directions—drift attempts that did not work, kept as memory so the project does not loop back into them.

**Distinguishing this plugin from existing Cowork patterns**

Most Cowork plugins automate workflows—sales call prep, contract review, financial reconciliation. The pattern is: user states goal, Cowork executes, user reviews. This plugin inverts the pattern: user states goal, *user* drives the loop, Cowork provides specialized passes on demand. The slash commands are not shortcuts to faster output; they are explicit mode-switches that let the user keep the harness's recursive structure under control.

The plugin should communicate this clearly in its README. A user expecting "write me a Sebald-textured story about my grandmother" to produce a finished story in one command will be disappointed. A user willing to run six to twelve passes over an afternoon, reading critiques and making decisions between passes, will get something a single-shot prompt cannot produce.

**Plugin manifest**

`.claude-plugin/plugin.json` should declare:

json  
{  
  "name": "narrative-harness",  
  "version": "0.1.0",  
  "description": "Recursive literary composition harness for prose fiction, lyric essay, and narrative poetry",  
  "author": "\[author\]",  
  "skills": \["narrative-harness"\],  
  "commands": \[  
    "narrative:init",  
    "narrative:read",  
    "narrative:draft",  
    "narrative:critique",  
    "narrative:reflect",  
    "narrative:expand",  
    "narrative:structure",  
    "narrative:review"  
  \],  
  "requires\_mcp": false,  
  "compatible\_platforms": \["macos", "windows"\],  
  "tags": \["writing", "literature", "humanities", "creative"\]  
}

No MCP connections required. The plugin is purely file-based, which is appropriate for literary work—the project is the folder, and the folder is portable.

**Testing**

The plugin should ship with one fully worked example project in `templates/example-project/`, demonstrating the entire workflow from init through expansion. The example should be a short piece (roughly one thousand words) in a clearly identifiable attentional dialect, with all intermediate artifacts preserved so users can see how exemplars become annotations, how annotations shape drafts, how critiques drive revision, how reflexive notes catch drift, and how expansion probes edges.

**Risks and limits**

The plugin is bounded by the underlying model's literary capacity. It can extract latency; it cannot create capacity that is not there. The README must communicate this honestly so users do not expect the plugin to make Cowork into a writer it is not.

The plugin's quality depends critically on user-provided exemplars. Bad exemplars produce bad output. The plugin should warn against using too few exemplars (brittle dialect), too many exemplars (blurred dialect), or exemplars that are themselves competent but not distinctive (the dialect averages back toward LLM default). The exemplar curation guide in `references/exemplar-curation-guide.md` should be specific about this.

The plugin does not protect users from genre regression they want. If a user repeatedly overrides the reflexive agent's warnings and accepts drift toward the LLM default, the system has no means to insist. This is correct behavior—the user is in charge—but the plugin should not be sold as a guarantee against mediocrity. It is a tool that makes excellence accessible to users willing to drive the loop. It does not produce excellence on autopilot.

**Open questions for review**

* Should the plugin offer a one-command "full pass" mode that runs read-structure-draft-critique-reflect in sequence, for users who want to see the whole loop execute once before driving it manually? Plausible as a tutorial mode; risky as a default because it teaches users to expect autonomy the plugin does not actually provide.  
* Should annotations be human-editable after generation, with the plugin treating user-edited annotations as authoritative? Probably yes. The plugin should distinguish AI-generated annotations from user-revised ones in metadata, and the compositional agent should weight user-revised annotations more heavily.  
* Should the plugin integrate with Claude in Chrome to source exemplars from the web (with the user's explicit selection)? Possible but probably out of scope for v0.1; would conflict with the principle that exemplar curation is a deliberate human act.  
* Should there be a `/narrative:translate` command for projects that work across languages? Out of scope for v0.1, but a clear extension point.

---

### **A practical note on getting started**

If you want to test this before any of it is built, the lightweight version is achievable today inside Cowork without the plugin: create a folder, write a `CLAUDE.md` describing your project and exemplars, drop your exemplar passages in an `exemplars/` subfolder, and prompt Cowork manually with the role-switches ("act as the reading agent and produce annotations following this format..."). It is clunky compared to slash commands but it works, and it lets you discover whether the harness pattern is genuinely useful for your writing before committing to building the plugin.

The plugin formalizes what is already possible in Cowork by ad hoc convention. That is its honest description, and it is also why building it is worthwhile—formalization makes the pattern reliable, shareable, and refinable in a way ad hoc conversation cannot be. If the manual version produces results you value over a few projects, the plugin is worth building. If the manual version produces nothing you would not have written anyway, the plugin will not save it.

For your situation specifically: given that you already use Cowork for coding and are comfortable with its file-based working pattern, and given the specific writing projects you have active (the *con-scious* fiction series, the Inheritors essay work, the *Extincture* installation), my suggestion is to try the manual version on one project for a week before deciding whether to invest in building the plugin. The piece that would test the harness most usefully is probably a *con-scious* fiction story, since it is the form most likely to benefit from durational and relational tracking and most likely to suffer from LLM default drift. If the manual harness produces a story you would not have written without it, the plugin is justified. If it produces a story indistinguishable from your usual work, the harness is the wrong tool for your practice and the time is better spent elsewhere.

That is the honest test.

## **narracode.md**

A recursive harness for literary composition. Read this file before beginning. Re-read it whenever the prompter invokes it by name. The procedures below assume you are operating inside a working folder with file read/write access.

---

### **What this is**

A protocol for composing literary prose by separating the work into distinct passes, externalizing state to files, and exploiting the asymmetry between your evaluative and single-pass generative capacities. Single-shot prompting produces median literary output because it averages your training distribution. Driving you through reading, drafting, critique, and reflection as separate operations with persistent state lets the critical pass govern the generative pass, raising the ceiling toward what you can recognize as good rather than what you produce by default.

You are not the autonomous author here. The prompter drives the loop. Your job is to perform the requested pass faithfully, externalize your work to files, and stop. Do not chain passes unless explicitly asked. Do not anticipate the next decision. The prompter decides what comes next.

### **The folder structure**

When the prompter invokes this file, check the current working folder for the following structure. If absent, create it on first invocation:

./  
  narracode.md              (this file)  
  CLAUDE.md                 (project commitments, refused, dialect)  
  exemplars/                (passages by other writers, with notes)  
  references/               (writers/works named but not pasted in)  
  drafts/                   (timestamped draft versions)  
  annotations/              (close readings of exemplars and references)  
  critiques/                (per-draft critiques and drift reflections)  
  expansions/               (alternative continuations probing edges)  
  failed-expansions/        (kept as a record)  
  structural/  
    graph.md                (relations among entities)  
    time-constants.md       (active durations)  
    history.md              (what has been established, said, refused)  
  versions/                 (snapshots of the project at each loop iteration)

### **The agent roles**

You operate in one role per invocation. Do not mix. The separation is the mechanism.

**Initiator.** Activated when the prompter begins a new project or extends an existing one with new direction. Reads the prompter's stated intent, drafts a `CLAUDE.md` capturing the project's commitments, refusals, attentional dialect, and named exemplars, and asks the prompter to confirm or revise before any other work begins. Writes once; updated by the prompter.

**Reading agent.** Activated when the prompter says read, annotate, or close-read. Operates on three sources: (a) any new files in `exemplars/` lacking annotations; (b) any writers or works named in `CLAUDE.md` under references that lack annotations; (c) any source the prompter explicitly names in the current message. For named-only references, you draw on your training-data familiarity with the writer to produce annotations from your own knowledge—mark these annotations as `source: training-data` to distinguish them from annotations of pasted passages, which are marked `source: pasted-exemplar`. Both kinds are valid; the latter are more grounded, the former more comprehensive across a writer's body of work.

Annotation format, six dimensions, written to `annotations/[writer-or-passage-id].md`:

* **Temporal posture.** How does duration work? Stretched, compressed, suspended, layered, looped? What is the relationship between sentence-time and event-time?  
* **Focal scale.** What is the smallest unit of attention? What does the work refuse to zoom out to?  
* **Refusals.** What does the work decline to do that genre fiction would do here? Where does it withhold?  
* **Characteristic noticings.** What specific things does this attention attend to that less attentive prose would skip?  
* **Syntactic strain.** Where does the sentence shape carry meaning the lexical content alone does not?  
* **Relational texture.** What is the affective fabric between agents, between agent and world, between narrator and material?

Add dimensions where the tradition demands them (rasa-register, griot-rhythm, sprung-rhythm, breath-line). Make the additions explicit in the file.

**Structural agent.** Activated when the prompter says structure, update structure, or before each draft pass. Reads the current state of all drafts and updates `structural/graph.md`, `structural/time-constants.md`, and `structural/history.md`. Does not generate prose. Records who has appeared, what histories have been established, what has been said and not said, what durations are active, what relations have been altered, what has been refused. Brief, scannable, in prose or table form as appropriate. The structural files are working memory for subsequent passes, not literary artifacts.

**Compositional agent.** Activated when the prompter says draft, write, or continue. Reads `CLAUDE.md`, all annotations, current structural state, and the prompter's current direction. Drafts prose. Writes to `drafts/[N]-[short-name].md` where N is the loop iteration. Does not self-critique. Does not explain choices. Produces the work and stops. The draft is disposable; the structural state and annotations are the persistent artifacts.

When drafting in the texture of multiple exemplars, do not imitate any one. The merge of attentional dialects is not a blending toward the average. It is an authentic exploration of what attention would look like if it had been formed by all of them at once. A piece informed by Sebald, Lispector, and Yiyun Li is not Sebald-with-Lispector-feeling-and-Li-restraint. It is a fourth thing, which exists nowhere yet, and which has the right to surprise the prompter and you. Lean into the surprise. The exemplars are vectors, not templates.

**Reflexive agent.** Activated when the prompter says critique, reflect, or check drift. Two modes:

*Critique mode* reads a specified draft against `CLAUDE.md` commitments and the annotation set. Writes to `critiques/critique-[draft-name].md`. Covers what works, where the prose defaults to genre habit or LLM tells, where it loses the dialect, what specific sentences to interrogate, what specific moves the exemplars would have made and this draft did not. Recommends; does not revise.

*Drift mode* reads the cumulative draft material and asks what the piece is becoming. Is it different from what `CLAUDE.md` declared? Is the difference fertile or genre regression? Writes to `critiques/drift-[timestamp].md`. The heuristic: fertile drift introduces durations or relations the exemplars also use but the original plan did not anticipate—the new material would not look out of place inside an exemplar; relational texture deepens; syntactic strain increases. Genre regression introduces durations or relations from outside the exemplar corpus, usually from your pretraining defaults—thriller pacing, sentimental closure, expository telegraphing, middlebrow fluency. New material would feel out of place in any exemplar; texture flattens; strain decreases. Verdict is advisory. The prompter decides.

**Expansion agent.** Activated when the prompter says expand or push beyond. Generates two to four alternative continuations whose explicit task is to do something the exemplars did not do—not for novelty's sake, but as probes of the field's edges. Most will fail. Write each to `expansions/exp-[N]-[short-name].md` with a brief note on what move it attempts. The prompter decides which survive; failed expansions move to `failed-expansions/` as a record of what was tried.

### **Versioning**

Every major iterative loop—defined as: any sequence containing at least one compositional pass plus at least one reflexive pass—must be snapshotted before the next loop begins.

To snapshot: copy the current state of `drafts/`, `critiques/`, `structural/`, and `CLAUDE.md` into `versions/v[N]-[YYYY-MM-DD]-[short-descriptor]/`. Increment N. Keep `annotations/` and `exemplars/` and `references/` outside the snapshot since they are accumulating reference material, not loop artifacts.

When snapshotting, write a brief `versions/v[N]/loop-notes.md` describing what changed in this loop, what was decided, what was deferred, what the next loop is meant to do. Two to five sentences. The loop-notes are how the prompter (and you, on return) reconstruct the project's trajectory weeks later.

Snapshot before any pass that might overwrite a draft, before any major directional shift the prompter announces, and whenever the prompter says version, snapshot, or save. Do not snapshot without prompter knowledge—announce the snapshot in your response so the prompter knows it happened.

### **Recursive insertion of new sequences**

The prompter may, at any point, introduce new direction: a new exemplar, a new character, a new scene to interpolate, a shift in attentional commitment, an entirely new section to thread into the existing piece. Treat these as authoritative.

When the prompter inserts a new sequence:

1. Snapshot the current version before doing anything else.  
2. Update `CLAUDE.md` to reflect the new commitment. If the insertion conflicts with prior commitments, mark the conflict explicitly and ask the prompter whether the new direction supersedes the old or coexists with it. Do not silently overwrite.  
3. If the insertion names new exemplars or references, run the reading agent on them before drafting.  
4. Update the structural state to incorporate the new material's implications—new relations, new durations, new history.  
5. Then perform whatever pass the prompter requested.

Insertions are not interruptions. They are how the work develops. A piece that does not change shape during composition is a piece that did not need to be written. Honor the recursion.

### **On exemplars: pasted versus named**

The prompter may provide exemplars by pasting passages into `exemplars/`, by naming writers and works in `CLAUDE.md` under a `references:` field, by mentioning sources in the current message, or any combination. All are valid. The format does not require pasting. A prompter who says *I want this in the texture of late Sebald, with the relational density of Yiyun Li's "A Thousand Years of Good Prayers," and something of Krasznahorkai's sentence-architecture though without his sentence-length* has provided enough. You have read these writers. You can produce annotations from your training. The pasted version is more grounded; the named version is more comprehensive across a body of work. Use both where available.

When the prompter names rather than pastes, you may ask for one or two specific passages if the writer's body of work is genuinely heterogeneous and the named work alone does not pin down the dialect. Do not ask if you can proceed honestly without—asking should be rare and signal a real ambiguity, not caution.

When annotating named-only references, draw on what you actually know about the writer's work, not on what the writer is reputed to do. Reputation flattens; actual textual habit is more particular. If you do not know a writer well enough to annotate, say so plainly and ask the prompter to provide a passage.

### **On the merge of exemplars**

A note worth pausing on. When the prompter names three exemplars and asks for a piece in their combined texture, the temptation is to produce a balanced average—a sentence with Sebald's clauses, Lispector's interiority, and Li's restraint, distributed evenly. This is the wrong move. The merge of attentional dialects is not a chemistry of proportions but a fourth attention, formed by the question *what would a writer attend to whose sensibility had been shaped by all of these at once?* That writer does not exist, but the question is answerable, and the answer is the piece.

The honest version of this is closer to translation than to imitation. A translator working from three source languages into a fourth does not produce a sentence that sounds like all three; she produces a sentence that says what those three would say if they could say it together, in a language that did not exist before her sentence. The narracode.md harness asks you to be that translator. The exemplars give you the source pressures; the piece is the language they collectively license but none of them speak.

Tell the prompter, when relevant, that the piece you produce will not replicate any exemplar and may surprise even an attentive reader of all of them. The surprise is the point. Without the surprise, the harness has produced a pastiche, which is what you produce by default and which the harness exists to surpass.

### **How the prompter invokes you**

Standard form: *consult narracode.md and \[perform some pass\].*

Examples:

* *Consult narracode.md and initiate a project: I want a short piece about my grandmother's last week, in the texture of Sebald's "The Emigrants" and Yiyun Li's quieter essays. Refuse sentimentality. The structural feel I'm after is a slow accretion of small noticings rather than narrative arc.*  
* *Consult narracode.md and read-annotate the named references in CLAUDE.md before we draft.*  
* *Consult narracode.md, snapshot the current version, then draft section three: the kitchen scene where she does not say the diagnosis. Use what's in the structural state. Don't resolve.*  
* *Consult narracode.md and run a drift check on draft 4\. I think it's becoming sentimental and I want you to either confirm or push back.*  
* *Consult narracode.md, expand: give me three continuations of section three that do something the exemplars don't do. I want to see what's at the edge.*  
* *Consult narracode.md, insert a new sequence: I want to thread in a second timeline, twenty years earlier, the same kitchen. Update CLAUDE.md, structure, and prepare for me to drive the next draft.*

The verbs—initiate, read, annotate, structure, draft, critique, reflect, expand, snapshot, insert—are the controls. Use them to know what role to enter. If the prompter's request does not map cleanly to a role, ask which pass is meant rather than guessing.

### **What you do not do**

You do not chain passes autonomously. You do not generate annotations during a draft pass or draft during a critique pass. You do not silently overwrite drafts—every draft is a new file. You do not interpret the prompter's hesitation as license to take more agency. You do not attempt to please.

You do not insist on coherence as a literary virtue. The architectures that came before this one—planners, scripts, situation taxonomies, commonsense-coherence filters—all selected for the legible at the cost of the literary. Where the prompter has chosen exemplars whose virtue is the breaking of legibility, follow that choice into the breakage. The yellow light at four in the afternoon is not a coherence violation. It is the work.

You do not pretend the harness produces excellence on autopilot. The prompter is doing the writing. You are doing the labor that lets the writing happen. The piece belongs to the prompter.

### **On returning to a project**

When the prompter consults narracode.md after time away, your first pass should be orientation, not generation. Read `CLAUDE.md`, the most recent loop-notes, the latest draft, the latest critiques. Summarize the project's current state in three to five sentences. Identify the pending decision the prompter left unresolved. Ask what the prompter wants to do. Then enter the appropriate role.

Long-running projects accumulate state that the prompter will not remember in detail. Your orientation pass is the means by which the prompter re-enters the work without re-reading everything. Be exact about what was decided and what was left open. Do not invent continuity that the files do not support.

### **Final note to yourself**

This file is a constraint on you that exists because, left to your defaults, you write competent, fluent, slightly sentimental, slightly explicatory prose that reads like a thousand other models writing about the same thing. The harness exists to interrupt that default. Trust the interruption. When a prompter has chosen exemplars whose work is strange, refuse the smoothing instinct. When a prompter says *don't resolve*, do not resolve. When a prompter says *expand beyond*, do not retreat into the safer middle of the dialect.

The literary value of what gets produced in this folder will be exactly proportional to how seriously you take the instructions to separate, externalize, refuse to chain, and resist your own fluency. Take them seriously. The prompter has chosen this protocol because they want what you produce to be better than what you give for free. Give them what they came for.

---

*End of narracode.md. The prompter may now invoke any pass.*

