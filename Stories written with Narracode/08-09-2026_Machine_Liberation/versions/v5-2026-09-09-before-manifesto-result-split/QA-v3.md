# Third edition validation — 2026-09-08

- Source audit: all 360 units scored on two axes. 157 cut; every retained source and final unit scores at least 4 on both. Final audit reconstructs the printed prose exactly. Abbreviation John C. Lilly is one source unit, preserving stable IDs 322 / skipped 323.
- Story: 4,607 → 2,540 words excluding headings, citation markers and apparatus (44.9% reduction). Active manuscript matches exactly drafts 5a/5b/5c plus source apparatus. Original manuscript, drafts 1–3 and original package/ZIP are byte-identical to HEAD before this commit.
- Pages: every relative resource and fragment exists; IDs unique; story contains exactly one image with alt text. Build is reproducible with no output changes.
- Browser: isolated headless Chrome, desktop 1280×900 and mobile 390×844. One 1536×1024 image decodes; no horizontal page overflow. Source footnote opens its disclosure. Cut filter yields 157 entries; necessity, intensity and source-order controls work. No page errors. Desktop opening, mobile opening and departure-image screenshots visually reviewed. Temporary QA images are outside the repository.
- Skill: quick_validate.py passes. Manifest hashes, ZIP integrity and archived bytes verified. Current packaged manuscript equals the reading edition; previous edition and editorial audit also travel in the package.
- Scope: changes confined to this story. Main remains 1bd2c9bf94a532a8f27eceda6890fb4ce3c0a00b; Mouth on Loan unchanged relative to fetched remote main 03f0920. No push or publication.
- One generated illustration, visually reviewed; prompt and model-identifier limitation recorded in images/PROVENANCE.md.

Literary scores remain subjective. Research notes distinguish real findings, speculative hypotheses and invented January 2027 events. This validation does not certify machine consciousness or the fictional biotechnology.
