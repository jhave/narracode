#!/usr/bin/env python3
"""
tillman_check.py — a prosody validator for the flat-declarative register.

Built for the project `Chauffé Éclairé` (23-08-2026). The register it enforces is
described in that project's POETICS.md and reference/voice-engine.md: short flat
declaratives, figuration near zero, no clause allowed to run long unless it breaks
on a semicolon.

The point is that the voice is a set of measurable properties, not an adjective.
This tool measures them. It does not rewrite.

Usage:
    python3 tools/tillman_check.py path/to/draft.md
    python3 tools/tillman_check.py path/to/draft.md --verbose   # list every offender
"""

import re
import sys
import statistics
from pathlib import Path

# ---------------------------------------------------------------- targets

TARGETS = {
    "median_max": 7,
    "pct_le8_min": 65.0,
    "pct_gt14_max": 8.0,
    "long_sentence_words": 12,      # above this a sentence must break on ';'
    "post_semicolon_max": 10,
    "figures_per_1000_max": 2.0,
    "para_sentences_max": 9,
    "emdash_per_1000_max": 1.5,
}

# ---------------------------------------------------------------- patterns

FIGURE_PATTERNS = [
    (r"\blike a\b", "simile: like a"),
    (r"\blike the\b", "simile: like the"),
    (r"\bas if\b", "simile: as if"),
    (r"\bas though\b", "simile: as though"),
    (r"\bthe way (?:you|a|an|one)\b", "analogy: the way you/a  [tells §11]"),
    (r"\bresembl", "figure: resembled"),
    (r"\breminded (?:me|her|him) of\b", "figure: reminded me of"),
    (r"\bsomething (?:like|of)\b", "hedged figure"),
    (r"\b(?:said|says|smell(?:ed|s)|tast(?:ed|es)|look(?:ed|s)|felt|feels|sound(?:ed|s)|move[ds]?) (?:it |them |her |him )?like\b", "simile: bare verb+like"),
]

TELL_PATTERNS = [
    (r"\bwhich (?:is|was) only\b", "tells §5: reductive 'which is only X'"),
    (r"\beveryone (?:assumes|thinks|believes)\b", "tells §6: corrective superiority"),
    (r"\bwhat people get wrong\b", "tells §6: corrective superiority"),
    (r"\bthe weight of it\b", "tells §1: overused object lexicon"),
    (r"\bthe air itself\b", "tells §1: overused object lexicon"),
    (r"\bshimmer", "tells §1: overused object lexicon"),
    (r"\btapestry\b", "tells §1: overused object lexicon"),
    (r"\btestament\b", "tells §1: overused object lexicon"),
    (r"\bhum(?:med|ming)?\b", "tells §1: overused object lexicon"),
    (r"\bkettle\b", "tells §1: overused object lexicon"),
]

DIET = ["thing", "things", "spent", "wage", "held", "holding", "bent", "small"]

ABSTRACTIONS = [
    "loneliness", "desire", "emptiness", "existence", "longing", "yearning",
    "sadness", "despair", "intimacy", "vulnerability", "connection", "trauma",
    "healing", "identity", "belonging", "grief",
]

SPEECH = re.compile(r'[""\"]')

# ---------------------------------------------------------------- parsing

def strip_markup(text):
    text = re.sub(r"^#.*$", "", text, flags=re.M)          # headers
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)     # bullets
    text = re.sub(r"[*_`]", "", text)                       # emphasis
    text = re.sub(r"^\s*---\s*$", "", text, flags=re.M)     # rules
    return text

def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

def sentences(para):
    # split after . ! ? … when followed by space or end, keeping the terminator
    parts = re.split(r"(?<=[.!?…])\s+", para.strip())
    return [s.strip() for s in parts if s.strip()]

def wordcount(s):
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9'’\-]+", s))

# ---------------------------------------------------------------- analysis

