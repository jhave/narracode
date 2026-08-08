#!/usr/bin/env python3
"""Step 2 — the falsification test.

Do jhave's edits push prose in a consistent direction in cadence space?

Runs at two levels, because 951 of 954 before-spans are a single sentence, so the
sequence dimensions d1 and d2 cannot be computed per pair:

  DOCUMENT level  every machine->human transition, whole draft before and after.
                  All six dimensions. Small n, and the only place d1/d2 exist.
  PAIR level      all corpus pairs. d3-d6 only. Large n.

Writes corpus/step2_displacement.md
"""
import json, os, re, sys, subprocess, statistics, math
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import yaml
from cadence import vector, displacement, DIMS, DOC_ONLY, VERSION as CAD_V
from align import match_drafts

ROOT = "Stories written with Narracode"


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def snapshots_for(survey, story):
    s = [r for r in survey["records"] if r["type"] == "snapshot" and r["story"] == story]
    s.sort(key=lambda r: (r["date"] or "", r["vnum"] if r["vnum"] is not None else 999))
    return s


def doc_transitions():
    """(story, label, before_text, after_text) for every machine->human transition."""
    L = yaml.safe_load(open("corpus/provenance.yaml"))
    survey = json.load(open("corpus/survey.json"))
    out = []
    for story, cfg in L["stories"].items():
        if cfg.get("usable") is False:
            continue
        prov = cfg.get("snapshots") or {}

        def p(e):
            d = (prov or {}).get(e) or {}
            return d.get("provenance", "unknown"), d.get("usable", True)

        seq = snapshots_for(survey, story)
        for a, b in zip(seq, seq[1:]):
            pa, ua = p(a["entry"]); pb, ub = p(b["entry"])
            if not (pa == "machine" and pb == "human" and ua and ub):
                continue
            pairs, _ = match_drafts(a["path"], a["drafts"], b["path"], b["drafts"], read)
            bt = "\n".join(read(os.path.join(a["path"], "drafts", fa)) for fa, _, _, _ in pairs)
            at = "\n".join(read(os.path.join(b["path"], "drafts", fb)) for _, fb, _, _ in pairs)
            if bt.strip() and at.strip() and bt != at:
                out.append((story, f"{a['entry']}->{b['entry']}", bt, at))

        for e in (cfg.get("human_commits") or cfg.get("git_commits") or []):
            sha = str(e["sha"])
            files = [f for f in sh(f'git diff-tree --no-commit-id --name-only -r {sha} '
                                   f'-- "*/drafts/*.md"').strip().split("\n") if f.strip()]
            bt = "\n".join(sh(f'git show {sha}~1:"{f}" 2>/dev/null') for f in files)
            at = "\n".join(sh(f'git show {sha}:"{f}"') for f in files)
            if bt.strip() and at.strip() and bt != at:
                out.append((story, f"git {sha}", bt, at))
    return out


