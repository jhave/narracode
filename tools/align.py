#!/usr/bin/env python3
"""Substep 1.4 — alignment and operation typing.

Given two versions of the same draft, produce aligned span pairs labelled with
the operation the edit performed. Used by both extract_pairs.py (snapshots) and
extract_git_pairs.py (git history).

No model calls. Deterministic.
"""
import os, re, difflib

VERSION = "1.0.0"

SUB_THR = 0.40        # order-preserving sub-alignment floor
GATE = 0.30           # emitted-pair confidence gate
CONTENT_MATCH = 0.50  # draft-to-draft content match floor
REORDER = 0.85        # delete+insert collapse floor
SPLITJOIN = 0.50      # 1->n / n->1 block similarity floor


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def ratio(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


# ---------------------------------------------------------------- draft pairing

def match_drafts(a_path, a_files, b_path, b_files, read):
    """Filename first, then content similarity. Never filename similarity.

    Cussinct saves its human edit as 1-cussinct-human-edit-snapshot.md, so exact
    matching alone drops the machine->human transition, the most valuable pair in
    that story.
    """
    A, B = set(a_files), set(b_files)
    pairs = [(f, f, 1.0, "name") for f in sorted(A & B)]
    ra, rb = sorted(A - B), sorted(B - A)
    unmatched = []
    if ra and rb:
        cands = []
        for fa in ra:
            for fb in rb:
                r = difflib.SequenceMatcher(
                    None, read(os.path.join(a_path, "drafts", fa))[:20000],
                    read(os.path.join(b_path, "drafts", fb))[:20000],
                    autojunk=False).quick_ratio()
                cands.append((r, fa, fb))
        cands.sort(reverse=True)
        ua, ub = set(), set()
        for r, fa, fb in cands:
            if r < CONTENT_MATCH or fa in ua or fb in ub:
                continue
            ua.add(fa); ub.add(fb)
            pairs.append((fa, fb, round(r, 2), "content"))
        unmatched = [f for f in ra if f not in ua] + [f for f in rb if f not in ub]
    else:
        unmatched = ra + rb
    return pairs, unmatched


# ------------------------------------------------------------- sub-alignment

def mono(A, B):
    """Order-preserving sub-alignment.

    Accept a candidate only if it neither reuses an index nor crosses an already
    accepted pair. Greedy similarity without the crossing constraint manufactures
    pairs — it matched 'Counter.' to 'Coffee.' on the Interim Edge passage.
    """
    cands = []
    for i, x in enumerate(A):
        for j, y in enumerate(B):
            r = ratio(x, y)
            if r >= SUB_THR:
                cands.append((r, i, j))
    cands.sort(reverse=True)
    acc = []
    for r, i, j in cands:
        if any(i == pi or j == pj or (i - pi) * (j - pj) < 0 for _, pi, pj in acc):
            continue
        acc.append((r, i, j))
    ua = {i for _, i, _ in acc}
    ub = {j for _, _, j in acc}
    out = [(A[i], B[j], r, i) for r, i, j in sorted(acc, key=lambda t: t[1])]
    out += [(A[i], "", 0.0, i) for i in range(len(A)) if i not in ua]
    out += [("", B[j], 0.0, -1) for j in range(len(B)) if j not in ub]
    return out


def op_of(before, after, forced=None):
    if forced:
        return forced
    if not after:
        return "delete"
    if not before:
        return "insert"
    lb, la = len(before.split()), len(after.split())
    if la <= lb * 0.85:
        return "shorten"
    if la >= lb * 1.15:
        return "lengthen"
    return "substitute"


def align(before_text, after_text, segment, substitutions_only=False):
    """Return (pairs, stats). Each pair: dict(before, after, op, confidence, index)."""
    A, B = segment(before_text), segment(after_text)
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    pairs, gated, accounted = [], 0, 0

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            accounted += i2 - i1
            continue
        AA, BB = A[i1:i2], B[j1:j2]
        accounted += len(AA)

        # block-level split / join before sub-aligning
        if len(AA) == 1 and len(BB) > 1 and ratio(AA[0], " ".join(BB)) >= SPLITJOIN:
            cand = [(AA[0], " ".join(BB), "split", i1)]
        elif len(BB) == 1 and len(AA) > 1 and ratio(" ".join(AA), BB[0]) >= SPLITJOIN:
            cand = [(" ".join(AA), BB[0], "join", i1)]
        else:
            cand = [(b, a, None, i1 + max(idx, 0)) for b, a, r, idx in mono(AA, BB)]

        for b, a, forced, idx in cand:
            if norm(b) == norm(a):                    # no-signal filter
                continue
            if substitutions_only and (not b or not a):
                continue
            conf = round(ratio(b, a), 2) if (b and a) else 0.0
            if b and a and conf < GATE:
                gated += 1
                continue
            pairs.append({"before": b, "after": a,
                          "op": op_of(b, a, forced), "confidence": conf, "index": idx})

    pairs = collapse_reorders(pairs)
    return pairs, {"sent_before": len(A), "sent_after": len(B),
                   "accounted": accounted, "gated": gated}


def collapse_reorders(pairs):
    """A delete whose text reappears as an insert is a move, not two edits."""
    dels = [p for p in pairs if p["op"] == "delete"]
    ins = [p for p in pairs if p["op"] == "insert"]
    used_d, used_i, merged = set(), set(), []
    for d in dels:
        if id(d) in used_d:
            continue
        for s in ins:
            if id(s) in used_i:
                continue
            if ratio(d["before"], s["after"]) >= REORDER:
                merged.append({"before": d["before"], "after": s["after"],
                               "op": "reorder", "confidence": round(ratio(d["before"], s["after"]), 2),
                               "index": d["index"]})
                used_d.add(id(d)); used_i.add(id(s))
                break
    keep = [p for p in pairs if id(p) not in used_d and id(p) not in used_i]
    return keep + merged
