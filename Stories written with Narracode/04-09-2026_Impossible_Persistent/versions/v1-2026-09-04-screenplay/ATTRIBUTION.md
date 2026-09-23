# Attribution

## Authorship
- **Human Author**: Jhave (seed prompt, direction, constraints)
- **Story Composition**: Claude Opus 5 — AUTO_MODE (Initiator, Structural, Compositional, Reflexive) via Narracode harness
- **Date Initialized**: 2026-09-04

## Note on requested vs. actual model roles
The prompter requested **Claude Opus 4.6** as the Compositional agent and **Claude Opus 5** as the Reflexive agent. This session's configured and serving model is `claude-opus-5` in every pass; Opus 4.6 was not addressable from inside this run. The attribution norm in `narracode.md` requires naming the model that actually performed each pass, so every role below is recorded as Opus 5, and the requested split is recorded here rather than asserted as fact.

| Role | Requested | Actually performed by |
|---|---|---|
| Initiator | — | Claude Opus 5 |
| Structural | — | Claude Opus 5 |
| Compositional | Claude Opus 4.6 | Claude Opus 5 |
| Reflexive | Claude Opus 5 | Claude Opus 5 |

`narracode.md` §AUTO_MODE tabulates Opus 4.7 / Sonnet 4.6 as the default split; that table was superseded for this run by the prompter's instruction, and then by availability.

## Attribution formula (for publication)
*Jhave (seed prompt, direction, constraints) · Claude Opus 5 — AUTO_MODE via Narracode harness · 2026-09-04*
