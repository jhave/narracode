# Narracode — FAQ

A short guide to using the harness. If you read nothing else, read "Start here."

---

## Start here

1. Put `narracode_Aug-9-2026.md` in a folder on your computer.
2. Open that folder with an agentic AI assistant — Claude Code, Cursor, Gemini CLI, Antigravity, or anything else that can read and write files.
3. Type:

   > Consult narracode.md and initiate a new project about [your premise].

That is the whole installation. The file unfolds into the system.

---

## What is it?

One markdown file that turns a general-purpose AI assistant into a literary composition system. It does this by refusing to let the model do everything at once. Instead of a single prompt producing a single answer, the work is split into separate passes — planning, reading, structuring, drafting, critiquing — each writing its state to files on disk.

The premise: a model's ability to *recognise* good prose exceeds its ability to *produce* it in one shot. Separating the critical pass from the generative pass lets the first govern the second.

## Why not just prompt the model directly?

Single-shot prompting averages the training distribution. You get competent, fluent, slightly sentimental prose that reads like a thousand other models writing about the same thing. The harness exists to interrupt that default.

## What do I need?

- An agentic AI assistant with file read/write access to a folder.
- A premise, a seed paragraph, or a stylistic constraint. Any of the three is enough to start.

No installation, no dependencies, no API keys beyond whatever your assistant already uses.

## Which model should I use?

Any frontier model works. The stories on this site were composed with Claude (Opus 4.6–5, Sonnet 4.6, Fable 5), Gemini (3.1 Pro–3.6 Flash), and GPT-5.5. Stronger models produce better critique passes, which matters more than raw generative fluency.

---

## Talking to it

You do not memorise commands. Say what you want in plain language; the harness maps it to the right pass.

| You say | What happens |
|---|---|
| "Start a new project about…" | Initiator — creates the folder, `POETICS.md`, `ATTRIBUTION.md`, structural memory |
| "Keep going" / "Write the next scene" | Compositional — drafts prose, then stops |
| "How does this sound?" / "Are we losing the style?" | Reflexive — critiques the draft against your poetics |
| "Does this hold together?" | Reflexive, check mode — continuity, obligations, motifs |
| "What could happen next?" | Suggests directions from the structural state, without drafting |
| "Save this" / "Lock it in" | Snapshots the project and learns from your edits |
| "Read [writer or work]" | Annotates a reference or upload for its attentional dialect |
| "Auto" / "Run auto through 5 acts" | AUTO_MODE — full pipeline, no confirmation pauses |

**One pass at a time.** The harness will not chain into the next pass on its own. That silence is deliberate — you decide what comes next.

---

## What ends up in the folder?

```
DD-MM-YYYY_TITLE/
  POETICS.md               your commitments, refusals, dialect
  ATTRIBUTION.md           who wrote what, human and model
  drafts/                  numbered draft files
  structural/              the story's working memory (8 files)
  critiques/               created when you first ask for feedback
  versions/                created at the first snapshot
```

The `structural/` folder is the part that matters. It holds `graph.md` (who relates to whom), `time-constants.md` (chronology and durations), `history.md` (what is now true), `obligations.md` (what the reader is waiting for), `motifs.md` (recurring images and their transformations), `scene-ledger.md` (what each scene does), `character-interiority.md` (private states and contradictions), and `reader-state.md` (what a first-time reader expects). These are read before every draft, so the story accumulates pressure instead of resetting.

## Can I edit the drafts myself?

Yes — and you should. This is the Seamless Edit method, and it is the main way you teach the system your register.

Edit any draft directly in your editor. On the next snapshot, the harness diffs your version against what it generated, works out what your edits were doing (compressing, sharpening, cutting explanation, changing agency), logs the observations, and proposes updates to `POETICS.md` when a pattern recurs. It proposes; it does not rewrite your poetics unilaterally.

## What is AUTO_MODE?

A full-pipeline run with all confirmation pauses suspended: initiate, draft every act, check and tell-scan each one, then critique and drift-check the whole. Use it to generate a complete story unattended. Do not use it for iterative work where your judgment is part of the loop.

## What is a "tell"?

A signature of machine prose — the em-dash cadence, the triad, the closing summary that explains what the scene just did. The harness carries a registry of seventeen classes, each with a detector and a target rate anchored on human corpora rather than zero. A scan runs after each draft and writes its findings without applying them. You decide what to cut.

Note the recursion: any remedy becomes the next tell the moment it is adopted. The registry rate-caps its own fixes.

## I came back after a month and lost the thread.

Ask it to orient you. It reads the poetics, the last loop notes, the latest draft, the open obligations, and the most recent critique, then tells you where the project stands and what decision you left unresolved. It will not generate until you say so.

## Does it work for anything other than fiction?

The structural vocabulary assumes narrative — scenes, obligations, characters, reader-state. Essays and criticism can use the pass separation and the edit-learning loop, but most of the memory files will sit idle.

## Will it argue with me?

No. If you have chosen references whose virtue is the breaking of legibility, it follows you into the breakage. Coherence is not treated as an automatic literary virtue. The piece belongs to you.

---

## Licence and credit

Narracode is by David Jhave Johnston (Jhave), released under CC BY-NC-SA 4.0. Every project it creates writes its own `ATTRIBUTION.md` naming the human author, the models that performed each pass, and the date. Keep it accurate — it is the point.

Source, issues, and the full story corpus: <https://github.com/jhave/narracode>
