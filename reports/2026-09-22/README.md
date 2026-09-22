# September 22, 2026 audit

Report: `../../2026-09-22_narracode-project-report.html`.

- `audit.json`: inventory, branch commit pins, method, totals, and complete daily data.
- `daily-counts.csv`: all 137 dates from May 9 through September 22, including zero-start dates.
- `image-prompt.md`: complete image prompt and generation provenance.

## Counting rules

Count one distinct project once at its dated folder / attribution start. Do not count scenes, snapshots, peripheral papers, reports, worktree copies, or the September 4 Machine Liberation precursor as additional projects. Folder dates are project-start proxies, not verified completion dates. The main library sorts separately by dated edition.

32 indexed works + 4 held projects = 36 distinct projects. There are 37 dated directories across current branch tips when the alternate Machine Liberation attempt is included. The older What Did Not Begin directory is a rename of Mature Water.

The held projects remain on their branches. Listing them in the recovery report is not publication as story cards or approval of completion.

## Reproduction

From the repository root, run `python3 tools/audit_library.py`. The baseline and branch objects are pinned in that script. `library-snapshot.json` freezes the dates and edition metadata used for this audit, so later public-library additions cannot change the dated counts.

For future index changes, edit `library.json` and run `python3 build_main_index.py`. `library-template.html` preserves the page layout. Do not regenerate published story pages as part of a root-index repair.