def analyse(path, verbose=False):
    raw = Path(path).read_text(encoding="utf-8")
    text = strip_markup(raw)
    paras = paragraphs(text)

    sents, para_of, long_para = [], [], []
    for i, p in enumerate(paras):
        ss = sentences(p)
        if len(ss) > TARGETS["para_sentences_max"]:
            long_para.append((i + 1, len(ss), ss[0][:60]))
        for s in ss:
            sents.append(s)
            para_of.append(i + 1)

    if not sents:
        print("no sentences found")
        return 1

    lens = [wordcount(s) for s in sents]
    total_words = sum(lens)
    per_k = total_words / 1000.0 or 1.0

    median = statistics.median(lens)
    pct_le8 = 100.0 * sum(1 for n in lens if n <= 8) / len(lens)
    pct_gt14 = 100.0 * sum(1 for n in lens if n > 14) / len(lens)

    # long sentences that do not break on a semicolon and are not speech
    unbroken = [
        (para_of[i], n, s)
        for i, (n, s) in enumerate(zip(lens, sents))
        if n > TARGETS["long_sentence_words"] and ";" not in s and not SPEECH.search(s)
    ]

    # words after a semicolon
    tails = []
    for i, s in enumerate(sents):
        if ";" in s:
            tail = s.split(";", 1)[1]
            n = wordcount(tail)
            if n > TARGETS["post_semicolon_max"]:
                tails.append((para_of[i], n, tail.strip()[:70]))

    figures, tells = [], []
    for i, s in enumerate(sents):
        low = s.lower()
        for pat, label in FIGURE_PATTERNS:
            if re.search(pat, low):
                figures.append((para_of[i], label, s[:70]))
        for pat, label in TELL_PATTERNS:
            if re.search(pat, low):
                tells.append((para_of[i], label, s[:70]))

    low_all = text.lower()
    diet = {w: len(re.findall(rf"\b{w}\b", low_all)) for w in DIET}
    diet = {w: c for w, c in diet.items() if c}
    abstr = {w: len(re.findall(rf"\b{w}\b", low_all)) for w in ABSTRACTIONS}
    abstr = {w: c for w, c in abstr.items() if c}

    emdash = low_all.count("—")
    copula = len(re.findall(r"\b(?:is|was|were|are|been|being)\b", low_all))

    # ------------------------------------------------------------ report
    print(f"\n=== {Path(path).name} ===")
    print(f"words {total_words}   sentences {len(sents)}   paragraphs {len(paras)}")
    print(f"mean {statistics.mean(lens):.1f}   median {median:.0f}   max {max(lens)}")

    checks = []

    def check(ok, label, detail):
        checks.append(ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:34} {detail}")

    print("\n-- prosody")
    check(median <= TARGETS["median_max"], "median <= 7 words", f"{median:.0f}")
    check(pct_le8 >= TARGETS["pct_le8_min"], "sentences <= 8 words >= 65%", f"{pct_le8:.1f}%")
    check(pct_gt14 <= TARGETS["pct_gt14_max"], "sentences > 14 words <= 8%", f"{pct_gt14:.1f}%")
    check(not unbroken, "long sentences break on ';'", f"{len(unbroken)} unbroken")
    check(not tails, "words after ';' <= 10", f"{len(tails)} over")
    check(not long_para, "paragraphs <= 9 sentences", f"{len(long_para)} over")

    print("\n-- figuration")
    fr = len(figures) / per_k
    check(fr <= TARGETS["figures_per_1000_max"], "figures per 1,000 words <= 2", f"{fr:.2f} ({len(figures)} total)")
    er = emdash / per_k
    check(er <= TARGETS["emdash_per_1000_max"], "em-dashes per 1,000 <= 1.5", f"{er:.2f} ({emdash} total)")
    check(not tells, "no registry tells", f"{len(tells)} hits")

    print("\n-- lexicon (audit, not pass/fail)")
    print(f"  copula rate           {100.0*copula/total_words:.1f}% of words")
    print(f"  lexical diet          {diet or 'clean'}")
    print(f"  abstraction nouns     {abstr or 'clean'}")

    if verbose:
        if unbroken:
            print("\n-- long, unbroken")
            for p, n, s in unbroken:
                print(f"  ¶{p} ({n}w) {s}")
        if tails:
            print("\n-- long semicolon tails")
            for p, n, s in tails:
                print(f"  ¶{p} ({n}w) ;{s}")
        if figures:
            print("\n-- figures")
            for p, l, s in figures:
                print(f"  ¶{p} [{l}] {s}")
        if tells:
            print("\n-- tells")
            for p, l, s in tells:
                print(f"  ¶{p} [{l}] {s}")
        if long_para:
            print("\n-- long paragraphs")
            for p, n, s in long_para:
                print(f"  ¶{p} ({n} sentences) {s}")

        print("\n-- length histogram")
        for lo, hi in [(1, 3), (4, 5), (6, 8), (9, 11), (12, 14), (15, 99)]:
            n = sum(1 for x in lens if lo <= x <= hi)
            bar = "█" * int(60 * n / len(lens))
            print(f"  {lo:2}-{hi:<2} {n:4}  {bar}")

    failed = checks.count(False)
    print(f"\n{'ALL CHECKS PASS' if not failed else f'{failed} CHECK(S) FAILING'}\n")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(analyse(sys.argv[1], "--verbose" in sys.argv))
