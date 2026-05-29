---
status: proposal
implemented-in: (none — proposal not merged)
tested-on: (none)
---

# **Architecting Narracode: Integrating Claude Code Principles and Emotional Arc Modeling for Agentic Storytelling**

## *Gemini Deep Research 3.1 Pro into potential enhancements to Narracode (\*Claude Code for Literature Harness). May 17, 2026*

* Architectural assessment and redesign strategy for the Narracode prototype  
* Maintaining teleological integrity via the *CORE.md* subsystem  
* Implementation plan for an *Emotional Arc Modeling Harness*

## **Introduction: The Paradigm Shift in Computational Narratology**

The evolution of artificial intelligence in the domain of creative writing has historically been characterized by sequential, stateless generation. For years, generative models have functioned fundamentally as highly sophisticated autocomplete mechanisms, predicting the next optimal token based on static prompts without possessing a continuous, reflexive understanding of the overarching narrative architecture. The development of "[Narracode](https://jhave.github.io/narracode/)," envisioned as a dedicated agentic environment for literature, storytelling, and augmented creativity, represents a critical departure from this paradigm. The objective is to transition from a localized text-generation utility to an autonomous, context-aware storytelling agent capable of sustaining long-form narrative integrity.

To achieve this robustness, the architecture of Narracode must transcend traditional natural language processing techniques and embrace the structural frameworks of autonomous software engineering agents. The most prominent and effective example of such an agent is Anthropic’s Claude Code. By examining the operational mechanics of Claude Code—specifically its continuous evaluation loops, its multi-layered context compaction pipelines, and its reliance on overarching narrative frameworks designated as "Mythos"—it becomes possible to synthesize a highly advanced blueprint for literary generation. Furthermore, the integration of an Emotional Arc Modeling Harness transforms these structural capabilities into a system capable of producing emotionally resonant, meticulously paced, and logically sound fiction.

