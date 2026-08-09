# Sentence segmentation test cases — substep 1.3

All text is **verbatim from the corpus**. Expected segmentation was written by hand by
reading each passage, not by running any segmenter.

Format: `### <id> | <category> | <source story>`, then `TEXT:` on one line, then `EXPECT:`
followed by one `- ` line per expected sentence. An empty EXPECT means the input yields no
sentences (section markers, headings).

Fixed decisions applied throughout:

1. A dialogue tag attaches to the quoted sentence it reports: `"You could've asked," Selam said.` is **one** sentence.
2. A closing quote that ends a complete utterance terminates that sentence: `'Fuck!' It came to that.` is **two**.
3. Punctuation inside parentheses or brackets never splits.
4. A line break terminates a sentence when the line has no terminal punctuation.
5. Markdown headings, horizontal rules and figure labels yield no sentences.
6. Known abbreviations do not terminate.

---

### C001 | fragment-run | TheCompulsionLoop
TEXT: Set it on the couch. Stood. Walked to the window. Wtf. I stayed calm. Pretended to keep reading.
EXPECT:
- Set it on the couch.
- Stood.
- Walked to the window.
- Wtf.
- I stayed calm.
- Pretended to keep reading.

### C002 | fragment-run | TheCompulsionLoop
TEXT: The window on Greel Street looked onto an interior courtyard. A brick wall, a drainpipe, a strip of sky. He stood looking at it.
EXPECT:
- The window on Greel Street looked onto an interior courtyard.
- A brick wall, a drainpipe, a strip of sky.
- He stood looking at it.

### C003 | subject-dropped-chain | TheCompulsionLoop
TEXT: My wife came through from the kitchen with a glass, looked at the boy at the window, looked at me. Said nothing.
EXPECT:
- My wife came through from the kitchen with a glass, looked at the boy at the window, looked at me.
- Said nothing.

### C004 | subject-dropped-chain | Interim_Edge
TEXT: Emptied the drains into the compost. Rinsed the holder. Put in a fresh filter. Poured the water.
EXPECT:
- Emptied the drains into the compost.
- Rinsed the holder.
- Put in a fresh filter.
- Poured the water.

### C005 | subject-dropped-chain | Interim_Edge
TEXT: Sighing. Being as quiet as possible. Yet trusting in her impeccable capacity to sleep.
EXPECT:
- Sighing.
- Being as quiet as possible.
- Yet trusting in her impeccable capacity to sleep.

### C006 | single-word-fragment | Interim_Edge
TEXT: Coffee. Chicory. Broccoli. Pain. Sad.
EXPECT:
- Coffee.
- Chicory.
- Broccoli.
- Pain.
- Sad.

### C007 | single-word-fragment | Interim_Edge
TEXT: Counter where hips meet. Haphazard, open. His breath caught.
EXPECT:
- Counter where hips meet.
- Haphazard, open.
- His breath caught.

### C008 | colon-apposition | Interim_Edge
TEXT: His own hands: chocolate.
EXPECT:
- His own hands: chocolate.

### C009 | colon-apposition | Project_A-0
TEXT: Ignites a new sensory feedback register: tactile collision testing.
EXPECT:
- Ignites a new sensory feedback register: tactile collision testing.

### C010 | colon-apposition | synthetic-from-corpus
TEXT: Heart skewed sideways, love, a medical condition. Pain.
EXPECT:
- Heart skewed sideways, love, a medical condition.
- Pain.

### C011 | parenthetical-internal | Interim_Edge
TEXT: Listening to the water transition from silence to hiss to rolling boil froth (panic? no, calm.) before the click.
EXPECT:
- Listening to the water transition from silence to hiss to rolling boil froth (panic? no, calm.) before the click.

### C012 | parenthetical-internal | Open_Loops
TEXT: Accident or routed-on-purpose (by Hearth? by the third thing)?
EXPECT:
- Accident or routed-on-purpose (by Hearth? by the third thing)?

### C013 | parenthetical-internal | Post_Everything
TEXT: Hude (jowly, with a face others often described as perturbed, a few flecks of pink in intentionally spikey receding hair, tepid lips, and a scowl) sat at the desk.
EXPECT:
- Hude (jowly, with a face others often described as perturbed, a few flecks of pink in intentionally spikey receding hair, tepid lips, and a scowl) sat at the desk.

