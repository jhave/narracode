#!/usr/bin/env python3
"""Merge snapshot- and git-derived pairs into one corpus, deduplicated.

Key: (story, normalised before, normalised after). Snapshot-derived records win,
because their provenance rests on a jhave-confirmed snapshot label rather than a
commit-message convention.

Writes corpus/all_pairs.jsonl
"""
import json, re, os
from collections import Counter


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.exists(p) else []


def main():
    snap = load("corpus/edit_pairs.jsonl")
    git = load("corpus/git_pairs.jsonl")
    for r in snap:
        r.setdefault("source", "snapshot")
    for r in git:
        r.setdefault("pair_type", "immediate")

    out, seen, dup = [], set(), 0
    for r in snap + git:                       # snapshot first: it wins ties
        k = (r["story"], norm(r["before"]), norm(r["after"]))
        if k in seen:
            dup += 1
            continue
        seen.add(k)
        out.append(r)

    out.sort(key=lambda r: (r["story"], r["draft"], r["index"], r["id"]))
    tmp = "corpus/all_pairs.jsonl.tmp"
    with open(tmp, "w") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, "corpus/all_pairs.jsonl")

    print(f"snapshot {len(snap)}  git {len(git)}  duplicates dropped {dup}")
    print(f"TOTAL {len(out)} -> corpus/all_pairs.jsonl")
    print("by source:", dict(Counter(r["source"] for r in out)))
    print("by story:")
    for k, v in Counter(r["story"] for r in out).most_common():
        print(f"   {k:44} {v}")


if __name__ == "__main__":
    main()
