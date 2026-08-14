---
status: Experiment 1 run on three stories, two of them blind
probes: plans/exp1-vetch-probes.md, plans/exp1-alpha-gaia-probes.md (both committed before drafts were opened)
---

# Experiment 1 — three stories, three shapes

*2026-08-14. Claude Opus 5.*

---

## 0. What was run

| Story | Branch | Sections | Obligations | Probes |
|---|---|---|---|---|
| Interim Edge | `main` | 7 | 13 | sighted — written after reading the scene ledger |
| **Vetch** *(Spiral Brief)* | `claude/narracode-spiral-brief-r7oz1y` | 8 | 11 | **blind**, pre-registered at `10f8b48` |
| **Alpha-Gaia** *(Garaiv)* | `claude/alpha-gaia-story` | 7 | 12 | **blind**, pre-registered at `a6fe4d0` |

The two blind probe sets were written from each story's `obligations.md` alone and committed
before any draft was opened. Neither was revised afterwards. Where a probe turned out badly
chosen it is reported as a miss, not corrected.

Both stories were snapshotted before annotation. Nothing on either story branch was modified —
the analysis ran against a read-only extract, and the annotated `obligations.md` for each is
available to drop onto its branch when jhave wants it.

A correction to my previous report: I said Garaiv and Spiral Brief were absent after checking
"all branches." The clone only had `main` and my own branch fetched, so `git log --all` was
searching a truncated ref set. Both stories were there. Eleven branches now fetched.

---

## 1. Three stories, three curve shapes

| | Interim Edge | Vetch | Alpha-Gaia |
|---|---|---|---|
| start → end | 3.00 → **12.22** | 2.00 → **7.47** | 4.00 → **9.40** |
| peak | final section | §VII (8.79) | §3 (9.45) |
| shape | monotone, never falls | rise, then **release** | rise, dip at §4–5, recover |
| final section touches | **11 of 13** | **1 of 11** | 5 of 12 |
| fade events | 0 | 0 | 0 |

**This is the result the experiment needed.** Three finished pieces produce three distinguishable
shapes, and the differences correspond to things a reader could name.

**Interim Edge accumulates and never lets go.** Monotone to the last section, which then
re-touches eleven of thirteen threads on the way out. Its `obligations.md` says *"Resolved:
(none — resolution refused as formal principle)"* and nine entries are marked *(Never answer.)*
The ledger reproduced the declared poetics from arithmetic alone.

**Vetch releases.** It climbs to 8.79 through *VII. Testimony* — the movement where the inserted
scene resolves Salome's thread — and then *VIII. Flatness* touches exactly **one** obligation
and lets the rest decay. It is the only final section in the three that stops holding. The
movement is titled *Flatness* and the curve goes flat. That is the closest thing to a
validation of the metric in this whole run: an independently chosen title and an independently
computed number agreeing about what the section does.

**Alpha-Gaia breathes.** The only curve with a genuine interior decline — peak at §3
(*transposition*), falling through §4 (*the announcement*) and §5 (*the objection*), recovering
at §6 (*ineligible*). Feed-structured fiction with a park frame, and the dip lands exactly
where the feed items crowd the frame out. §4 and §5 are the two sections with no park return
at all (below, §3).

**Zero fade events across all three stories and 36 obligations.** Discussed in §4 — it is a
calibration finding, not a fact about the fiction.

---

## 2. What the ledger caught in Alpha-Gaia

Three findings, each checkable, each invisible before the count.

**The greyed field was never planted.** It is the *first* entry in `obligations.md` —
*"Garaiv opens the customization profile and one field will not take input. Planted early,
never explained."* In `drafts/5-alpha-gaia-linked.md`: `greyed` 0 occurrences, `gray` 0,
`will not take` 0, `customization` 0. The five hits on `field` are `ballfield`. The obligation
carries the only explicit **ceiling** in any of the three stories — *"must not be returned to
more than twice"* — and it is satisfied vacuously, by never appearing.

I am reporting this as absence rather than probe failure because four independent probes
including the obligation's own two distinguishing phrases all returned zero. That is a
different evidentiary situation from Vetch's *figure* (§3).

**The ID-V2V thread does not carry the ending.** `obligations.md` flags it as *"the newest and
the most likely to be left as decoration. It has to carry the ending."* It appears in **§3
only** — one section out of seven, and not the last. Checked against `vehicle`, `identit`, and
`ID` in case it is carried under another name: none appear in §6. §6 resolves through the
antibody offer instead. The file named the risk; the count confirms it happened.

