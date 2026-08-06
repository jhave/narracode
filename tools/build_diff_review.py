#!/usr/bin/env python3
"""Build a chronological diff-lineage page for provenance review.

For every story: each consecutive snapshot transition, in order, showing what
actually changed. Plus final-draft -> published index.html, which is usually a
human edit that no snapshot records.

Display-only. Uses a crude sentence splitter; the production segmenter is
substep 1.3. Nothing here writes to the corpus.
"""
import os, re, json, html, difflib
from collections import defaultdict

ROOT = "Stories written with Narracode"
BLOB = ("https://github.com/jhave/narracode/blob/"
        "claude/narracode-harness-qualitative-research-report/")
MAX_SPANS = 14          # changed spans shown per transition
CTX = 90                # chars of context either side

SPLIT = re.compile(r'(?<=[.!?])\s+|\n{2,}')


def sents(text):
    text = re.sub(r'^---.*?---', '', text, flags=re.S)          # yaml front matter
    text = re.sub(r'^#+ .*$', '', text, flags=re.M)             # headings
    out = []
    for chunk in text.split("\n"):
        chunk = chunk.strip()
        if not chunk or chunk in ("***", "---", "* * *"):
            continue
        out += [s.strip() for s in SPLIT.split(chunk) if s.strip()]
    return out


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def published_text(story):
    """Story prose from the published index.html, prompt paragraphs dropped."""
    p = os.path.join(ROOT, story, "index.html")
    if not os.path.exists(p):
        return None
    s = read(p)
    m = re.search(r'<body.*?>(.*)</body>', s, re.S)
    body = m.group(1) if m else s
    body = re.sub(r'<(script|style|details|nav|footer).*?</\1>', '', body, flags=re.S | re.I)
    ps = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    keep = []
    for x in ps:
        t = html.unescape(re.sub(r'<[^>]+>', '', x)).strip()
        if not t:
            continue
        if re.match(r"^\[?(let'?s write|follow-up|amendment|prompt)", t, re.I):
            continue
        keep.append(t)
    return "\n".join(keep) if keep else None


def diff_spans(a_txt, b_txt):
    A, B = sents(a_txt), sents(b_txt)
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    spans, eq = [], 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            eq += i2 - i1
            continue
        spans.append({"tag": tag,
                      "before": " ".join(A[i1:i2]),
                      "after": " ".join(B[j1:j2]),
                      "at": i1})
    total = max(len(A), 1)
    return spans, {"sent_before": len(A), "sent_after": len(B),
                   "unchanged_pct": round(100 * eq / total),
                   "w_before": len(a_txt.split()), "w_after": len(b_txt.split()),
                   "changed": len(spans)}


def word_diff(before, after):
    """Inline word-level highlight."""
    a, b = before.split(), after.split()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ob, oa = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        sb, sa = html.escape(" ".join(a[i1:i2])), html.escape(" ".join(b[j1:j2]))
        if tag == "equal":
            ob.append(sb); oa.append(sa)
        elif tag == "delete":
            ob.append(f"<del>{sb}</del>")
        elif tag == "insert":
            oa.append(f"<ins>{sa}</ins>")
        else:
            ob.append(f"<del>{sb}</del>"); oa.append(f"<ins>{sa}</ins>")
    return " ".join(x for x in ob if x), " ".join(x for x in oa if x)


def shape(st):
    """Descriptive evidence only. jhave decides provenance, not this function."""
    u = st["unchanged_pct"]
    grew = st["w_after"] > st["w_before"] * 1.4
    if grew:                       # checked first: keeping all text and adding
        return "expansion", "prior text retained, substantial new text appended"
    if u >= 85 and st["w_after"] <= st["w_before"]:
        return "surgical", "most text untouched, net shorter"
    if u >= 85:
        return "surgical", "most text untouched, slightly longer"
    if u >= 55:
        return "mixed", "substantial edits, much retained"
    return "wholesale", "most sentences replaced"


def match_drafts(a, b):
    """Pair drafts across two snapshots.

    Exact filename first. Any leftovers on both sides are matched by CONTENT
    similarity, because a human edit is sometimes saved under a new name
    (Cussinct v2 `1-cussinct.md` -> v3 `1-cussinct-human-edit-snapshot.md`),
    and exact-name matching silently drops precisely the machine->human pairs
    that matter most. Content matching is measurable, unlike name guessing.
    """
    A, B = set(a["drafts"]), set(b["drafts"])
    pairs = [(f, f, 1.0, "name") for f in sorted(A & B)]
    ra, rb = sorted(A - B), sorted(B - A)
    if not ra or not rb:
        return pairs
    cache = {}

    def txt(rec, fn):
        k = (rec["path"], fn)
        if k not in cache:
            cache[k] = read(os.path.join(rec["path"], "drafts", fn))[:20000]
        return cache[k]

    cands = []
    for fa in ra:
        for fb in rb:
            r = difflib.SequenceMatcher(None, txt(a, fa), txt(b, fb),
                                        autojunk=False).quick_ratio()
            cands.append((r, fa, fb))
    cands.sort(reverse=True)
    used_a, used_b = set(), set()
    for r, fa, fb in cands:
        if r < 0.50 or fa in used_a or fb in used_b:
            continue
        used_a.add(fa); used_b.add(fb)
        pairs.append((fa, fb, round(r, 2), "content"))
    return pairs


