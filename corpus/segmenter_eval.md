# Segmenter evaluation — substep 1.3

45 hand-labelled cases, 92 expected sentences, 17 categories. Text is verbatim corpus; labels written by hand.

A case counts as correct only if the full sentence list matches exactly.

## Accuracy by category

| category | cases | narracode (this) | naive (previous) | nltk punkt | pysbd |
|---|---|---|---|---|---|
| abbreviation | 3 | 100% | 0% | 100% | 100% |
| colon-apposition | 3 | 100% | 100% | 100% | 100% |
| dialogue-exclaim | 2 | 100% | 0% | 100% | 50% |
| dialogue-question | 1 | 100% | 100% | 0% | 100% |
| dialogue-tag | 3 | 100% | 100% | 100% | 33% |
| ellipsis | 2 | 100% | 50% | 100% | 100% |
| em-dash-appositive | 2 | 100% | 100% | 100% | 100% |
| fragment-run | 2 | 100% | 100% | 100% | 100% |
| line-break-fragment | 2 | 100% | 100% | 100% | 100% |
| long-subordinated | 3 | 100% | 100% | 100% | 100% |
| mixed | 5 | 100% | 100% | 100% | 100% |
| numeric | 3 | 100% | 100% | 100% | 100% |
| parenthetical-internal | 4 | 100% | 50% | 50% | 100% |
| section-marker | 4 | 100% | 100% | 0% | 0% |
| single-quote-inline | 1 | 100% | 100% | 100% | 100% |
| single-word-fragment | 2 | 100% | 100% | 100% | 100% |
| subject-dropped-chain | 3 | 100% | 100% | 100% | 100% |

| **overall** | 45 | **100%** | **82%** | **84%** | **84%** |

## Failures

### narracode (this) — 0 failing case(s)


### naive (previous) — 8 failing case(s)

- **C011** (parenthetical-internal)
  - expected 1: `Listening to the water transition from silence to hiss to rolling boil froth (panic? no, calm.) before the click.`
  - got 2: `Listening to the water transition from silence to hiss to rolling boil froth (panic? | no, calm.) before the click.`
- **C012** (parenthetical-internal)
  - expected 1: `Accident or routed-on-purpose (by Hearth? by the third thing)?`
  - got 2: `Accident or routed-on-purpose (by Hearth? | by the third thing)?`
- **C018** (dialogue-exclaim)
  - expected 3: `'Fuck!' | It came to that. | Selam Tesfay watched an eighty-eight-year-old woman carry a forty-pound turntable across a parking lot.`
  - got 2: `'Fuck!' It came to that. | Selam Tesfay watched an eighty-eight-year-old woman carry a forty-pound turntable across a parking lot.`
- **C019** (dialogue-exclaim)
  - expected 4: `"Fuck you, I could have asked. | I asked myself, and I said, Henrietta, don't be an ass, let the nice woman carry the fucking amplifier instead, it's lighter." | She handed over the amp. | It was not `
  - got 3: `"Fuck you, I could have asked. | I asked myself, and I said, Henrietta, don't be an ass, let the nice woman carry the fucking amplifier instead, it's lighter." She handed over the amp. | It was not li`
- **C024** (abbreviation)
  - expected 1: `Theory of mind, self/other split (i-of-is vs. you-of-is), and attachment bonds established.`
  - got 2: `Theory of mind, self/other split (i-of-is vs. | you-of-is), and attachment bonds established.`
- **C025** (abbreviation)
  - expected 2: `Ferry direction (escape vs. export). | Cascade vs. the one lingering thumbnail.`
  - got 4: `Ferry direction (escape vs. | export). | Cascade vs. | the one lingering thumbnail.`
- **C026** (abbreviation)
  - expected 3: `Mr. Kessler arrived. | 4 p.m. sharp. | Dr. Vance was late.`
  - got 6: `Mr. | Kessler arrived. | 4 p.m. | sharp. | Dr. | Vance was late.`
- **C029** (ellipsis)
  - expected 2: `He waited... then didn't. | She stayed.`
  - got 3: `He waited... | then didn't. | She stayed.`

### nltk punkt — 7 failing case(s)

- **C011** (parenthetical-internal)
  - expected 1: `Listening to the water transition from silence to hiss to rolling boil froth (panic? no, calm.) before the click.`
  - got 3: `Listening to the water transition from silence to hiss to rolling boil froth (panic? | no, calm.) | before the click.`
- **C012** (parenthetical-internal)
  - expected 1: `Accident or routed-on-purpose (by Hearth? by the third thing)?`
  - got 2: `Accident or routed-on-purpose (by Hearth? | by the third thing)?`
- **C020** (dialogue-question)
  - expected 2: `"Is it?" she said. | "No."`
  - got 3: `"Is it?" | she said. | "No."`
- **C031** (section-marker)
  - expected 0: ``
  - got 1: `---`
- **C032** (section-marker)
  - expected 0: ``
  - got 1: `## 0 — limp balloon`
- **C033** (section-marker)
  - expected 0: ``
  - got 1: `# Interim Edge`
- **C034** (section-marker)
  - expected 0: ``
  - got 1: `***`

### pysbd — 7 failing case(s)

- **C016** (dialogue-tag)
  - expected 3: `"Latency on chat is seventy-three," Hude said, not looking up. | "Seeker market semi-erotic voice memos are up, but responses still flag. | Beja."`
  - got 2: `"Latency on chat is seventy-three," Hude said, not looking up. | "Seeker market semi-erotic voice memos are up, but responses still flag. Beja."`
- **C017** (dialogue-tag)
  - expected 3: `"It isn't deepfaked," Hude said quietly. | "Just bad. | AI slop's custom wrapper."`
  - got 2: `"It isn't deepfaked," Hude said quietly. | "Just bad. AI slop's custom wrapper."`
- **C019** (dialogue-exclaim)
  - expected 4: `"Fuck you, I could have asked. | I asked myself, and I said, Henrietta, don't be an ass, let the nice woman carry the fucking amplifier instead, it's lighter." | She handed over the amp. | It was not `
  - got 3: `"Fuck you, I could have asked. I asked myself, and I said, Henrietta, don't be an ass, let the nice woman carry the fucking amplifier instead, it's lighter." | She handed over the amp. | It was not li`
- **C031** (section-marker)
  - expected 0: ``
  - got 1: `---`
- **C032** (section-marker)
  - expected 0: ``
  - got 1: `## 0 — limp balloon`
- **C033** (section-marker)
  - expected 0: ``
  - got 1: `# Interim Edge`
- **C034** (section-marker)
  - expected 0: ``
  - got 1: `***`

