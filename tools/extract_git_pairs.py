#!/usr/bin/env python3
"""Substep 1.1b — emit edit pairs from git history.

For stories whose machine state exists only as a git parent commit, read the
before/after text by SHA and emit aligned span pairs. Source files are not
required in the working tree.

Reads  corpus/provenance.yaml  (human_commits / git_commits per story)
Writes corpus/git_pairs.jsonl, corpus/git_pairs_report.md
"""
import subprocess, sys, os, re, json, difflib, hashlib, yaml

sys.path.insert(0, os.path.dirname(__file__))
from build_diff_review import sents

EXTRACTOR_VERSION = "1.0.0"
SEGMENTER_VERSION = "0.9.0-crude"     # replaced by tools/segment.py at substep 1.3
THR = 0.40


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def mono(A, B):
    """Order-preserving sub-alignment (substep 1.4 method 5)."""
    cands = []
    for i, x in enumerate(A):
        for j, y in enumerate(B):
            r = difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()
            if r >= THR:
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


def op_of(before, after):
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


def main():
    L = yaml.safe_load(open("corpus/provenance.yaml"))
    records, report = [], []

    for story, cfg in L["stories"].items():
        commits = cfg.get("human_commits") or cfg.get("git_commits")
        if not commits:
            continue
        mm = None
        for mc in (cfg.get("machine_commits") or []):
            if mc.get("model"):
                mm = mc["model"]
        n_story = 0
        for entry in commits:
            sha = str(entry["sha"])
            parent = sh(f"git rev-parse --short {sha}~1").strip()
            date = str(entry.get("date", ""))
            files = [f for f in sh(f'git diff-tree --no-commit-id --name-only -r {sha} '
                                   f'-- "*/drafts/*.md"').strip().split("\n") if f.strip()]
            for path in files:
                before = sh(f'git show {sha}~1:"{path}" 2>/dev/null')
                after = sh(f'git show {sha}:"{path}"')
                if not before or not after:
                    report.append(f"| {story} | `{sha}` | {os.path.basename(path)} | "
                                  f"skipped — no parent version |")
                    continue
                A, B = sents(before), sents(after)
                n = 0
                for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
                        None, A, B, autojunk=False).get_opcodes():
                    if tag == "equal":
                        continue
                    for b, a, r, idx in mono(A[i1:i2], B[j1:j2]):
                        if norm(b) == norm(a):        # no-signal filter
                            continue
                        gid = hashlib.sha1(
                            f"{sha}{path}{i1+max(idx,0)}{b}{a}".encode()).hexdigest()[:10]
                        records.append({
                            "id": f"{story}/{os.path.basename(path)[:-3]}/{gid}",
                            "story": story,
                            "draft": os.path.basename(path),
                            "from_snapshot": parent,
                            "to_snapshot": sha,
                            "date": date,
                            "index": i1 + max(idx, 0),
                            "before": b,
                            "after": a,
                            "op": op_of(b, a),
                            "confidence": round(r, 2),
                            "source": "git",
                            "machine_model": mm,
                            "provenance_source": "jhave",
                            "extractor_version": EXTRACTOR_VERSION,
                            "segmenter_version": SEGMENTER_VERSION,
                        })
                        n += 1
                        n_story += 1
                report.append(f"| {story} | `{sha}` | {os.path.basename(path)} | {n} pairs |")
        print(f"{story:44} {n_story:5} pairs")

    records.sort(key=lambda r: (r["story"], r["date"], r["draft"], r["index"]))
    with open("corpus/git_pairs.jsonl", "w") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    from collections import Counter
    ops = Counter(r["op"] for r in records)
    st = Counter(r["story"] for r in records)
    lines = ["# Git-derived edit pairs — substep 1.1b", "",
             f"Generated by `tools/extract_git_pairs.py`. **{len(records)} pairs.**", "",
             "Source files are not in this tree; before/after text is read from branch",
             "SHAs. The extractor requires those refs to be fetched.", "",
             "## Per story", "", "| story | pairs |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in st.most_common()]
    lines += ["", "## Operation distribution", "", "| op | count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in ops.most_common()]
    lines += ["", "## Per commit", "", "| story | commit | draft | result |", "|---|---|---|---|"]
    lines += report
    open("corpus/git_pairs_report.md", "w").write("\n".join(lines) + "\n")

    print(f"\nTOTAL {len(records)} pairs -> corpus/git_pairs.jsonl")
    print("ops:", dict(ops))


if __name__ == "__main__":
    main()
