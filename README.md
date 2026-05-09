# Narracode: a *Claude Code* for literature.

Computer code is a solved problem for AI. Why not literature? 

Narracode is a storytelling harness for agentic AI (inspired by Claude Code). It is a neurosymbolic approach to narrative generation.

It emerged from the realization that the intrinsic embodied complexity of nunanced narrative might become comptationally tractable by recursively entwining a LLM with a symbolic harness that is somehow equivalent to Claude Code https://github.com/weikma/claude-code-rebuilt specifically re-purposed for narrative literature.  

## Background Information on Claude Code (*how it became public*)

Claude Code is a CLI tool developed by Anthropic for AI-assisted software development. It has been extremely popular and is extremely powerful. 

On March 31, 2026, Anthropic accidentally leaked the full source code of Claude Code (the CLI coding agent) via a 59.8 MB source map file bundled in NPM package version 2.1.88. The leak revealed 500,000+ lines of TypeScript, including its system prompt, tool logic (bash, edit), and agentic loop, sparking widespread analysis. 

So now the architecture of the system is public. 

## Project Overview

Narracode arises from an inquiry: can we build a literature AI-augmentation system on the same model as Claude Code? One that is structured, algorithmic, agentic — but for literary purposes? 

Historically, AI falls into 2 camps: symbolic AI (plans, templates, expert systems) and connectionist AI (neural networks, large language models).  Symbolic AI has failed at narrative because it treats it as a planning problem. Connectionist AI has succeeded at generating text, but has failed to capture the deeper structures of narrative, the way that stories are not just strings of words, but systems of relations and atmospheres. 

Narracode is an attempt to bridge this gap. It is a neurosymbolic approach to narrative generation. It is a tool for orchestrating agents specifically for literary purposes. 

The core premise is that the architecture of a narrative generator is not neutral; rather, it is a "narrative philosophy" written in code. The structural logic of a program—its "Narracode"—acts as a set of cognitive and social presuppositions that fundamentally shape the generated story-world.

## Historical Computational Narrative Systems

