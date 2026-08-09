#!/usr/bin/env python3
"""Substep 1.3 — evaluate segmenter candidates against the hand-labelled cases.

Reports accuracy PER CATEGORY, because an overall figure hides categorical
failure and the fragment categories are the ones that matter here.

Writes corpus/segmenter_eval.md
"""
import re, sys, os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import segment as narracode_seg

CASES = "tools/tests/segment_cases.md"


def load_cases():
    txt = open(CASES, encoding="utf-8").read()
    cases = []
    for blk in re.split(r'^### ', txt, flags=re.M)[1:]:
        head, _, rest = blk.partition("\n")
        parts = [p.strip() for p in head.split("|")]
        cid, cat = parts[0], parts[1]
        m = re.search(r'^TEXT:\s?(.*?)(?=^EXPECT:)', rest, re.S | re.M)
        if not m:
            continue
        text = m.group(1).rstrip("\n")
        if text.startswith(" "):
            text = text[1:]
        exp_blk = rest[rest.index("EXPECT:") + len("EXPECT:"):]
        exp = [l[2:].strip() for l in exp_blk.split("\n") if l.startswith("- ")]
        cases.append({"id": cid, "cat": cat, "text": text, "expect": exp})
    return cases


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


# ---- candidates -------------------------------------------------------------

def cand_narracode(t):
    return narracode_seg.segment(t)


def cand_naive(t):
    """The crude splitter used before this substep."""
    SPLIT = re.compile(r'(?<=[.!?])\s+|\n{2,}')
    out = []
    t = re.sub(r'^#+ .*$', '', t, flags=re.M)
    for chunk in t.split("\n"):
        chunk = chunk.strip()
        if not chunk or chunk in ("***", "---", "* * *"):
            continue
        out += [s.strip() for s in SPLIT.split(chunk) if s.strip()]
    return out


def cand_nltk(t):
    import nltk
    return [s for line in t.split("\n") if line.strip()
            for s in nltk.sent_tokenize(line.strip())]


def cand_pysbd(t):
    import pysbd
    seg = pysbd.Segmenter(language="en", clean=False)
    return [s.strip() for line in t.split("\n") if line.strip()
            for s in seg.segment(line.strip()) if s.strip()]


def main():
    cases = load_cases()
    cands = {"narracode (this)": cand_narracode, "naive (previous)": cand_naive}
    try:
        import nltk
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt", quiet=True)
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab", quiet=True)
        cand_nltk("Test. Test.")
        cands["nltk punkt"] = cand_nltk
    except Exception as e:
        print(f"nltk unavailable: {type(e).__name__}")
    try:
        cand_pysbd("Test. Test.")
        cands["pysbd"] = cand_pysbd
    except Exception as e:
        print(f"pysbd unavailable: {type(e).__name__}")

    cats = sorted({c["cat"] for c in cases})
    results = {}
    failures = defaultdict(list)
    for name, fn in cands.items():
        per = defaultdict(lambda: [0, 0])
        for c in cases:
            try:
                got = [norm(x) for x in fn(c["text"])]
            except Exception:
                got = ["<ERROR>"]
            exp = [norm(x) for x in c["expect"]]
            ok = got == exp
            per[c["cat"]][1] += 1
            if ok:
                per[c["cat"]][0] += 1
            else:
                failures[name].append((c["id"], c["cat"], exp, got))
        results[name] = per

    tot_sents = sum(len(c["expect"]) for c in cases)
    L = ["# Segmenter evaluation — substep 1.3", "",
         f"{len(cases)} hand-labelled cases, {tot_sents} expected sentences, "
         f"{len(cats)} categories. Text is verbatim corpus; labels written by hand.", "",
         "A case counts as correct only if the full sentence list matches exactly.", "",
         "## Accuracy by category", "",
         "| category | cases | " + " | ".join(results) + " |",
         "|---|---|" + "---|" * len(results)]
    for cat in cats:
        n = results[list(results)[0]][cat][1]
        row = f"| {cat} | {n} |"
        for name in results:
            g, t = results[name][cat]
            row += f" {100*g//t if t else 0}% |"
        L.append(row)
    L.append("")
    L.append("| **overall** | " + str(len(cases)) + " |" + "".join(
        f" **{100*sum(v[0] for v in results[n].values())//len(cases)}%** |" for n in results))

    L += ["", "## Failures", ""]
    for name in results:
        fl = failures[name]
        L.append(f"### {name} — {len(fl)} failing case(s)")
        L.append("")
        for cid, cat, exp, got in fl[:12]:
            L.append(f"- **{cid}** ({cat})")
            L.append(f"  - expected {len(exp)}: `{' | '.join(exp)[:200]}`")
            L.append(f"  - got {len(got)}: `{' | '.join(got)[:200]}`")
        if len(fl) > 12:
            L.append(f"- …and {len(fl)-12} more")
        L.append("")

    open("corpus/segmenter_eval.md", "w").write("\n".join(L) + "\n")

    print(f"\n{'candidate':22} overall   worst category")
    for name in results:
        g = sum(v[0] for v in results[name].values())
        worst = min(((100*v[0]//v[1] if v[1] else 0), k) for k, v in results[name].items())
        print(f"{name:22} {100*g//len(cases):3}%      {worst[1]} {worst[0]}%")


if __name__ == "__main__":
    main()