def main():
    S = json.load(open("corpus/survey.json"))
    recs = S["records"]
    snaps = defaultdict(list)
    for r in recs:
        if r["type"] == "snapshot":
            snaps[r["story"]].append(r)
    for v in snaps.values():
        v.sort(key=lambda r: (r["date"] or "", r["vnum"] if r["vnum"] is not None else 999))

    amb = {(r["story"], r["entry"]) for r in recs
           if r["type"] == "snapshot"
           and r["name_signal"] in ("content-only", "ambiguous-temporal", "none")}

    blocks, summary = [], []
    for story in sorted(snaps):
        seq = snaps[story]
        if len(seq) < 1:
            continue
        rows = []
        # consecutive transitions
        for a, b in zip(seq, seq[1:]):
            pairs = match_drafts(a, b)
            if not pairs:
                rows.append({"kind": "nopair", "a": a, "b": b}); continue
            for fa, fb, ratio, how in pairs:
                at = read(os.path.join(a["path"], "drafts", fa))
                bt = read(os.path.join(b["path"], "drafts", fb))
                if at == bt:
                    continue
                sp, st = diff_spans(at, bt)
                if not sp:
                    continue
                rows.append({"kind": "diff", "a": a, "b": b, "fn": fa, "fn_b": fb,
                             "match": how, "ratio": ratio, "spans": sp, "st": st})
        # final draft -> published
        pub = published_text(story)
        if pub and seq:
            last = seq[-1]
            best = max(last["drafts"], key=lambda f: last["draft_words"].get(f, 0))
            lt = read(os.path.join(last["path"], "drafts", best))
            sp, st = diff_spans(lt, pub)
            if sp:
                rows.append({"kind": "pub", "a": last, "fn": best,
                             "spans": sp, "st": st})
        if not rows:
            continue

        blocks.append(f'<h2 id="{html.escape(story)}">{html.escape(story)}</h2>')
        for r in rows:
            if r["kind"] == "nopair":
                blocks.append(
                    f'<p class="note">No shared draft filenames between '
                    f'<code>{html.escape(r["a"]["entry"])}</code> and '
                    f'<code>{html.escape(r["b"]["entry"])}</code> — no pair possible.</p>')
                continue
            st = r["st"]; kind, why = shape(st)
            if r["kind"] == "pub":
                head = (f'<code>{html.escape(r["a"]["entry"])}/{html.escape(r["fn"])}</code>'
                        f' &rarr; <strong>published index.html</strong>')
                flag = '<span class="pub">FINAL — likely your edit</span>'
                aq = (r["a"]["story"], r["a"]["entry"])
                links = (f'<a href="{BLOB}{q(r["a"]["path"])}/drafts/{r["fn"]}" target="_blank">draft</a> · '
                         f'<a href="{BLOB}{q(os.path.join(ROOT, story))}/index.html" target="_blank">published</a>')
            else:
                fnlabel = (html.escape(r["fn"]) if r["fn"] == r.get("fn_b", r["fn"])
                           else f'{html.escape(r["fn"])} &rarr; {html.escape(r["fn_b"])}')
                renamed = ('' if r.get("match") == "name"
                           else f' <span class="ren">renamed · matched on content {r.get("ratio")}</span>')
                head = (f'<code>{html.escape(r["a"]["entry"])}</code> &rarr; '
                        f'<code>{html.escape(r["b"]["entry"])}</code> · '
                        f'<span class="fn">{fnlabel}</span>{renamed}')
                marks = []
                if (story, r["a"]["entry"]) in amb: marks.append("from")
                if (story, r["b"]["entry"]) in amb: marks.append("to")
                flag = (f'<span class="amb">? {"/".join(marks)} unknown</span>' if marks
                        else '<span class="known">both known</span>')
                links = (f'<a href="{BLOB}{q(r["a"]["path"])}/drafts/{r["fn"]}" target="_blank">before</a> · '
                         f'<a href="{BLOB}{q(r["b"]["path"])}/drafts/{r.get("fn_b", r["fn"])}" target="_blank">after</a>')

            summary.append((story, head, kind, st, flag))
            body = []
            for sp in r["spans"][:MAX_SPANS]:
                b_, a_ = word_diff(sp["before"], sp["after"])
                body.append('<div class="sp">')
                if sp["before"]:
                    body.append(f'<div class="b">{b_ or "&nbsp;"}</div>')
                if sp["after"]:
                    body.append(f'<div class="a">{a_ or "&nbsp;"}</div>')
                body.append(f'<div class="t">{sp["tag"]} @ sentence {sp["at"]}</div></div>')
            more = (f'<p class="note">…and {len(r["spans"]) - MAX_SPANS} further changed spans. '
                    f'Open the files to see all.</p>' if len(r["spans"]) > MAX_SPANS else "")
            blocks.append(
                f'<details class="tr {kind}"><summary>{head} &nbsp; {flag}'
                f'<span class="stat">{st["changed"]} changed · {st["unchanged_pct"]}% untouched · '
                f'{st["w_before"]:,}&rarr;{st["w_after"]:,} w · <em>{kind}</em></span></summary>'
                f'<p class="note">{why}. {links}</p>{"".join(body)}{more}</details>')

    open("corpus/diff_review_blocks.html", "w").write("\n".join(blocks))
    json.dump([{"story": s, "kind": k, "stats": st} for s, _, k, st, _ in summary],
              open("corpus/diff_summary.json", "w"), indent=1)
    print(f"stories {len(snaps)}  diff blocks {len(summary)}")


def q(p):
    import urllib.parse
    return urllib.parse.quote(p)


if __name__ == "__main__":
    main()