*(This section synthesizes an analysis from a [Claude conversation on narrative architecture](https://claude.ai/share/c262de57-1678-4bf5-a437-260aac71b497))*

### CascadeMind (Kawada & Holyoak, 2026)
- **Type**: Neurosymbolic
- **Model**: Narrative similarity classification using a cascade architecture. Employs LLM neural voting with supermajority thresholds, falling back to a classical symbolic ensemble (lexical overlap, story grammar, tension) only when the LLM's uncertainty is too high.
- **Bias**: Designed for the SemEval-2026 challenge, optimizing for measurable "similarity" between texts, assuming narratives can be objectively weighed against one another through an ensemble of signals.
- **Presupposition**: Ambiguity and uncertainty are the primary obstacles in analyzing narratives. The architecture posits connectionist models as the default, utilizing symbolic structures merely as tie-breakers for the most uncertain scenarios.

### METATRON (Concepción et al., 2025)
- **Type**: Neurosymbolic
- **Model**: Narrative as the instantiation of classical European dramaturgy. Uses Georges Polti’s 36 dramatic situations as a symbolic planning substrate, with an LLM rendering the text and a coherence filter checking fidelity.
- **Bias**: A triple-layered bias combining 19th-century European theatrical canons, the LLM’s genre-heavy pretraining, and the coherence filter's aversion to deviation.
- **Presupposition**: Dramatic situations are a finite, enumerable set that precedes character interiority. It assumes stories have clear recognizable arcs (complication, catastrophe) and penalizes the emergence of new, unnamed narrative shapes.

### Affective Reasoner + ChatGPT (Clark Elliott, 2023)
- **Type**: Neurosymbolic
- **Model**: Narrative as emotionally-driven scenario generation. Uses the classic Affective Reasoner (based on the OCC cognitive model of emotion) as an underlying symbolic state engine to prompt an LLM to render the textual surface.
- **Bias**: Inherits the OCC model's highly structured, appraisal-based view of emotion (e.g., joy, distress, hope, fear as mathematical functions of goal-congruence and blameworthiness).
- **Presupposition**: Emotion can be formally categorized and mathematically appraised before language is applied. The symbolic engine calculates *how* a character feels, while the LLM merely translates that calculus into prose.

### CoRRPUS (Martin et al., 2022)
- **Type**: Neurosymbolic
- **Model**: Narrative understanding via Code-based Structured Prompting. Prompts LLMs to extract a structured, code-like "world model" from a story to track character locations, relationships, and logical states.
- **Bias**: Biased towards literal, physical, and state-machine-like interpretations of stories, where a character's state can be cleanly serialized as code.
- **Presupposition**: Linguistic neural networks are too flexible to maintain long-range coherence natively, requiring a symbolic code representation of the story state to prevent hallucination. 

### CAST (Peng, Li, Wiegreffe, Riedl, 2022)
- **Type**: Neurosymbolic
- **Model**: Narrative as goal-coherence over learned commonsense distributions. Uses an LLM to generate continuations, and the COMET commonsense inference graph to filter them for consistency with character intent.
- **Bias**: Relies on crowdworkers' annotations of human psychology, steering narratives toward legible, predictable, transactionally social behavior while filtering out complex, contemplative, or unpredictable literary moves.
- **Presupposition**: Coherence is the highest narrative virtue. It models the reader as constantly updating a mental model of what characters "would do next," making character action (rather than setting or silence) the unit of narrative interest.

### Façade (Michael Mateas & Andrew Stern, 2005)
- **Type**: Symbolic planning / Interactive Drama
- **Model**: Narrative as a tension-managed interactive social performance. Uses "beat" managers and behavioral engines to parse user input and orchestrate character responses in real-time.
- **Bias**: Focuses on the intense, upper-middle-class domestic breakdown of a married couple. Limits interaction to a bounded, pressure-cooker social etiquette.
- **Presupposition**: Narrative is a collection of dramatic beats structured by ascending tension. Characters are highly reactive agents managing their own social boundaries and psychological states in response to an unpredictable interactor.

### DayDreamer (Erik Mueller, 1989)
- **Type**: Symbolic planning
- **Model**: Narrative as interior monologue and recursive emotional simulation. Extends case-based reasoning with "daydreaming goals" (rationalization, revenge, recovery) that operate on emotional states.
- **Bias**: Reflects a 1980s Western, autonomous subjectivity. Fixates on instrumental interiority where daydreaming is a functional meta-planning process to resolve wounds, avoiding aimless wandering or unresolvable mourning.
- **Presupposition**: Mental life is goal-structured all the way down, even during rumination. Emotions are signals that mark episodes for re-processing toward closure, and the self is unified across counterfactuals.

### Racter (William Chamberlain & Thomas Etter, 1983)
- **Type**: Symbolic planning / Procedural generation
- **Model**: Narrative as surface-level lexical juxtaposition and template matching.
- **Bias**: Reflects the "pseudo-intellectual" and surrealist lexicon of its human curators.
- **Presupposition**: Meaning is an emergent property of syntax projected by the reader, rather than a deep simulation of intent. It operates on "timbral/mood-based" logic rather than strict planning.

### Tailspin (James Meehan, 1976)
- **Type**: Symbolic planning
- **Model**: Narrative as goal-driven problem solving (based on Roger Schank's Conceptual Dependency).
- **Bias**: Individualistic and Western-centric. Success is defined entirely by the achievement of private, material goals.
- **Presupposition**: The mind is a planning engine. The system operates under the assumption that characters lack an unconscious, social context, or collective meaning. It relies heavily on "causal chain" logic.

## Key Concepts

- **Code-as-Story**: The idea that algorithms themselves encode a worldview.
- **Narrative Weather vs. Planning**: The contrast between the rigid, causal-chain logic of planning systems (like Tailspin) and the atmospheric, syntactic logic of generative textual arrays (like Racter).