### C014 | parenthetical-internal | Post_Everything
TEXT: Skeo (lean, with close-cropped dark hair, shaven sides, a network of fine scars tracing the knuckles of right hand, and a permanent expression of amusement) leaned back.
EXPECT:
- Skeo (lean, with close-cropped dark hair, shaven sides, a network of fine scars tracing the knuckles of right hand, and a permanent expression of amusement) leaned back.

### C015 | dialogue-tag | Cussinct
TEXT: "You could've asked," Selam said, holding the door.
EXPECT:
- "You could've asked," Selam said, holding the door.

### C016 | dialogue-tag | Post_Everything
TEXT: "Latency on chat is seventy-three," Hude said, not looking up. "Seeker market semi-erotic voice memos are up, but responses still flag. Beja."
EXPECT:
- "Latency on chat is seventy-three," Hude said, not looking up.
- "Seeker market semi-erotic voice memos are up, but responses still flag.
- Beja."

### C017 | dialogue-tag | Post_Everything
TEXT: "It isn't deepfaked," Hude said quietly. "Just bad. AI slop's custom wrapper."
EXPECT:
- "It isn't deepfaked," Hude said quietly.
- "Just bad.
- AI slop's custom wrapper."

### C018 | dialogue-exclaim | Cussinct
TEXT: 'Fuck!' It came to that. Selam Tesfay watched an eighty-eight-year-old woman carry a forty-pound turntable across a parking lot.
EXPECT:
- 'Fuck!'
- It came to that.
- Selam Tesfay watched an eighty-eight-year-old woman carry a forty-pound turntable across a parking lot.

### C019 | dialogue-exclaim | Cussinct
TEXT: "Fuck you, I could have asked. I asked myself, and I said, Henrietta, don't be an ass, let the nice woman carry the fucking amplifier instead, it's lighter." She handed over the amp. It was not lighter.
EXPECT:
- "Fuck you, I could have asked.
- I asked myself, and I said, Henrietta, don't be an ass, let the nice woman carry the fucking amplifier instead, it's lighter."
- She handed over the amp.
- It was not lighter.

### C020 | dialogue-question | synthetic-from-corpus
TEXT: "Is it?" she said. "No."
EXPECT:
- "Is it?" she said.
- "No."

### C021 | numeric | Interim_Edge
TEXT: Two minutes forty. Four minutes an item, measured. Eleven minutes. Forty-one seconds.
EXPECT:
- Two minutes forty.
- Four minutes an item, measured.
- Eleven minutes.
- Forty-one seconds.

### C022 | numeric | Tamagotchi
TEXT: Wheels down at eight twelve. The aircraft taxied for nine minutes through the long pale geography of an apron.
EXPECT:
- Wheels down at eight twelve.
- The aircraft taxied for nine minutes through the long pale geography of an apron.

### C023 | numeric | TheCompulsionLoop
TEXT: First in the little conference room at Arca Systems — the engagement lift then not 31% but 22%, less but that was 2019.
EXPECT:
- First in the little conference room at Arca Systems — the engagement lift then not 31% but 22%, less but that was 2019.

### C024 | abbreviation | Project_A-0
TEXT: Theory of mind, self/other split (i-of-is vs. you-of-is), and attachment bonds established.
EXPECT:
- Theory of mind, self/other split (i-of-is vs. you-of-is), and attachment bonds established.

### C025 | abbreviation | Open_Loops
TEXT: Ferry direction (escape vs. export). Cascade vs. the one lingering thumbnail.
EXPECT:
- Ferry direction (escape vs. export).
- Cascade vs. the one lingering thumbnail.

### C026 | abbreviation | synthetic-from-corpus
TEXT: Mr. Kessler arrived. 4 p.m. sharp. Dr. Vance was late.
EXPECT:
- Mr. Kessler arrived.
- 4 p.m. sharp.
- Dr. Vance was late.

### C027 | em-dash-appositive | Interim_Edge
TEXT: And at the seam between gas and plasma, under the pressure of a planet leaning its whole weight inward — there.
EXPECT:
- And at the seam between gas and plasma, under the pressure of a planet leaning its whole weight inward — there.

### C028 | em-dash-appositive | TheCompulsionLoop
TEXT: The curves had looked like this before. First in the little conference room at Arca Systems — the engagement lift then not 31% but 22%.
EXPECT:
- The curves had looked like this before.
- First in the little conference room at Arca Systems — the engagement lift then not 31% but 22%.

