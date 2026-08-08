#!/usr/bin/env python3
"""Substep 1.5 — emit the edit-pair corpus from version snapshots.

Reads corpus/provenance.yaml and corpus/survey.json.
Writes corpus/edit_pairs.jsonl and corpus/extract_report.md

  python3 tools/extract_pairs.py --rebuild
  python3 tools/extract_pairs.py --story <name>
  python3 tools/extract_pairs.py --validate
"""
import os, re, sys, json, html, hashlib, argparse, datetime
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(__file__))
import yaml
from segment import segment, VERSION as SEG_VERSION
from align import align, match_drafts, norm, VERSION as ALIGN_VERSION

ROOT = "Stories written with Narracode"
EXTRACTOR_VERSION = "1.0.0"


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def published_text(story):
    p = os.path.join(ROOT, story, "index.html")
    if not os.path.exists(p):
        return None
    s = read(p)
    m = re.search(r'<body.*?>(.*)</body>', s, re.S)
    body = m.group(1) if m else s
    body = re.sub(r'<(script|style|details|nav|footer).*?</\1>', '', body, flags=re.S | re.I)
    keep = []
    for x in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S):
        t = html.unescape(re.sub(r'<[^>]+>', '', x)).strip()
        if not t or re.match(r"^\[?(let'?s write|follow-up|amendment|prompt)", t, re.I):
            continue
        keep.append(t)
    return "\n".join(keep) if keep else None


def snapshots_for(survey, story):
    s = [r for r in survey["records"] if r["type"] == "snapshot" and r["story"] == story]
    # v0 must sort first: `vnum or 999` would send it last, silently reversing
    # transition direction. See substep 1.6 section E0.
    s.sort(key=lambda r: (r["date"] or "", r["vnum"] if r["vnum"] is not None else 999))
    return s


def transitions(seq, prov):
    """machine -> human, immediate and cumulative."""
    def p(e):
        d = (prov or {}).get(e) or {}
        return d.get("provenance", "unknown"), d.get("usable", True)

    out = []
    for a, b in zip(seq, seq[1:]):
        pa, ua = p(a["entry"]); pb, ub = p(b["entry"])
        if pa == "machine" and pb == "human" and ua and ub:
            out.append((a, b, "immediate"))
    i = 0
    while i < len(seq) - 1:
        pa, ua = p(seq[i]["entry"])
        if pa == "machine" and ua:
            j, last = i + 1, None
            while j < len(seq):
                pj, uj = p(seq[j]["entry"])
                if pj == "human" and uj:
                    last = j; j += 1
                else:
                    break
            if last is not None and last > i + 1:
                out.append((seq[i], seq[last], "cumulative"))
            i = last if last else i + 1
        else:
            i += 1
    return out


def build(only_story=None):
    L = yaml.safe_load(open("corpus/provenance.yaml"))
    survey = json.load(open("corpus/survey.json"))

    bad = [f"{s}/{k}" for s, c in L["stories"].items()
           for k, v in (c.get("snapshots") or {}).items()
           if v.get("provenance") == "unknown" and v.get("usable", True)]
    if bad:
        sys.exit(f"ERROR: usable snapshots with unknown provenance: {bad[:5]}")

    records, exceptions, report = [], [], []
    for story, cfg in L["stories"].items():
        if only_story and story != only_story:
            continue
        if cfg.get("usable") is False:
            report.append((story, "EXCLUDED", cfg.get("note", "")[:70], 0))
            continue
        seq = snapshots_for(survey, story)
        prov = cfg.get("snapshots") or {}
        n = 0

        for a, b, kind in transitions(seq, prov):
            pairs_f, unmatched = match_drafts(a["path"], a["drafts"],
                                              b["path"], b["drafts"], read)
            for f in unmatched:
                exceptions.append((story, f"{a['entry']}->{b['entry']}", f, "no draft match"))
            for fa, fb, mr, how in pairs_f:
                bt = read(os.path.join(a["path"], "drafts", fa))
                at = read(os.path.join(b["path"], "drafts", fb))
                if bt == at:
                    continue
                ps, st = align(bt, at, segment)
                for p in ps:
                    records.append(mk(story, fb, a["entry"], b["entry"],
                                      b.get("date") or "", p, "snapshot",
                                      kind, how, mr, cfg))
                    n += 1
                if st["gated"]:
                    exceptions.append((story, f"{a['entry']}->{b['entry']}", fb,
                                       f"{st['gated']} below confidence gate"))

        pc = cfg.get("published") or {}
        if pc.get("usable") and seq:
            last = seq[-1]
            draft = pc.get("draft") or max(last["drafts"],
                                           key=lambda f: last["draft_words"].get(f, 0))
            t = published_text(story)
            fp = os.path.join(last["path"], "drafts", draft)
            if t and os.path.exists(fp):
                ps, st = align(read(fp), t, segment, substitutions_only=True)
                for p in ps:
                    records.append(mk(story, draft, last["entry"], "published",
                                      "", p, "published", "published", "name", 1.0, cfg))
                    n += 1
        report.append((story, f"{len(transitions(seq, prov))} transitions", "", n))
    return records, exceptions, report