def stats(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return None
    m = statistics.mean(vals)
    sd = statistics.pstdev(vals)
    agree = sum(1 for v in vals if (v > 0) == (m > 0) and v != 0)
    nz = sum(1 for v in vals if v != 0)
    # one-sample t against 0, normal approximation (no scipy available)
    t = m / (sd / math.sqrt(len(vals))) if sd else float('inf') if m else 0.0
    return {"n": len(vals), "mean": m, "sd": sd, "t": t,
            "consistency": agree / nz if nz else 0.0, "nonzero": nz}


def fmt(s, dim):
    if not s:
        return f"| {dim} | — | insufficient data |"
    star = "***" if abs(s["t"]) > 3 else "**" if abs(s["t"]) > 2 else ""
    return (f"| {dim} | {s['n']} | {s['mean']:+.4f} | {s['sd']:.4f} | "
            f"{s['t']:+.2f}{star} | {100*s['consistency']:.0f}% |")


def main():
    L = ["# Step 2 — displacement test", "",
         f"`tools/step2_displacement.py` · cadence {CAD_V}", "",
         "**The question:** do jhave's edits push prose in a consistent direction?", "",
         "If displacements scatter, there is no recurring correction to learn and "
         "Steps 3-5 should not be built.", "",
         "`t` is a one-sample t against zero (normal approximation; scipy is not "
         "available here). `**` marks |t|>2, `***` |t|>3. `consistency` is the share "
         "of non-zero displacements agreeing with the mean's sign.", ""]

    # ---------------- document level ----------------
    docs = doc_transitions()
    dd = defaultdict(list)
    rows = []
    for story, label, bt, at in docs:
        d, va, vb = displacement(bt, at, doc_level=True)
        for k in DIMS:
            dd[k].append(d[k])
        dd["_dwords"].append(d["_dwords"])
        rows.append((story, label, d))

    L += ["## Document level", "",
          f"{len(docs)} machine&rarr;human transitions, whole drafts. "
          "The only level where d1 and d2 exist.", "",
          "| dimension | n | mean Δ | sd | t | consistency |", "|---|---|---|---|---|---|"]
    doc_stats = {}
    for k in DIMS:
        s = stats(dd[k]); doc_stats[k] = s
        L.append(fmt(s, k))
    ws = stats(dd["_dwords"])
    L.append(fmt(ws, "word count"))
    L.append("")

    # ---------------- pair level ----------------
    pairs = [json.loads(l) for l in open("corpus/all_pairs.jsonl")]
    both = [p for p in pairs if p["before"].strip() and p["after"].strip()]
    pd = defaultdict(list)
    for p in both:
        d, _, _ = displacement(p["before"], p["after"], doc_level=False)
        for k in DIMS:
            if k not in DOC_ONLY:
                pd[k].append(d[k])
        pd["_dwords"].append(d["_dwords"])

    L += ["## Pair level", "",
          f"{len(both)} pairs with text on both sides. d1 and d2 are omitted: "
          "951 of 954 before-spans are a single sentence, so a length series does "
          "not exist.", "",
          "| dimension | n | mean Δ | sd | t | consistency |", "|---|---|---|---|---|---|"]
    pair_stats = {}
    for k in DIMS:
        if k in DOC_ONLY:
            continue
        s = stats(pd[k]); pair_stats[k] = s
        L.append(fmt(s, k))
    pws = stats(pd["_dwords"])
    L.append(fmt(pws, "word count"))
    L.append("")

    # ---------------- per story, direction agreement ----------------
    by_story = defaultdict(lambda: defaultdict(list))
    for story, label, d in rows:
        for k in DIMS:
            by_story[story][k].append(d[k])
    L += ["## Does the direction hold across stories?", "",
          "Mean displacement per story, document level. Agreement matters more than "
          "magnitude: a direction that reverses between projects is not a direction.", "",
          "| story | " + " | ".join(d.replace("_", " ") for d in DIMS) + " | n |",
          "|---|" + "---|" * (len(DIMS) + 1)]
    for st in sorted(by_story):
        cells = []
        for k in DIMS:
            v = [x for x in by_story[st][k] if x is not None]
            cells.append(f"{statistics.mean(v):+.3f}" if v else "—")
        L.append(f"| {st[:34]} | " + " | ".join(cells) + f" | {len(by_story[st][DIMS[0]])} |")
    L.append("")

    # ---------------- verdict ----------------
    strong = [k for k in DIMS
              if (doc_stats.get(k) and abs(doc_stats[k]["t"]) > 2
                  and doc_stats[k]["consistency"] > 0.6)]
    pstrong = [k for k in pair_stats
               if pair_stats[k] and abs(pair_stats[k]["t"]) > 2
               and pair_stats[k]["consistency"] > 0.6]
    verdict = "PROCEED" if (strong or pstrong) else "STOP"
    L.insert(3, f"## VERDICT: **{verdict}**\n\n"
                f"Document-level dimensions with a consistent direction: "
                f"{', '.join(strong) if strong else 'none'}.\n\n"
                f"Pair-level: {', '.join(pstrong) if pstrong else 'none'}.\n")
    open("corpus/step2_displacement.md", "w").write("\n".join(L) + "\n")

    print(f"VERDICT: {verdict}")
    print(f"\ndocument level ({len(docs)} transitions)")
    for k in DIMS:
        s = doc_stats[k]
        if s:
            print(f"  {k:16} mean {s['mean']:+.4f}  t {s['t']:+6.2f}  "
                  f"consistency {100*s['consistency']:3.0f}%  n {s['n']}")
    print(f"\npair level ({len(both)} pairs)")
    for k in DIMS:
        if k in DOC_ONLY:
            continue
        s = pair_stats[k]
        if s:
            print(f"  {k:16} mean {s['mean']:+.4f}  t {s['t']:+6.2f}  "
                  f"consistency {100*s['consistency']:3.0f}%  n {s['n']}")
    print(f"\n  word count doc  mean {ws['mean']:+.1f}  t {ws['t']:+.2f}" if ws else "")
    print(f"  word count pair mean {pws['mean']:+.2f}  t {pws['t']:+.2f}" if pws else "")


if __name__ == "__main__":
    main()
