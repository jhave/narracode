# Blind reading pilot — UNFINISHED CHECKPOINT

Paused at the author’s request on 2026-09-07 to limit cost. Resume during the week of September 14 if requested; no background work is scheduled.

## Saved
- Twelve frozen baseline passages, 231–412 words, from six projects; exact source spans, hashes, and provenance caveats in samples.json.
- Source selection script. Do not rerun over future variants without preserving the dataset.
- App source in app/: representative reading page, four-arm assignment logic, session/response/finish/reveal/export routes, and generated two-table migration.
- A Sites project was registered but never deployed. Reuse its project_id from app/.openai/hosting.json; do not register a duplicate. No credentials are saved.

## Not done — do not deploy or recruit readers yet
- Only baseline text exists. The other three variants per sample have NOT been written. The server expects these variants and is not usable as a study yet.
- The page is an early static preview. Its controls are not wired to the API.
- Migration generated, not verified/applied to a study database. No participant data collected.
- No production build, API integration tests, blind-leak tests, or deployment completed. Starter dependencies reported 14 audit advisories (6 moderate, 8 high); assess reachable impact before deployment rather than applying a blind forced upgrade.
- Ratings and response collection need completion, including reload/resume, errors, skip/tie/neither, and locking before reveal.
- Validate that labels, source paths, and condition keys never enter the blind client payload; audit exports and concurrent finish/save behavior.

## Next iteration
1. Agree a modest generation budget. Generate and freeze 36 revision variants (200–450 words each), with exact method/model provenance. Keep failures and identical outcomes rather than manufacturing differences.
2. Complete the interface. Each reviewer sees two versions of each source; the six possible pairs appear twice, with randomized source and A/B order stored per session.
3. Run focused persistence, assignment balance, validation, and confidentiality tests. Exclude test responses from analysis.
4. Build and deploy privately, then decide how to invite readers. Keep scoring about literary effect and voice; Pangram is optional and not a generation target.

The original working copy was in the workspace’s sibling ai-tells-pilot directory; the repository copy in app/ is this checkpoint’s durable source. The preview server was stopped.