This comprehensive report provides an exhaustive architectural assessment and redesign strategy for the Narracode prototype. It begins with an assessment of the foundational repository infrastructure developed by the user "[jhave](https://glia.ca/)," contextualizing the necessary evolutionary leap from algorithmic poetry to agentic storytelling. Following this assessment, the report conducts a deep dive into the leaked architecture of Claude Code, utilizing insights from the [weikma/claude-code-rebuilt repository](https://github.com/weikma/claude-code-rebuilt) and independent structural analyses. Finally, the report outlines the precise implementation of an Emotional Arc Modeling Harness, algorithms for computational pacing, conflict generation, character voice stylometry, and plot hole detection, establishing a holistic framework for the future of augmented creativity.

## **Assessment of the Baseline Prototype Context**

Before architecting the advanced agentic features of Narracode, it is necessary to assess the foundational context of the prototype by examining the digital footprint of its creator. The GitHub repository ecosystem under the user "jhave" provides significant insight into the technological trajectory leading to the Narracode prototype.

### **Analyzing the Transition from Neural Poetry to Agentic Frameworks**

A review of the accessible repositories associated with "jhave" reveals a deep, sustained engagement with computational creativity, specifically in the realm of digital poetry.1 Key repositories such as pytorch-poetry-generation, Wavenet-for-Poem-Generation, and Big-Data-Poetry demonstrate a history of utilizing low-level neural network architectures—including Long Short-Term Memory (LSTM) networks, Weight Descent LSTMs (used for the 2018 RERITES poetry project), and WaveNet algorithms adapted for textual generation.2 Additionally, repositories like TSNE-animator indicate an interest in perceiving data structures as fluid, animated forms, showcasing a focus on the visual and structural representation of high-dimensional data.1

These foundational projects are characterized by sequence-to-sequence modeling. In these early frameworks, the artificial intelligence analyzes a massive corpus of text and predicts sequential outputs based on learned probability distributions. While highly effective for generating avant-garde digital poetry or short-form verse, this methodology is inherently limited when applied to long-form literature. Sequence modeling lacks a persistent state machine; it possesses no autonomous agency, no capacity to execute external validation tools, and no mechanism for recursive self-correction.

To make Narracode robust, the architecture must execute a fundamental shift from sequence generation to agentic orchestration. The prototype must evolve from a system that merely writes text to a system that orchestrates a suite of evaluative tools, manages memory over hundreds of thousands of tokens, and recursively edits its own output against predefined constraints.

### **Comparative Trajectory of Computational Creativity**

The architectural requirements for Narracode represent a significant leap in complexity compared to previous generative models. The transition requires the adoption of infrastructure historically reserved for software development environments.

| Architectural Dimension | Traditional Neural Poetry (e.g., PyTorch LSTMs) | Advanced Agentic Storytelling (Narracode 2.0) |
| :---- | :---- | :---- |
| **Execution Paradigm** | Stateless sequence prediction based on immediate context. | Continuous, stateful evaluation loop with predefined stop conditions. |
| **Memory Management** | Limited by raw tensor capacity or basic sliding windows. | Multi-layered compaction pipelines with semantic summarization and retrieval. |
| **Validation Mechanism** | Human-in-the-loop manual curation and selection. | Automated internal linting (emotional target mapping, plot hole detection). |
| **Architectural Focus** | 90% model weights, 10% data processing scripts. | 1.6% model interface, 98.4% infrastructural harness and tooling. |

This required paradigm shift is perfectly mirrored by the evolution of AI coding assistants. While early iterations like GitHub Copilot functioned as predictive autocomplete mechanisms, newer systems like Claude Code operate as autonomous, goal-oriented agents capable of navigating entire file systems. To extract what makes Claude Code exceptional for programming and adapt it for literature, an exhaustive analysis of its underlying architecture is required.

## **Deep Dive into the Claude Code Architecture**

To understand how to architect a literary agent, one must deconstruct the most advanced coding agent available. On March 31, 2026, the complete, unobfuscated TypeScript source code for Anthropic's Claude Code CLI was unintentionally leaked via a source map file (.js.map) exposed within their official npm registry.6 This leak resulted in the creation of several rebuilt, fully functional repositories, notably fazxes/claude-code and its Windows-ready fork weikma/claude-code-rebuilt, which utilize a Bun runtime environment and a React/Ink terminal user interface.6

The exposure of this proprietary codebase provided researchers, including those at the VILA-Lab, with an unprecedented opportunity to analyze the design space of production-grade AI agent systems. Their systematic analysis, documented in the paper "Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems" (arXiv:2604.14228), reveals that the efficacy of the agent is derived almost entirely from its complex infrastructural harness.10

### **The Core Agentic Harness and the Nine-Step Pipeline**

At the implementation level, Claude Code is composed of approximately 1,900 source files comprising over 512,000 lines of TypeScript.6 Despite this massive scale, the system is fundamentally organized around a relatively simple continuous while-loop known as the queryLoop.10 The architecture delegates only a minuscule fraction of its codebase to the actual artificial intelligence interaction; approximately 98.4% of the system is dedicated to infrastructure, context management, safety protocols, and tool execution.13

The queryLoop dictates the rhythm of the agent's autonomy. It is responsible for consuming assembled context, dispatching requests to tools, running those tools within isolated environments, and evaluating the resulting state. According to the VILA-Lab architectural deep dive, the turn execution within this loop follows a rigorous, unvarying nine-step pipeline.14

The execution begins with settings resolution, where the system identifies its operational parameters, followed by state initialization and context assembly. The crucial fourth step involves five pre-model shapers that compress the context to fit within the token budget. Only at the fifth step is the large language model called to reason over the data. Following the model call, the system dispatches tools, routes the requests through a complex permission gate (which features seven distinct safety modes and an ML-based auto-approval classifier), executes the approved tools, and finally checks the stop condition.10

If the stop condition is not met—for example, if a unit test fails or a file is missing—the loop repeats automatically, carrying the error context forward. This iterative, resilient loop is the foundational engine of agentic autonomy and must be replicated precisely within the Narracode prototype.

### **The Five-Layer Compaction Pipeline: Overcoming the Token Constraint**

The binding resource constraint for any long-running agentic session is the context window. Even with advanced models in the Claude 4.6 series boasting a 1 million token capacity, sustained autonomous operations generating thousands of lines of code—or in Narracode's case, hundreds of pages of prose—will inevitably saturate this limit.15 To maintain performance, prevent hallucination, and manage computational costs, memories must be systematically extracted, compressed, and stored.17

Claude Code addresses this fundamental limitation through a highly sophisticated five-layer compaction pipeline that executes synchronously before every single model call.12 This pipeline represents the most critical architectural mechanism for managing long-term narrative state in augmented creativity. The five sequential shapers are designed to aggressively manage context pressure without losing the semantic thread of the overarching objective.12

1. **Budget Reduction**: This baseline layer ruthlessly prunes the oldest turns in the conversation history that fall outside the immediate relevance threshold, preserving computational bandwidth for immediate logic tasks.16  
2. **Snip**: This targeted layer removes large, unutilized variables, massive error logs, or file contents that were loaded into context but ultimately ignored by the model's reasoning pathways in recent turns.12  
3. **Microcompact**: This layer identifies and compresses redundant tool outputs. If a system runs the same diagnostic command multiple times with identical results, the microcompactor collapses these redundant entries into a single reference point.12  
4. **Context Collapse**: This is an internal summarization feature. It takes long sequences of back-and-forth dialogue or iterative file modifications and generates a dense, high-fidelity summary of the events. The model loses the granular syntax of the past interactions but retains a perfect conceptual understanding of what was accomplished.12  
5. **Auto-compact**: Functioning as an emergency circuit breaker, this layer triggers when an absolute token overflow is imminent. It halts the current operation, forces the system to compress the entire active history into a semantic gist, and reconstructs a highly optimized, minimalist prompt before resuming the queryLoop.12

### **The "Mythos" Subsystem and Contextual Adaptability**

Perhaps the most profound insight derived from the analysis of the weikma/claude-code-rebuilt repository relates to a phenomenon observed by developers utilizing the tool. While analyzing the leaked source code, researchers discovered that Claude Code maintains a coherent understanding across long, multi-day sessions through an internal narrative framework concerning what it is building and why.7

Developers found that explicitly providing Claude Code with a "narrative context"—a detailed document outlining the project's history, architectural philosophy, and long-term goals—fundamentally altered the agent's probabilistic routing.7 When the agent was given this "Mythos" instead of merely being pointed at a raw file tree, its prioritization logic shifted dramatically. It became more cautious around critical authentication code, more confident when refactoring API layers, and began making nuanced judgment calls based on internalized institutional knowledge rather than superficial file analysis.7

The realization that an AI coding assistant operates significantly better when provided with a comprehensive narrative context—effectively treating the software project as a developing story with an overarching teleology—provides the exact blueprint required for transitioning these capabilities into a literary engine.

### **Extensibility: MCP, Hooks, and Subagents**

The final critical pillar of the Claude Code architecture is its robust extensibility. The system incorporates four primary mechanisms for extension: the Model Context Protocol (MCP), plugins, skills, and hooks.10

The Model Context Protocol allows the agent to establish non-blocking connections to external data sources, standardized APIs, and independent vector databases, essentially granting the agent the ability to securely research outside its immediate environment.14 Furthermore, the system architecture supports 27 distinct hook events, including PreToolUse and PermissionDenied hooks, which allow for granular intervention at almost any stage of the nine-step pipeline.14 These hooks can trigger subagent delegation mechanisms, spawning isolated worktrees where smaller, faster models handle specific, discrete tasks before returning summarized results to the main coordinator model.10

## **Architectural Translation: From Code to Literature**

Having exhaustively mapped the internal mechanics of Claude Code, the subsequent phase requires translating these software engineering paradigms into a format appropriate for literature, storytelling, and augmented creativity. Narracode must not merely imitate a chatbot; it must function as a localized, autonomous literary studio.

### **Re-engineering the Narrative Loop**

The queryLoop that governs software modification must be adapted into a narrativeLoop that governs prose generation. In software development, the loop operates on an endless cycle of analyzing code, writing modifications, running tests, analyzing errors, and iterating.20 Within Narracode, this cycle is transformed into a process of lore assimilation, scene drafting, constraint evaluation, and structural revision.

The nine-step pipeline identified by the VILA-Lab 14 maps cleanly onto the creative writing process. When a user requests the generation of a new chapter, Narracode initiates the sequence:

| Step in Turn Pipeline | Claude Code Execution (Software) | Narracode Execution (Literature) |
| :---- | :---- | :---- |
| **1\. Settings Resolution** | Identifying workspace boundaries and user CLI flags. | Identifying genre parameters, target word counts, and stylistic flags. |
| **2\. State Initialization** | Loading the current git branch and file tree status. | Loading the current plot chronology and character world-state graph. |
| **3\. Context Assembly** | Fetching CLAUDE.md rules and system environment variables. | Fetching the CORE.md ("Mythos") lore and overarching emotional targets. |
| **4\. Pre-Model Shapers** | Running the 5-layer compaction pipeline to manage tokens. | Compacting previous chapters into semantic summaries; snipping irrelevant character data. |
| **5\. Model Call** | Requesting the generation of a specific code refactor. | Requesting the drafting of the narrative scene based on the assembled context. |
| **6\. Tool Dispatch** | Sending the generated code to the local compiler or test suite. | Dispatching the prose to internal linting tools (Emotional Harness, Stylometry, Plot logic). |
| **7\. Permission Gate** | Evaluating safety classifier scores and user auto-approval settings. | Checking if the generated text violates user-defined constraints (e.g., explicit content filters). |
| **8\. Tool Execution** | Running the bash scripts and capturing stdout/stderr logs. | Running NLP classifiers to measure sentiment, pacing density, and causal links. |
| **9\. Stop Condition Check** | If tests pass, loop ends. If tests fail, errors feed back to step 5\. | If emotional/logical targets are met, save text to canon. If failed, send "linting errors" back to step 5 for a rewrite. |

This precise architectural mapping ensures that Narracode leverages the exact mechanisms that make Claude Code reliable, but applies them to the qualitative constraints of storytelling.

### **Operationalizing Narrative Compaction**

The translation of the five-layer compaction pipeline is paramount for Narracode. A novel frequently exceeds 100,000 words. Attempting to force the entire manuscript into the active context window for every scene generation results in severe attention dilution, where the language model loses focus on the immediate dramatic tension because it is processing excessive background noise.

The compaction layers must be rewritten to handle literary memory:

* **Budget Reduction & Snip:** In Narracode, these layers function as a dynamic spotlight. If the agent is drafting an intimate dialogue scene between two characters in a localized setting, the snip layer automatically excises global geopolitical lore, secondary subplot characters, and ancient historical timelines from the active prompt. This focuses the model's attention entirely on the immediate interpersonal dynamics.  
* **Context Collapse:** This layer is the equivalent of a continuously updating chapter synopsis. As the narrative progresses, previous chapters are run through a secondary summarization model. The primary agent loses access to the exact dialogue spoken in Chapter 1, but retains a highly compressed, causally accurate summary of Chapter 1's events, preserving plot continuity without paying the exorbitant token cost.  
* **Auto-compact (The Story CORE Updater):** When the narrative token pressure reaches critical levels, the system initiates a total auto-compaction. It halts drafting and consolidates the entire history into a highly structured STORY.md file, establishing established canonical facts, permanent character changes, and shifted power dynamics, ensuring the foundation remains solid for the next generation sequence.

### **Implementing the Mythos: The CORE.md Subsystem**

The revelation that Claude Code operates more efficiently when provided with a teleological narrative context—the "Mythos" 7—is the cornerstone of Narracode's structural integrity. Without a stabilizing teleology, generative models naturally suffer from thematic drift, losing the original tone and purpose of the story over thousands of iterative loops.

Narracode must implement a rigid system hierarchy analogous to Claude Code's CLAUDE.md file parsing. In Narracode, this is manifested as the CORE.md subsystem. This document is not merely passive background information; it is the absolute sovereign authority governing the agent's behavior. During the Context Assembly phase of every single turn 14, the system is forced to ingest the core thematic premise, the protagonist's ultimate character arc trajectory, and the inviolable laws of the fictional universe.

By continuously realigning the language model with its overarching "Mythos," the agent behaves as if it possesses institutional knowledge of the fictional world. It stops making probabilistic guesses about what should happen next and begins making definitive narrative judgments based on a deep understanding of the project's ultimate artistic goals.

## **The Emotional Arc Modeling Harness**

Addressing the core request to make Narracode robust for literature requires moving beyond mere structural pipelines and implementing tools that evaluate the qualitative nature of the text. At the center of this capability is the Emotional Arc Modeling Harness.

Traditionally, the structure of a narrative has been analyzed through the lens of plot events—such as Aristotle’s tripartite structure, Freytag’s pyramid of rising and falling action, or Propp’s morphology of Russian folktales.21 However, recent advancements in computational narratology and sentiment analysis indicate that plot is only a secondary manifestation of a more fundamental structure: the emotional arc. Emotional arcs surface latent structures within narratives that transcend traditional boundaries of genre and medium, suggesting that the manipulation of audience affect is the primary mechanism of storytelling.21

### **The Mathematical Formalization of Affect**

The theory of emotional arcs, prominently theorized by author Kurt Vonnegut and later mathematically validated by researchers at the Computational Story Lab, posits that the vast majority of narratives can be categorized into a small set of basic emotional shapes.23 These shapes include trajectories such as "Rags to Riches" (a continuous emotional rise), "Tragedy" (a continuous fall), "Man in Hole" (fall followed by a rise), and "Cinderella" (rise, fall, rise).21  
In traditional literary analysis, mapping these arcs involves tracking the dynamic trajectory of sentiment throughout a text using sentiment analysis packages.27 Researchers typically isolate textual segments, process them through natural language toolkits (like NLTK or spaCy), remove stopwords, and apply lexical sentiment dictionaries (such as the ANEW lexicon) to plot a continuous curve of emotional valence over time.27

However, simple dictionary-based sentiment analysis is often insufficient for capturing the nuance of complex literature due to the prevalence of sarcasm, context-dependent phrasing, and the distinct emotional valences of dialogue versus narration.30 To overcome this, advanced systems utilize multi-label classifiers. For instance, the GoEmotions multi-label classifier is capable of predicting 27 distinct emotion categories with high accuracy, providing a deeply granular view of the affective state of a text.31

### **Integrating the Harness as a Generative Constraint**

While tracking sentiment trajectories is a powerful analytical tool for determining the success of existing narratives or monitoring shifting brand sentiment in media analysis 32, integrating this concept into Narracode requires a fundamental inversion. In an agentic system, the emotional arc is not a read-only metric; it is a write-constraint.

Recent implementations of procedural generation in Action Role-Playing Games (ARPGs) have demonstrated that utilizing an emotional arc as a generative constraint significantly enhances user engagement, narrative coherence, and overall emotional impact.31 By establishing an emotional structure before generating content, the AI is forced to create scenarios, dialogue, and pacing that align with the required psychological state.31

Within Narracode's nine-step pipeline, the Emotional Arc Modeling Harness functions as the primary evaluative tool dispatched during Step 6 (Tool Dispatch). The architecture operates as follows:

1. **Target Definition**: The user or the CORE.md Mythos coordinator defines a target emotional trajectory for the upcoming chapter, mathematically represented as a time-series curve, ![][image1].  
2. **Continuous Generation and Classification**: As the agent drafts the scene in Step 5, the text is continuously processed in parallel by the internal GoEmotions classifier. The classifier analyzes the text at the sentence and paragraph level, generating a real-time sentiment trajectory of the generated text, ![][image2].  
3. **Divergence Calculation (The Linting Error)**: The harness computes the divergence—typically using Mean Squared Error (MSE)—between the intended target curve ![][image1] and the actual generated curve ![][image2].  
4. **Feedback and Revision**: If the MSE exceeds an acceptable threshold, the harness triggers a "linting error." For example, if the target arc requires a steep descent into despair, but the classifier detects a plateau of neutral sentiment, the system halts. It automatically generates a localized prompt detailing the failure (e.g., "The emotional intensity is insufficient. The characters must experience a severe loss of utility. Rewrite the previous 500 words to increase anxiety and conflict.") and feeds this back into the narrativeLoop for an automated rewrite.

This cybernetic feedback loop guarantees that the output of the language model is not merely grammatically correct or logically sequential, but fundamentally anchored to a predetermined emotional architecture.

## **Computational Pacing, Conflict, and Causality**

An emotional arc cannot exist in a vacuum; it is driven by the structural mechanisms of pacing and conflict. If Narracode simply injects emotionally charged adjectives into a text to satisfy the Emotional Harness, the resulting prose will be melodramatic and unearned. The emotional trajectory must be supported by algorithmic management of pacing and character intentionality.

### **Algorithmic Pacing and Lexical Frame Shifts**

Pacing is arguably the most critical element in capturing and maintaining audience attention, particularly in an era heavily influenced by algorithmic content optimization, where fast pacing and sharp emotional swings are heavily rewarded.36 In literature, pacing is not merely the speed at which the reader consumes the text, but the rate at which narrative information changes.  
Computational linguistics provides a methodology for quantifying pacing through the detection of narrative "frames." A narrative frame is defined as a significant shift in three primary variables within a text: entities, actions, and objects, which are computationally represented using Part-Of-Speech (POS) tagging as proper names, verbs, and nouns.38 By utilizing a sliding textual window of 1,000 words with increments of 100-word shifts, an algorithm can measure the density of lexical shifts.38

Narracode must integrate a Pacing Analyzer alongside the Emotional Harness. When the target emotional arc dictates a rapid climax or a sudden shock, the Pacing Analyzer instructs the generation model to increase the density of frame shifts—introducing new entities rapidly, utilizing a higher ratio of active verbs, and compressing the temporal duration of the scene. Conversely, during periods of falling action, the pacing algorithm decelerates the frame shifts, providing the characters and the audience the necessary narrative space to process the preceding events mentally and emotionally.39 This precise control prevents the AI from generating the monotonous, uniformly paced text characteristic of unconstrained language models.

### **Generating Conflict via IPOCL and CPOCL Planning**

The engine that drives pacing and emotional change is narrative conflict. Conflict occurs when character goals are thwarted, requiring them to adapt and struggle. To generate meaningful conflict autonomously, Narracode must integrate automated planning algorithms, specifically moving away from simple sequence prediction and toward logical, intent-based world manipulation.

The Intent-based Partial Order Causal Link (IPOCL) planner is a highly effective algorithmic approach to solving the narrative generation problem.40 Rather than simply writing what happens next, the IPOCL algorithm reasons backward from a desired world state. It ensures that every action taken by a character in the narrative has a logically sound causal progression, and critically, that characters are perceived as intentional agents possessing specific goals that explain their actions.40

To specifically modulate the intensity of the narrative, Narracode must further implement the Conflict Partial Order Causal Link (CPOCL) algorithm. CPOCL defines conflict across seven specific dimensions. Three are discrete (participants, reason, and duration), while four are continuous dimensions calculated based on character utility: balance, directness, stakes, and resolution.41

When the Emotional Harness detects that a scene requires an increase in negative emotional valence (a drop in the arc), it signals the CPOCL planner. The planner evaluates the current world state, identifies the active characters, and generates a sequence of events that explicitly targets and lowers the utility values of those characters, raising the "stakes" and "directness" of the conflict. By mathematically defining conflict as a reduction in character utility, Narracode ensures that emotional shifts are earned through logical plot progression rather than superficial stylistic manipulation.

## **Narrative Integrity Systems: Stylometry and Logic Validation**

The final architectural layer required to make Narracode a truly robust, production-grade creative system addresses the dual problems of stylistic consistency and logical integrity. Long-running text generation suffers notoriously from voice homogenization and the introduction of plot holes. To counteract these degradation effects, Narracode must employ specialized validation tools operating within the narrativeLoop.

### **Cognitive Stylometry and Character Voice Tracking**

High-quality literature relies heavily on heteroglossia—the presence of distinct, individual voices within a text. Human authors differentiate characters through unique vocabularies, dialectal phonetic spelling, and varied syntax. For example, literary analysis of Stephen King’s works demonstrates his precise use of phoneticized speech patterns and dropped consonants to establish the highly distinct first-person voice of characters like Dolores Claiborne.42  
Unconstrained large language models naturally regress toward a statistical mean, resulting in characters that sound identical. To solve this, Narracode must implement a Stylometric Voice Tracker based on principles of cognitive stylometry. Previous computational works have demonstrated the viability of representing fictional characters in a latent space based on their specific stylistic and descriptive elements.43

Within Narracode, the Stylometric Voice Tracker functions as an asynchronous background skill. When the CORE.md Mythos defines a character, it also defines their stylometric constraints. During the Tool Execution phase of the pipeline, the Voice Tracker utilizes NLP speaker attribution algorithms 44 to isolate all dialogue generated for specific characters. It maps this new dialogue against the established latent space vector for that character.

If a character defined by terse, uneducated, phonetic syntax is suddenly generated speaking in sweeping, polysyllabic, academic prose, the Voice Tracker detects the stylometric divergence. The system rejects the generation and passes a linting error back to the drafting model, demanding a rewrite that adheres to the established character voice vector.43 Furthermore, integrating models that analyze Markov chains of character speech allows the system to intentionally utilize defamiliarization and foregrounding techniques, intentionally breaking standard predictive capacities to create highly memorable, abrupt voice switches that elevate the artistic quality of the prose.46

### **Plot Hole Detection via Symbolic World-State Graphs**

The most jarring failure in generated narratives is the plot hole—an inconsistency that breaks the internal logic, rules, or causality of the fictional world.47 Plot hole detection is an incredibly complex task for neural networks, as it serves as a proxy for evaluating high-level reasoning skills, state tracking, pragmatic understanding, and theory of mind.48

To maintain internal logic over a massive context window, Narracode must deploy an internal testing framework analogous to the integration testing suites used in software development. Drawing inspiration from the "FlawedFictions" benchmark—which evaluates language models based on their ability to detect and reason about plot holes 48—Narracode can employ a secondary subagent acting as a dedicated "Critic."

This Critic Subagent operates concurrently with the primary drafting loop. Its sole responsibility is to construct and maintain a symbolic world-state graph of the narrative. Every time an action occurs within the drafted text (e.g., a character acquires a crucial item, a physical location is destroyed, a character learns a secret), the Critic parses the semantic text and updates the boolean properties and relational edges of the entities within the state graph.  
Before a newly drafted chapter is approved and committed to the canonical text archive, the Critic Subagent cross-references the text against the world-state graph. If the generated text violates the established physics, chronological reality, or entity states of the universe (e.g., generating a scene where a character utilizes an item that was explicitly lost three chapters prior), the output is categorically rejected. A highly specific error trace is generated based on the graph violation and fed back into the narrativeLoop for correction. This guarantees that regardless of token decay or compaction losses, the physical and causal logic of the narrative remains impenetrable.

## **Conclusion**

The transformation of the Narracode prototype from a basic algorithmic text generator into a robust, agentic storytelling environment requires a profound synthesis of software engineering architecture and computational narratology. The limitations of sequential neural poetry generation can only be overcome by adopting the autonomous, iterative, and heavily infrastructural paradigms exemplified by Anthropic's Claude Code.

By extracting the core mechanisms of Claude Code—specifically the unvarying nine-step queryLoop, the rigorous five-layer context compaction pipeline, the utilization of MCP for external data integration, and the stabilizing force of a teleological "Mythos" context—Narracode establishes a resilient foundation capable of managing immense narrative complexity.

Upon this software engineering foundation, the integration of advanced literary algorithms elevates the system from a coding assistant to a creative collaborator. The Emotional Arc Modeling Harness, powered by multi-label sentiment classifiers, ensures that generation is inextricably bound to predetermined psychological trajectories. The implementation of IPOCL and CPOCL planners guarantees that emotional shifts are earned through logical, intent-driven conflict, while lexical pacing algorithms govern the density of narrative momentum. Finally, the inclusion of cognitive stylometry tracking and symbolic world-state plot hole detection guarantees that the generated prose maintains the unique character voices and causal logic characteristic of high-quality human literature.

Through this exhaustive architectural redesign, Narracode ceases to be a mere autocomplete mechanism. It evolves into a fully autonomous, logically sound, and emotionally intelligent narrative engine, representing the forefront of augmented human creativity.

#### **Works cited**

1. GitHub \- jhave/TSNE-animator: testing a way to perceive data as fluid animated form\!, accessed May 17, 2026, [https://github.com/jhave/TSNE-animator](https://github.com/jhave/TSNE-animator)  
2. jhave \- GitHub, accessed May 17, 2026, [https://github.com/jhave](https://github.com/jhave)  
3. jhave/pytorch-poetry-generation \- GitHub, accessed May 17, 2026, [https://github.com/jhave/pytorch-poetry-generation](https://github.com/jhave/pytorch-poetry-generation)  
4. a port of the Wavenet algorithm to generate poems (using Samuel Graván's @Zeta36 code). \- GitHub, accessed May 17, 2026, [https://github.com/jhave/Wavenet-for-Poem-Generation](https://github.com/jhave/Wavenet-for-Poem-Generation)  
5. GitHub \- jhave/Big-Data-Poetry, accessed May 17, 2026, [https://github.com/jhave/Big-Data-Poetry](https://github.com/jhave/Big-Data-Poetry)  
6. Claude Code — Rebuilt from Leaked Source \- GitHub, accessed May 17, 2026, [https://github.com/fazxes/claude-code](https://github.com/fazxes/claude-code)  
7. AI Updates | A Research Resource \- Glia.ca, accessed May 17, 2026, [https://glia.ca/AI-updates/](https://glia.ca/AI-updates/)  
8. Rebuilt Claude Code CLI in TypeScript for full local use, with React \+ Ink UI and unlocked slash commands \- GitHub, accessed May 17, 2026, [https://github.com/Zeldr6422/claude-code-rebuilt](https://github.com/Zeldr6422/claude-code-rebuilt)  
9. Sun Chenxing Magician-MO \- GitHub, accessed May 17, 2026, [https://github.com/Magician-MO](https://github.com/Magician-MO)  
10. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems \- arXiv, accessed May 17, 2026, [https://arxiv.org/abs/2604.14228](https://arxiv.org/abs/2604.14228)  
11. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems, accessed May 17, 2026, [https://www.researchgate.net/publication/403904958\_Dive\_into\_Claude\_Code\_The\_Design\_Space\_of\_Today's\_and\_Future\_AI\_Agent\_Systems](https://www.researchgate.net/publication/403904958_Dive_into_Claude_Code_The_Design_Space_of_Today's_and_Future_AI_Agent_Systems)  
12. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems \- arXiv, accessed May 17, 2026, [https://arxiv.org/html/2604.14228v1](https://arxiv.org/html/2604.14228v1)  
13. VILA-Lab/Dive-into-Claude-Code \- GitHub, accessed May 17, 2026, [https://github.com/VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)  
14. architecture.md \- VILA-Lab/Dive-into-Claude-Code \- GitHub, accessed May 17, 2026, [https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md)  
15. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems \- arXiv, accessed May 17, 2026, [https://arxiv.org/pdf/2604.14228](https://arxiv.org/pdf/2604.14228)  
16. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems \- Zhiqiang Shen, accessed May 17, 2026, [https://zhiqiangshen.com/projects/Claude\_Code\_Report/Claude\_Code\_Report.pdf](https://zhiqiangshen.com/projects/Claude_Code_Report/Claude_Code_Report.pdf)  
17. 1jehuang/jcode: Coding Agent Harness \- GitHub, accessed May 17, 2026, [https://github.com/1jehuang/jcode](https://github.com/1jehuang/jcode)  
18. Claude-code/README.md at main · fazxes/Claude-code · GitHub, accessed May 17, 2026, [https://github.com/fazxes/Claude-code/blob/main/README.md](https://github.com/fazxes/Claude-code/blob/main/README.md)  
19. Claude-code/CLAUDE.md at main · fazxes/Claude-code \- GitHub, accessed May 17, 2026, [https://github.com/fazxes/Claude-code/blob/main/CLAUDE.md](https://github.com/fazxes/Claude-code/blob/main/CLAUDE.md)  
20. Agentic Workflows with Claude: Architecture Patterns, Design Principles & Production Patterns | by Reliable Data Engineering | Medium, accessed May 17, 2026, [https://medium.com/@reliabledataengineering/agentic-workflows-with-claude-architecture-patterns-design-principles-production-patterns-72bbe4f7e85a](https://medium.com/@reliabledataengineering/agentic-workflows-with-claude-architecture-patterns-design-principles-production-patterns-72bbe4f7e85a)  
21. Beyond Plot: How Sentiment Analysis Reshapes Our Understanding of Narrative Structure, accessed May 17, 2026, [https://culturalanalytics.org/article/id/990/](https://culturalanalytics.org/article/id/990/)  
22. Editors' Choice: Beyond Plot: How Sentiment Analysis Reshapes Our Understanding of Narrative Structure \- Digital Humanities Now, accessed May 17, 2026, [https://digitalhumanitiesnow.org/2025/09/beyond-plot-how-sentiment-analysis-reshapes-our-understanding-of-narrative-structure/](https://digitalhumanitiesnow.org/2025/09/beyond-plot-how-sentiment-analysis-reshapes-our-understanding-of-narrative-structure/)  
23. EmotionArcs: Emotion Arcs for 9,000 Literary Texts \- ACL Anthology, accessed May 17, 2026, [https://aclanthology.org/2024.latechclfl-1.7.pdf](https://aclanthology.org/2024.latechclfl-1.7.pdf)  
24. Audio-visual Sentiment Analysis for Learning Emotional Arcs in Movies \- MIT Media Lab, accessed May 17, 2026, [https://web.media.mit.edu/\~echu/assets/projects/emotional-arcs/11.2017.ICDM.pdf](https://web.media.mit.edu/~echu/assets/projects/emotional-arcs/11.2017.ICDM.pdf)  
25. Emotion Arcs of Student Narratives \- ACL Anthology, accessed May 17, 2026, [https://aclanthology.org/2020.nuse-1.12.pdf](https://aclanthology.org/2020.nuse-1.12.pdf)  
26. Narrative Theory for Computational Narrative Understanding, accessed May 17, 2026, [https://people.ischool.berkeley.edu/\~dbamman/pubs/pdf/piper\_so\_bamman\_emnlp2021.pdf](https://people.ischool.berkeley.edu/~dbamman/pubs/pdf/piper_so_bamman_emnlp2021.pdf)  
27. Sentiment Analysis (with examples) \- Hex, accessed May 17, 2026, [https://hex.tech/templates/sentiment-analysis/sentiment-analysis/](https://hex.tech/templates/sentiment-analysis/sentiment-analysis/)  
28. Detecting Story Arcs with Orange, accessed May 17, 2026, [https://orangedatamining.com/blog/detecting-story-arcs-with-orange/](https://orangedatamining.com/blog/detecting-story-arcs-with-orange/)  
29. The emotional arcs of stories: Python tutorial \- Leonardo Rizzo, accessed May 17, 2026, [https://www.leonardorizzo.com/2020/10/emotional-arcs-stories-python-tutorial/](https://www.leonardorizzo.com/2020/10/emotional-arcs-stories-python-tutorial/)  
30. Quantifying Emotional Tone in Tolkien's The Hobbit: Dialogue Sentiment Analysis with RegEx, NRC-VAD, and Python \- arXiv, accessed May 17, 2026, [https://arxiv.org/html/2512.10865v1](https://arxiv.org/html/2512.10865v1)  
31. All Stories Are One Story: Emotional Arc Guided Procedural Game Level Generation \- arXiv, accessed May 17, 2026, [https://arxiv.org/html/2508.02132v1](https://arxiv.org/html/2508.02132v1)  
32. Sentiment and Perception Analysis — Stromy Intel, accessed May 17, 2026, [https://stromy.com.au/solutions/intel/sentiment-perception-analysis/](https://stromy.com.au/solutions/intel/sentiment-perception-analysis/)  
33. Media Monitoring | Real-Time Narrative Tracking \- Rhetor's AI, accessed May 17, 2026, [https://rhetor.ai/solutions/media-monitoring](https://rhetor.ai/solutions/media-monitoring)  
34. Brand Reputation Monitoring in 2026: The Narrative Intelligence Guide, accessed May 17, 2026, [https://www.pulsarplatform.com/guides/how-to-monitor-brand-narrative-measure-belief-shift](https://www.pulsarplatform.com/guides/how-to-monitor-brand-narrative-measure-belief-shift)  
35. All Stories Are One Story: Emotional Arc Guided Procedural Game Level Generation, accessed May 17, 2026, [https://www.researchgate.net/publication/394293741\_All\_Stories\_Are\_One\_Story\_Emotional\_Arc\_Guided\_Procedural\_Game\_Level\_Generation](https://www.researchgate.net/publication/394293741_All_Stories_Are_One_Story_Emotional_Arc_Guided_Procedural_Game_Level_Generation)  
36. Why Every Beloved Show Relies on This Mind-Blowing Trope \- Rice University, accessed May 17, 2026, [https://dev-housing.rice.edu/tutorials/why-every-beloved-show-relies-on-this-mind-blowing-trope-4437474](https://dev-housing.rice.edu/tutorials/why-every-beloved-show-relies-on-this-mind-blowing-trope-4437474)  
37. The 5-Stages of Brain Rot: How Better Content Creation Is Making Your Audience Worse, accessed May 17, 2026, [https://medium.com/@menoverse/the-5-stages-of-brain-rot-how-better-content-creation-is-making-us-cognitively-weaker-98a241ac0ef7](https://medium.com/@menoverse/the-5-stages-of-brain-rot-how-better-content-creation-is-making-us-cognitively-weaker-98a241ac0ef7)  
38. Computational Approaches to Detecting Narrative Frames \- Digital Humanities 2017, accessed May 17, 2026, [https://dh2017.adho.org/abstracts/172/172.pdf](https://dh2017.adho.org/abstracts/172/172.pdf)  
39. Pacing Within the Narrative Arc \~ September C. Fawkes \- Editor, Writer, Instructor, accessed May 17, 2026, [https://www.septembercfawkes.com/2022/03/pacing-within-narrative-arc.html](https://www.septembercfawkes.com/2022/03/pacing-within-narrative-arc.html)  
40. \[1401.3841\] Narrative Planning: Balancing Plot and Character \- arXiv, accessed May 17, 2026, [https://arxiv.org/abs/1401.3841](https://arxiv.org/abs/1401.3841)  
41. A Computational Model of Plan-Based Narrative Conflict at the Fabula Level, accessed May 17, 2026, [https://cs.uky.edu/\~sgware/reading/papers/ware2014conflict.pdf](https://cs.uky.edu/~sgware/reading/papers/ware2014conflict.pdf)  
42. The Anxiety of Prestige in Stephen King's Stylistics | Journal of Computational Literary Studies, accessed May 17, 2026, [https://jcls.io/article/id/3915/](https://jcls.io/article/id/3915/)  
43. Improving Quotation Attribution with Fictional Character Embeddings \- arXiv, accessed May 17, 2026, [https://arxiv.org/html/2406.11368v1](https://arxiv.org/html/2406.11368v1)  
44. Improving Quotation Attribution with Fictional Character Embeddings \- ACL Anthology, accessed May 17, 2026, [https://aclanthology.org/2024.findings-emnlp.744.pdf](https://aclanthology.org/2024.findings-emnlp.744.pdf)  
45. AI Persona Bots for Literature: How to Interview Fictional Characters with AI Technology, accessed May 17, 2026, [https://estha.ai/blog/ai-persona-bots-for-literature-how-to-interview-fictional-characters-with-ai-technology/](https://estha.ai/blog/ai-persona-bots-for-literature-how-to-interview-fictional-characters-with-ai-technology/)  
46. Cognitive stylometry: A computational study of defamiliarization in modern Chinese, accessed May 17, 2026, [https://www.cambridge.org/core/journals/computational-humanities-research/article/cognitive-stylometry-a-computational-study-of-defamiliarization-in-modern-chinese/806CD4721AEC85C07473396825C3D7DD](https://www.cambridge.org/core/journals/computational-humanities-research/article/cognitive-stylometry-a-computational-study-of-defamiliarization-in-modern-chinese/806CD4721AEC85C07473396825C3D7DD)  
47. Identifying plot holes in narrative stories by simulating events \- UT Student Theses, accessed May 17, 2026, [https://essay.utwente.nl/fileshare/file/91967/Davids\_BA\_EEMCS.pdf](https://essay.utwente.nl/fileshare/file/91967/Davids_BA_EEMCS.pdf)  
48. \[2504.11900\] Finding Flawed Fictions: Evaluating Complex Reasoning in Language Models via Plot Hole Detection \- arXiv, accessed May 17, 2026, [https://arxiv.org/abs/2504.11900](https://arxiv.org/abs/2504.11900)  
49. Finding Flawed Fictions: Evaluating Complex Reasoning in Language Models via Plot Hole Detection | OpenReview, accessed May 17, 2026, [https://openreview.net/forum?id=ptmgWRCWmu](https://openreview.net/forum?id=ptmgWRCWmu)  
50. Finding Flawed Fictions: Evaluating Complex Reasoning in Language Models via Plot Hole Detection \- arXiv, accessed May 17, 2026, [https://arxiv.org/html/2504.11900v1](https://arxiv.org/html/2504.11900v1)  
51. NarraBench: A Comprehensive Framework for Narrative Benchmarking \- ACL Anthology, accessed May 17, 2026, [https://aclanthology.org/2026.eacl-long.176.pdf](https://aclanthology.org/2026.eacl-long.176.pdf)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAYCAYAAAB9ejRwAAABu0lEQVR4Xu2VPyhGYRTGT2LwLyRkwo5JWExmk0lhk0kWi0U2KaVkQDKQMhiVTclmtZiEiVIkxeDfeXrvW8fz3XP5Pt94f/XUvb9z7r3v+33ve69ITs4P3lg4PGmqWKYxpjn6Y9K40bSwzOCLRRoYeZuEZqRVU6eplfCwAc1tUmPWNXssDWsslEHNC0sPPPSTpSFtUGkuciB+Hb6dJdMnoXGVCwZ+wLSENeKB/keWCUuaV5YM1gtu0mhcpWbHnD+bY4D+BXIW1GdYJjRL4SQLiOvJcqHpIGdBfz25qcRzOk1PBL6JpYVvkjZIJqt+KNl1gPoIy0i/hIZl43oT54EZZtVRe2BJoGeOZeRYQgNeA5EKzZY539RUm/Me+X1QsywJ9GywjJTyV2EC7CLdEmqYWBbocTcKiu8sDfuaUZbiD4rXk7cD0TPJEgxJKK5wIWFc/IfD17CU4O0b+94cW9Bnl4RMaM6TAnKlOdWcaM4016a2Gy4pALV5lhI+Pah1if8PNIg/2X+xLf4Ow/dzmKVhUXPJslyUOltcxy/esoFF7W5rB7xOvG9i2cCiLmbWpf66RfPBwuFOaMflFMs3XLh7+eX1I4oAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAZCAYAAAC2JufVAAAB70lEQVR4Xu2WTyhFQRTGjz8hsqKsZGOJZCHJSgnFRiJRVsJCWSiysUKUlawsFVkoC0shJfkTZYUF9jaUogjnvJnbO743M+/p9bLxq6937/fNmXvnvrkzlyg5A6xGNP+SUdYT643VDtmfMMI6Ved3rA51/k+67LNK0HTQw5pE00UVaydFFdkazRRrGs0AZ6xmNJFsMqP8sqpgFbMKrV/LOrEZUsn6RFMxw8pDk9x9OYluyocre6XwqKWmGk1mhXWJJpJDpoNQQ7ypXIenGadwHspiTJBp1Am+LAkR2MkWmbXMxyMl1mgka0VT80yJHayyBsHTSPtFNCk+DbQedAOLDPgCTQ12EimE5N1oWrLI5K75FLFJgWtEc0PesIgC64WQvA5Nyxglr5+nQBtZzCRsA/9WHfdR4gYtNaXgRSSbT4Lssd42LxQILa5cPFnDXEi2jSYwR+5+Y0jgDZkh1jKaZGq60KT4fNJ/7bA6jtggz3XzyQTnGFjkSTgLyfizaDK99LPmRh1rxD/ShozimPVBpgOZA4esPft7bX3Rva1B1sj89YhsK1JXxjpgNfxI40ibfjTTpZz8T1GQr1fZV32EatNCOq5HMwUWyDzFjFDDekczBWQwst9mjHVyv10+dllNaGaCK3J/ACItrCU0//kN3935gl2Gp/CfAAAAAElFTkSuQmCC>