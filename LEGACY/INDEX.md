# LEGACY/INDEX.md

A chronological table-of-contents for the narracode harness. Read this file first. From here, the front-matter inside each `narracode_*.md` chains you to the plan that proposed the change and to the previous and next versions. The point is to make the evolution of the system legible in plain text, without inspecting git branches.

## Versions

| Active dates | File | Derived from plan | One-line change |
|---|---|---|---|
| 2026-05-09 → 2026-05-11 | [narracode_2026-05-09T1820.md](narracode_2026-05-09T1820.md) | [plans/Claude Opus 4-7 details the first Narracode architecture (May 10,2026).md](../plans/Claude%20Opus%204-7%20details%20the%20first%20Narracode%20architecture%20%28May%2010%2C2026%29.md) | Initial harness. Five agent roles, externalised structural memory, draft/critique separation. No explicit hook surface yet. |
| 2026-05-11 → 2026-05-25 | [narracode_2026-05-11T0623.md](narracode_2026-05-11T0623.md) | (proposal D1 — commit a9abdaa) | Declared explicit hook surface (`on_init`, `pre_draft`, `on_draft`, `post_draft`, `post_draft_check`, `on_critique`, `on_check`, `on_drift`, `on_snapshot`, `on_new_direction`, `on_orient`). The `post_draft` silence becomes a first-class negative hook. |
| 2026-05-25 → *(current)* | [narracode_2026-05-25T0907.md](narracode_2026-05-25T0907.md) | (AUTO_MODE — commit 1b35f79) | Added AUTO_MODE: a setting that suspends human-confirmation pauses and chains passes automatically through a full Initiator → Compositional → Reflexive pipeline. Sonnet 4.6 drafts; Opus 4.7 governs. |

## In testing (not yet promoted)

| Proposed | File | Plan | Status |
|---|---|---|---|
| 2026-05-29 | [../narracode_2026-05-29T0611_testing.md](../narracode_2026-05-29T0611_testing.md) | [plans/2026-05-24_continual-harness-evaluation-affect-module-report.md](../plans/2026-05-24_continual-harness-evaluation-affect-module-report.md) | testing — awaits story selection and trial run; **does not yet contain AUTO_MODE**, see the reconciliation note in the plan. |

## Promotion ritual

When a tested harness is ready to become live:

1. Copy the tested file (`narracode_DATETIME_testing.md`) into `LEGACY/narracode_DATETIME.md` with `_testing` stripped from the name.
2. Edit the front-matter of the previously-active `LEGACY/<retiring>.md` to fill `superseded-by:` and close the `active:` date range.
3. Copy the same file's contents into the root `narracode.md` (overwriting the live file).
4. Add a row to the table above (with the new active range).
5. Rewrite the three lines of `LEGACY/ACTIVE.md`.
6. Update the corresponding plan's front-matter: set `status: implemented`, fill `implemented-in:`.

## Reading this archive

Each `narracode_*.md` file under `LEGACY/` begins with a front-matter block of seven fields:

- `active:` — the date range during which this version was the live harness.
- `derived-from-plan:` — the plan file that proposed the changes embodied here.
- `supersedes:` — the previous version this one replaced.
- `superseded-by:` — the next version that replaced this one (blank for current live).
- `git-sha:` — the commit hash for cross-reference with git, when needed.
- `one-line:` — a single-sentence summary of what changed.

Plans under `plans/` carry reciprocal front-matter with `status:`, `implemented-in:`, and `tested-on:` fields. Following these links in either direction reconstructs the architectural conversation.
