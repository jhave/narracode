#!/usr/bin/env python3
"""Substep 1.3 — sentence segmentation for Narracode literary prose.

Hand-written because the prose is deliberately full of fragments, subject-dropped
verb chains and unconventional punctuation, which trained tokenizers smooth away.
See corpus/segmenter_eval.md for the comparison that decided this.

No dependencies, no network, no model call. Deterministic.
"""
import re

VERSION = "1.0.0"

# Terminators that do not end a sentence.
ABBREV = {
    "mr", "mrs", "ms", "dr", "prof", "st", "sr", "jr", "vs", "etc", "eg", "ie",
    "cf", "al", "no", "fig", "vol", "ch", "pp", "approx", "dept", "est",
    "a.m", "p.m", "am", "pm", "u.s", "u.k",
}

_HEADING = re.compile(r'^\s{0,3}#{1,6}\s')
_RULE = re.compile(r'^\s*([-*_=]\s*){3,}$')
_FIGLABEL = re.compile(r'^\s*\*{0,2}(fig|figure|table|plate)\s*[\d.]+\**\s*[—-]', re.I)
_YAML = re.compile(r'\A---\n.*?\n---\n', re.S)
_LISTMARK = re.compile(r'^\s*([-*+]|\d+[.)])\s+')

# Terminal punctuation, optionally followed by closing quotes/brackets.
_CLOSERS = '"\'’”′″)]}'
_TERM = re.compile(r'[.!?…]+[' + re.escape(_CLOSERS) + r']*')

_OPEN_TO_CLOSE = {'(': ')', '[': ']', '{': '}'}


def _depth_map(s):
    """Bracket depth before each character; punctuation inside brackets never splits."""
    out, d = [], 0
    for ch in s:
        out.append(d)
        if ch in _OPEN_TO_CLOSE:
            d += 1
        elif ch in ')]}' and d > 0:
            d -= 1
    return out


def _is_abbrev(text, end):
    """True if the '.' at end-1 closes a known abbreviation."""
    if end - 1 < 0 or text[end - 1] != '.':
        return False
    m = re.search(r'([A-Za-z][A-Za-z.]*)\.$', text[:end])
    if not m:
        return False
    w = m.group(1).lower().rstrip('.')
    if w in ABBREV:
        return True
    # Single initial, e.g. "J. Smith" — but only when the letter genuinely stands
    # alone. Without this guard a contraction ending in one letter ("didn't.",
    # "won't.", "isn't.") looks like an initial and the sentence never terminates,
    # silently merging it with the next one.
    if len(w) == 1 and w.isalpha():
        before = text[:m.start(1)]
        # A straight apostrophe must NOT count as an opening delimiter here: it is
        # also the contraction apostrophe, so allowing it makes "didn't." parse as
        # the initial "t." and the sentence never terminates.
        return before == "" or before[-1] in " \t([\"‘“"
    return False


def _split_line(line):
    """Split one physical line into sentences."""
    depth = _depth_map(line)
    out, start = [], 0
    for m in _TERM.finditer(line):
        i, j = m.start(), m.end()
        if depth[i] > 0:                       # inside brackets
            continue
        if _is_abbrev(line, i + 1):
            continue
        # An ellipsis mid-line does not terminate unless the next word is capitalised.
        if m.group().startswith('…') or line[i:j].startswith('...'):
            rest = line[j:].lstrip()
            if rest and not rest[0].isupper():
                continue
        rest = line[j:].lstrip()
        # A closing quote followed by a lowercase dialogue tag keeps the sentence open:
        #   "You could've asked," Selam said.   -> handled by comma, not here
        #   "Is it?" she said.                  -> do not split before "she said"
        if line[j - 1] in _CLOSERS and rest and rest[0].islower():
            continue
        seg = line[start:j].strip()
        if seg:
            out.append(seg)
        start = j
    tail = line[start:].strip()
    if tail:
        out.append(tail)
    return out


def segment(text):
    """Split prose into sentences.

    Decisions fixed 2026-08-06. Changing any of these invalidates every stored
    cadence vector, so treat this list as a contract:

      - a dialogue tag attaches to the sentence it reports:
        '"You could\'ve asked," Selam said.' -> 1 sentence
      - a closing quote ending a complete utterance terminates:
        "'Fuck!' It came to that." -> 2 sentences
      - punctuation inside (), [] or {} never splits
      - a line break terminates when the line has no terminal punctuation
      - markdown headings, horizontal rules, figure labels and YAML front
        matter yield no sentences
      - listed abbreviations and single initials do not terminate
      - '...' mid-line terminates only when followed by a capital
    """
    text = _YAML.sub('', text)
    out = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if _HEADING.match(line) or _RULE.match(line) or _FIGLABEL.match(line):
            continue
        line = _LISTMARK.sub('', line)
        if not line.strip():
            continue
        out.extend(_split_line(line))
    return out


if __name__ == "__main__":
    import sys
    for s in segment(open(sys.argv[1], encoding="utf-8").read()):
        print(repr(s))