**The park vanishes exactly where the file predicted.** *"Under the weight of four feed items
the bench can vanish. Every feed section owes the park one return."* `park` fires in §0, 1, 3, 6;
`bench` in §0, 2, 3, 6. Union: everywhere except **§4 and §5** — the announcement and the
objection, the two most feed-dense sections. Which is precisely the mechanism the risk entry
describes.

Two of Alpha-Gaia's three self-declared risks are confirmed as having happened. The third
(Garaiv's skepticism staying funny) is not measurable this way and was declared unmeasurable
in advance.

---

## 3. Where the blind probes failed, and what that taught

**Vetch's *figure* never fired — and it is a probe miss, not an absence.** The obligation is
*"The figure must appear without being explained."* The word `figure` appears **0 times** in
the drafts; `shape` appears 12. The story almost certainly renders it under another noun. My
pre-registration predicted this exact failure (weakness #2: *"depends on the story literally
using the phrase"*), which is why the prediction was worth writing down.

**Vetch's *Ines's pressing problem* fired in all eight movements — worthless.** The obligation
offers three alternatives (*debt/eviction/sick parent*) and I probed all of them blind. `owed`
and `owes` are ordinary English. Noise, as predicted in weakness #1.

**Vetch's bare character names over-report, as predicted.** `Kwesi` [3,4,5,7], `Marit` [4,6,7],
`Salome` [3,4,5,7] measure presence, not whether the obligation was pressed.

### The finding underneath the failures

Compare the two blind sets. Alpha-Gaia's probes mostly worked; Vetch's mostly did not. The
difference is not the stories. It is **how each `obligations.md` was written**.

| Alpha-Gaia writes | Vetch writes |
|---|---|
| "**The dragonfly.** Lands, stays too long." | "The figure must appear without being explained." |
| "**The mist.** Beads on the forearm and sits." | "Kwesi must be right at least twice." |
| "**The child at the pond.** Looks twice." | "Marit must be sympathetic and correct about risk." |

Alpha-Gaia names **objects with a lexical surface**. Vetch names **requirements about the
craft**. Both are legitimate things to track, but only the first is a thing the story puts on
the page in words, and only the first can be counted.

Predictions #1 and #3 from the Alpha-Gaia pre-registration both held — the dragonfly plants at
§2 and returns once at §6, the pond looks exactly twice (§0, §2) — because those obligations
name objects. Nothing in the Vetch set could be checked at all.

**This is a harness change, not a tooling change.** An obligation is a promise the *reader* is
holding, and a reader holds objects, images, and questions — not craft requirements. "Kwesi
must be right at least twice" is a note to the writer. "The dragonfly, owed a small return"
is an obligation. Now stated in `narracode.md → Obligation salience`.

---

## 4. Zero fades in 36 obligations — the calibration finding

Not one obligation in any of the three stories crossed the 0.1 floor. That is not three
stories all refusing to release; it is arithmetic. At `half-life: 3`, an untouched obligation
needs **ten consecutive untouched scenes** to fade. These pieces are seven and eight sections
long. The floor is unreachable by construction.

Two consequences:

1. **Half-lives were set for novels and applied to short fiction.** At this length the useful
   half-lives are probably 1–2, not 3–6. The values in these three files are my guesses and
   should be treated as a first calibration, not a result.
2. **`## Faded` may be a novel-length concept.** In a 7-section piece the reader plausibly
   holds everything to the end, and the meaningful signal is not *what faded* but *what the
   final section chose to touch* — where Interim Edge (11/13) and Vetch (1/11) differ
   completely. The instrument's most discriminative output turned out to be the one I added
   almost incidentally.

---

## 5. Status against the falsification condition

The Experiment 1 condition was: *if the curves do not separate the pieces jhave rates highly
from the ones he does not, the physics has no purchase and the track stops.*

**Not yet answerable, and it needs jhave.** What is established is the weaker but necessary
precondition: **the curves separate the stories from each other**, along axes that correspond
to describable narrative behaviour (accumulate-and-hold, rise-and-release, rise-dip-recover),
and in one case (Vetch VIII) the number agrees with a title chosen independently of it.

What is needed now is his ranking. Three curves and three rankings is still a small n, but it
is the first point at which the question can be asked at all.

Also worth noting against §2.6 of the ensemble critique: every finding here is a *negative*
one — a thread that vanished, an obligation never planted, a park that dropped out. None of
them suggests a target to optimise. The ledger has so far been useful exactly in the way it
was supposed to be, and useless as a controller. That is the intended result.
