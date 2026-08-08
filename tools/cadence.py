#!/usr/bin/env python3
"""Step 2 — the six-dimension cadence vector.

d1, d2 are sequence statistics and need a document. d3-d6 are rates and can be
computed on any span. All are regex or tokenizer only: no model call.
"""
import re, statistics, sys, os

sys.path.insert(0, os.path.dirname(__file__))
from segment import segment

VERSION = "1.0.0"

# Revised 2026-08-06 after the Step 2 test. The original six were all rates per
# 1,000 words, but the text shortens ~20% under edit, which inflates every rate by
# ~25% mechanically. Counting instead of rating changed one result's sign and
# strengthened three others. The two sequence dimensions were also confounded:
# d2's raw adjacent jump looked strong (t=-3.28, 93%) but collapses to null when
# normalised by mean sentence length (t=-1.10, 53%). What actually moves is mean
# sentence length itself.
# d7 added 2026-08-06. Lexical rarity is the strongest measure found: t = -18.60
# across pairs, -9.07 under strict one-for-one substitution control, versus -5.72 for
# the best of the original six. It raises explained coverage from 9% to 54%.
# See plans/2026-08-06_lexical-temperature.md
DIMS = ["d1_mean_sent_len", "d2_len_cv", "d3_figuration", "d4_tricolon",
        "d5_naming", "d6_emdash", "d7_lexical_rarity"]
DOC_ONLY = {"d1_mean_sent_len", "d2_len_cv"}
COUNT_DIMS = {"d3_figuration", "d4_tricolon", "d5_naming", "d6_emdash"}

_FIG = re.compile(r'\bthe way (?:you|a|an|one)\b|\blike a\b|\bas if\b|\bas though\b', re.I)
_TRI = re.compile(r'\b[\w\'-]+,\s+[\w\'-]+,\s+(?:and\s+)?[\w\'-]+\b')
_NAME = re.compile(r',\s*which\s+(?:is|was|are|were)\b|\band this was\b|'
                   r'\ba kind of\b|,\s*which is only\b', re.I)
_EM = re.compile(r'—')
_WORD = re.compile(r"[a-zA-Z][a-zA-Z'-]*")

try:
    from wordfreq import zipf_frequency as _zipf
except ImportError:            # rarity is skipped rather than faked
    _zipf = None


def mean_zipf(text):
    """Mean Zipf frequency of the words in `text`. None if wordfreq is absent.

    Zipf 7 is `the`, 4 ordinary, 2 rare, 0 absent from the list. Lower means rarer,
    so a NEGATIVE displacement is a move toward rarer vocabulary.
    """
    if _zipf is None:
        return None
    ws = _WORD.findall(text.lower())
    if not ws:
        return None
    return round(sum(_zipf(w, "en") for w in ws) / len(ws), 4)


def _rate(pat, text, words):
    return round(1000 * len(pat.findall(text)) / words, 3) if words else 0.0


def vector(text, doc_level=True):
    """Six dims. d3-d6 are COUNTS, not rates — see the note on DIMS.

    Per-1,000-word rates are also returned, suffixed `_rate`, for reporting only.
    Never difference the rates: the text shortens under edit and the rates move
    with it.
    """
    words = len(text.split())
    v = {
        "d3_figuration": float(len(_FIG.findall(text))),
        "d4_tricolon": float(len(_TRI.findall(text))),
        "d5_naming": float(len(_NAME.findall(text))),
        "d6_emdash": float(len(_EM.findall(text))),
        "d3_figuration_rate": _rate(_FIG, text, words),
        "d4_tricolon_rate": _rate(_TRI, text, words),
        "d5_naming_rate": _rate(_NAME, text, words),
        "d6_emdash_rate": _rate(_EM, text, words),
    }
    if doc_level:
        lens = [len(s.split()) for s in segment(text)]
        if len(lens) >= 3:
            m = statistics.mean(lens)
            v["d1_mean_sent_len"] = round(m, 3)
            v["d2_len_cv"] = round(statistics.pstdev(lens) / m, 4) if m else 0.0
        else:
            v["d1_mean_sent_len"] = None
            v["d2_len_cv"] = None
    else:
        v["d1_mean_sent_len"] = None
        v["d2_len_cv"] = None
    v["d7_lexical_rarity"] = mean_zipf(text)
    v["_words"] = words
    v["_sentences"] = len(segment(text)) if doc_level else 1
    return v


def displacement(before, after, doc_level=True):
    a, b = vector(before, doc_level), vector(after, doc_level)
    d = {}
    for k in DIMS:
        if a.get(k) is None or b.get(k) is None:
            d[k] = None
        else:
            d[k] = round(b[k] - a[k], 4)
    d["_dwords"] = b["_words"] - a["_words"]
    return d, a, b