def mk(story, draft, frm, to, date, p, source, kind, how, mr, cfg):
    gid = hashlib.sha1(f"{story}{draft}{frm}{to}{p['index']}"
                       f"{p['before']}{p['after']}".encode()).hexdigest()[:10]
    mm = None
    for c in (cfg.get("machine_commits") or []):
        if c.get("model"):
            mm = c["model"]
    return {
        "id": f"{story}/{draft[:-3] if draft.endswith('.md') else draft}/{gid}",
        "story": story, "draft": draft,
        "from_snapshot": frm, "to_snapshot": to, "date": date,
        "index": p["index"], "before": p["before"], "after": p["after"],
        "op": p["op"], "confidence": p["confidence"],
        "source": source, "pair_type": kind,
        "draft_match": how, "draft_match_ratio": mr,
        "machine_model": mm,
        "provenance_source": "jhave",
        "extractor_version": EXTRACTOR_VERSION,
        "align_version": ALIGN_VERSION,
        "segmenter_version": SEG_VERSION,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--story")
    ap.add_argument("--validate", action="store_true")
    a = ap.parse_args()

    t0 = datetime.datetime.now()
    records, exceptions, report = build(a.story)

    if a.story:
        for r in records[:40]:
            print(f"  [{r['op']:10}] {r['before'][:60]!r}\n{'':16}-> {r['after'][:60]!r}")
        print(f"\n{len(records)} pairs (not written)")
        return

    records.sort(key=lambda r: (r["story"], r["draft"], r["index"], r["id"]))
    if a.validate:
        old = [json.loads(l) for l in open("corpus/edit_pairs.jsonl")]
        same = [r["id"] for r in records] == [r["id"] for r in old]
        print(f"validate: {len(records)} vs {len(old)} stored — "
              f"{'IDENTICAL' if same else 'DRIFT'}")
        return

    tmp = "corpus/edit_pairs.jsonl.tmp"
    with open(tmp, "w") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, "corpus/edit_pairs.jsonl")

    ops = Counter(r["op"] for r in records)
    src = Counter(r["source"] for r in records)
    conf = sorted(r["confidence"] for r in records if r["confidence"])
    L = ["# Snapshot-derived edit pairs — substep 1.5", "",
         f"`tools/extract_pairs.py` · extractor {EXTRACTOR_VERSION} · "
         f"align {ALIGN_VERSION} · segmenter {SEG_VERSION}", "",
         f"**{len(records)} pairs.** Run {t0:%Y-%m-%d %H:%M}, "
         f"{(datetime.datetime.now()-t0).total_seconds():.1f}s", "",
         "## Per story", "", "| story | transitions | pairs |", "|---|---|---|"]
    L += [f"| {s} | {t} | {n} |" for s, t, _, n in sorted(report)]
    L += ["", "## Operations", "", "| op | count |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in ops.most_common()]
    L += ["", "## Source", "", "| source | count |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in src.most_common()]
    if conf:
        L += ["", f"Confidence: min {conf[0]}, median {conf[len(conf)//2]}, "
                  f"max {conf[-1]}, below 0.5: {sum(1 for c in conf if c < 0.5)}"]
    L += ["", f"## Exceptions ({len(exceptions)})", "",
          "| story | transition | draft | reason |", "|---|---|---|---|"]
    L += [f"| {s} | {t} | {d} | {r} |" for s, t, d, r in exceptions]
    open("corpus/extract_report.md", "w").write("\n".join(L) + "\n")

    print(f"{len(records)} pairs -> corpus/edit_pairs.jsonl")
    print("ops:", dict(ops))
    print(f"exceptions: {len(exceptions)}")


if __name__ == "__main__":
    main()