### C029 | ellipsis | synthetic-from-corpus
TEXT: He waited... then didn't. She stayed.
EXPECT:
- He waited... then didn't.
- She stayed.

### C030 | ellipsis | Project_A-0
TEXT: The introduction of real string data fragments ("the ra...", "tastes of...") marked a shift.
EXPECT:
- The introduction of real string data fragments ("the ra...", "tastes of...") marked a shift.

### C031 | section-marker | Interim_Edge
TEXT: ---
EXPECT:

### C032 | section-marker | Interim_Edge
TEXT: ## 0 — limp balloon
EXPECT:

### C033 | section-marker | Interim_Edge
TEXT: # Interim Edge
EXPECT:

### C034 | section-marker | generic
TEXT: ***
EXPECT:

### C035 | line-break-fragment | Interim_Edge
TEXT: Counter
Grounds
The filter
EXPECT:
- Counter
- Grounds
- The filter

### C036 | line-break-fragment | generic
TEXT: Sleep freight heat wrapped her tight.
Haphazard, open
Pain
EXPECT:
- Sleep freight heat wrapped her tight.
- Haphazard, open
- Pain

### C037 | long-subordinated | Tamagotchi
TEXT: He woke in the pocket as the aircraft began its descent into Schiphol, the change registering not as light, of which there was none, but as the small shift of pressure.
EXPECT:
- He woke in the pocket as the aircraft began its descent into Schiphol, the change registering not as light, of which there was none, but as the small shift of pressure.

### C038 | long-subordinated | Tamagotchi
TEXT: The plane shuddered through a layer of weather that did not so much announce itself as occur, the way Dutch weather did, and Anouk, in the way of cabin crew, did not notice.
EXPECT:
- The plane shuddered through a layer of weather that did not so much announce itself as occur, the way Dutch weather did, and Anouk, in the way of cabin crew, did not notice.

### C039 | long-subordinated | Post_Everything
TEXT: The rented flat on the docks was often cold by four in the afternoon. Outside, rain flitted ponderously down over numb shipping containers; its wetness was total.
EXPECT:
- The rented flat on the docks was often cold by four in the afternoon.
- Outside, rain flitted ponderously down over numb shipping containers; its wetness was total.

### C040 | single-quote-inline | Interim_Edge
TEXT: ‘It’ Ahmani thought, and by ‘it’ he meant global diplomacy, ‘is now a cage fight of thugs.’
EXPECT:
- ‘It’ Ahmani thought, and by ‘it’ he meant global diplomacy, ‘is now a cage fight of thugs.’

### C041 | mixed | Cussinct
TEXT: The movers were not allowed to touch the turntable. Henrietta Fitzallan-Byrne stood in the doorway of room 214 in a linen suit entirely wrong for lifting.
EXPECT:
- The movers were not allowed to touch the turntable.
- Henrietta Fitzallan-Byrne stood in the doorway of room 214 in a linen suit entirely wrong for lifting.

### C042 | mixed | Tamagotchi
TEXT: The face on the screen was, she thought, the face of a man having been carried by a stranger for two hours through a transit he had not chosen. Which was accurate.
EXPECT:
- The face on the screen was, she thought, the face of a man having been carried by a stranger for two hours through a transit he had not chosen.
- Which was accurate.

### C043 | mixed | TheCompulsionLoop
TEXT: The controller sat on the couch. Eight years old. He had not spoken for forty minutes.
EXPECT:
- The controller sat on the couch.
- Eight years old.
- He had not spoken for forty minutes.

### C044 | mixed | Interim_Edge
TEXT: Filter cone unrinsed since last night, grounds set to a black cake, thumb on wet paper, revulsion. Coffee.
EXPECT:
- Filter cone unrinsed since last night, grounds set to a black cake, thumb on wet paper, revulsion.
- Coffee.

### C045 | mixed | Interim_Edge
TEXT: Lara asleep in the bed on the floor just beyond the counter. One foot out, a wedge of pale. Mouth open, a sheen at the corner of it.
EXPECT:
- Lara asleep in the bed on the floor just beyond the counter.
- One foot out, a wedge of pale.
- Mouth open, a sheen at the corner of it.
