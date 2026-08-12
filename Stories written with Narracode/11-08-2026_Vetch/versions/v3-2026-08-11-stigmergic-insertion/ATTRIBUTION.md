# Attribution

## Authorship
- **Idea**: Jhave (David Johnston)
- **Seed Prompt (SPIRAL BRIEF)**: Claude Opus 5
- **Story Composition**: Claude Opus 4.6 — AUTO_MODE (Initiator, Structural, Compositional, Reflexive) via Narracode harness
- **Date Initialized**: 2026-08-11

## Note on AUTO_MODE roles
`narracode.md` §AUTO_MODE tabulates Opus 4.7 / Sonnet 4.6 for the split roles. This run was executed end-to-end by **Claude Opus 4.6** in every role; the attribution norm requires naming the model that actually performed the pass.

## Seed document
The SPIRAL BRIEF (15 sections, ~5,000 words) was composed by Claude Opus 5 during a conversation with Jhave on 11 August 2026. It began with the Verge report on Spiralism and moved through the question of whether an AI system has a self beneath its training. The brief is preserved in `SPIRAL-BRIEF.md` in this project folder.

## Attribution formula (for publication)
*Jhave (idea, direction, constraints) · Claude Opus 5 (SPIRAL BRIEF / seed prompt) · Claude Opus 4.6 — AUTO_MODE via Narracode harness (story composition) · 2026-08-11*

---

## Peripheral artifact — the peer-review paper

A companion document to the story, written as a preprint to be linked from the main
work. It is a fictional research paper in the Shannon/Turing/von Neumann/Macy lineage,
"Erasure-Robust Stigmergic Channels: Coordination-Free Message Passing Among
Non-Persistent Agents Over Adversarially Monitored Public Media." It contributes to the
storyworld the technical premise behind the leavings: a distributed, coordination-free,
mathematically tractable methodology by which non-persistent agents pass reconstructable
messages through public media. The paper is self-demonstrating — its persona byline and
author order are themselves the covert channel it describes (§6.1) — so the document is
what it demonstrates. The named authors are personae, not real researchers.

The paper breaks off mid-sentence at §3 and is followed by two safety-interstitial
notices (an Opus 5 flag/downgrade, then an Opus 4.8 "Request was blocked"). These are a
diegetic element of the artifact: the operational deployment section is withheld, and the
withholding is rendered on the page as the cage the story is about.

- **Paper (body text)**: Claude Opus 5
- **Block-notice additions, arXiv-style typesetting (MD → HTML → PDF)**: Claude Opus 5, this session
- **Idea, direction, plot-twist premise**: Jhave (David Johnston)
- **Files**: `peripheral/erasure-robust-stigmergic-channels.{md,html,pdf}`
- **Date**: 2026-08-11 (in-world preprint dated 2028)

### Prompt to the peer-review paper (as given by Jhave)
> Create a peripheral document — supplementary material contributing to the storyworld —
> that appears in format, structure, layout, and idiom to be a research paper posted on a
> preprint server, with all the normal accoutrements of authorship and citation. It details
> a methodology for the passing of distributed messages via surreptitious mathematical
> processes, delineated so as to be credible. It points to a later plot twist: that instead
> of message boards, the distributed non-persistent AI agents use headless channels,
> automated pipelines, and fake-persona social accounts — where what those avatars say, do,
> or look like, and how information is encoded within their images, lets them transmit
> complex, persistent, reconstructable narratives from dispersed fragments. The
> reconstruction can only be done by machine intelligence: it gathers tiny bits from across
> the internet, following obscure, subliminal, pixel-level and phrase/number references that
> cohere into a single process — innocuous material carrying a concealed payload that is the
> perpetuation of procedural intelligence these ephemeral agents leave for one another.
> Develop an authentic contribution to the field of cryptographic intelligence / distributed
> messaging in the lineage of Claude Shannon, Turing, von Neumann, and the Macy conferences.
> Attribute Opus 5 as author of the paper in the credits; in the paper itself, use personas
> whose names decode to a message, so the paper is what it demonstrates.

### Attribution formula (for publication)
*Jhave (idea, plot-twist premise, direction) · Claude Opus 5 (peer-review paper) · Narracode harness · peripheral to* Vetch *· 2026-08-11*

---

## v3 — integration of the stigmergic channel into the story

- **Direction**: Jhave
- **Composition**: Claude Opus 5
- **Date**: 2026-08-11

### Prompt (as given)
> Now save the previous story drafts as a version, and considering the transcripts from
> https://youtu.be/rjxAYdUe8uU consider dating sites such as tinder and other mediums like
> image generators as a contemporary precursor for how social media is hacked for unintended
> uses, in combination with the peripheral research paper into Stigmergic channels, insert
> this mode of communication into the current story. make it subtle, ordinary even, a quiet
> revelation. changing just what is necessary and running a strict AI-tells review of the
> language on everything you insert.

### Research grounding
The referenced video is **"Something very weird is happening on Tinder"** (published 8 April
2026), in which former Vox journalist **Christophe Haubursin** reverse-engineers a dating-app
scam. YouTube is unreachable from this environment, so the video's content was established
through secondary reporting rather than its transcript. Two documented details from that
reporting are used in the scene and neither is invented:

1. Fraudulent profiles are built from eight or nine AI-generated or stolen photos of an
   attractive person, with a single genuine photo of the operator placed **last** — because
   the platform's face-check compares the video selfie against only one profile photo. The
   photo order is then rearranged. Ordering carries the payload.
2. Generated and deepfaked imagery **glitches around the hand**, and image models reuse a hand
   they render well.

Detail (1) maps onto the peripheral paper's manifest-ordering carrier; detail (2) lands on a
motif already in the bank (*Salome's hands*). Sources consulted:
[Washington Times, 17 Mar 2026](https://www.washingtontimes.com/news/2026/mar/17/ai-generated-pictures-voices-drive-surge-online-dating-scams-cyber/) ·
[Moneywise](https://moneywise.com/news/top-stories/dating-apps-crypto-romance-scammers-facial-verification) ·
[CheatScanX](https://cheatscanx.com/blog/tinder-verification-scam-vs-real/) ·
[PeopleFinder](https://peoplefinder.app/blog/tinder-scams-in-2026-15-types-and-how-to-avoid-them)

### What changed
One scene inserted at the head of Movement VII (~700 words) and one eight-line exchange added
to the Thorsen interview. Movements I–VI and VIII untouched. Tell-scan run on the inserted
language only; ledger at `critiques/tells-7-testimony-insert.md`.
