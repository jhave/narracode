#!/usr/bin/env python3
"""Diff-lineage page for Crepuscular, which lives only on an unmerged branch.

Reads everything from git (the story is not in the working tree). Shows every
commit in order, with word-level diffs for each of jhave's edits, plus the full
final text of each act so the story can be read.
"""
import subprocess, sys, os, re, html, difflib

sys.path.insert(0, os.path.dirname(__file__))
from build_diff_review import sents, word_diff

BRANCH = "origin/claude/life-game-awakening-story-cbc1kj"
STORY = "Stories written with Narracode/25-06-2026_Crepuscular"
GH = "https://github.com/jhave/narracode"
BR = "claude/life-game-awakening-story-cbc1kj"
ACTS = ["0-character-creation", "1-the-casual-hack", "2-the-branch-trails",
        "3-edits", "4-crepuscular"]


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def mono(A, B, thr=0.40):
    c = []
    for i, x in enumerate(A):
        for j, y in enumerate(B):
            r = difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()
            if r >= thr:
                c.append((r, i, j))
    c.sort(reverse=True)
    acc = []
    for r, i, j in c:
        if any(i == pi or j == pj or (i - pi) * (j - pj) < 0 for _, pi, pj in acc):
            continue
        acc.append((r, i, j))
    ua = {i for _, i, _ in acc}
    ub = {j for _, _, j in acc}
    out = [(A[i], B[j], "edit", r) for r, i, j in sorted(acc, key=lambda t: t[1])
           if norm(A[i]) != norm(B[j])]
    out += [(A[i], "", "cut", 0.0) for i in range(len(A)) if i not in ua]
    out += [("", B[j], "added", 0.0) for j in range(len(B)) if j not in ub]
    return out


def diff_commit(sha, path):
    before = sh(f'git show {sha}~1:"{path}" 2>/dev/null')
    after = sh(f'git show {sha}:"{path}"')
    if not after:
        return None
    A, B = sents(before), sents(after)
    rows = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        rows += mono(A[i1:i2], B[j1:j2])
    return rows, len(A), len(B)


def main():
    log = sh(f'git log --reverse --format="%h|%an|%ad|%s" --date=short '
             f'{BRANCH} -- "{STORY}/drafts/*.md"').strip().split("\n")
    commits = [l.split("|", 3) for l in log if l]

    blocks = []
    n_edit = n_cut = n_add = 0
    for sha, author, date, msg in commits:
        is_h = author == "jhave"
        files = [f for f in sh(f'git diff-tree --no-commit-id --name-only -r {sha} '
                               f'-- "{STORY}/drafts/*.md"').strip().split("\n") if f.strip()]
        if not is_h:
            blocks.append(
                f'<div class="mach"><span class="tag m">MACHINE</span> '
                f'<code>{sha}</code> · {date} · {html.escape(msg)} '
                f'<span class="fl">{len(files)} draft(s)</span></div>')
            continue
        for path in files:
            res = diff_commit(sha, path)
            if not res:
                continue
            rows, na, nb = res
            rows = [r for r in rows if r[0] or r[1]]
            if not rows:
                continue
            e = sum(1 for r in rows if r[2] == "edit")
            c = sum(1 for r in rows if r[2] == "cut")
            a = sum(1 for r in rows if r[2] == "added")
            n_edit += e; n_cut += c; n_add += a
            body = []
            for b, af, kind, r in rows:
                body.append('<div class="sp">')
                if kind == "edit":
                    bd, ad = word_diff(b, af)
                    body.append(f'<div class="b">{bd}</div><div class="a">{ad}</div>')
                elif kind == "cut":
                    body.append(f'<div class="b">{html.escape(b)}</div>')
                else:
                    body.append(f'<div class="a">{html.escape(af)}</div>')
                body.append(f'<div class="t">{kind}{"" if r==0 else f" · similarity {r:.2f}"}</div></div>')
            fn = os.path.basename(path)
            blocks.append(
                f'<details class="tr"><summary><span class="tag h">JHAVE</span> '
                f'<code>{sha}</code> · {date} · <strong>{html.escape(fn)}</strong>'
                f'<span class="stat">{e} edited · {c} cut · {a} added · '
                f'{na}&rarr;{nb} sentences</span></summary>'
                f'<p class="note"><a href="{GH}/commit/{sha}" target="_blank">view commit on GitHub</a></p>'
                f'{"".join(body)}</details>')

    # full text of each act, final state
    reads = []
    total_w = 0
    for act in ACTS:
        txt = sh(f'git show {BRANCH}:"{STORY}/drafts/{act}.md"')
        if not txt:
            continue
        w = len(txt.split()); total_w += w
        esc = html.escape(txt)
        reads.append(
            f'<details class="rd"><summary>{html.escape(act)}.md '
            f'<span class="stat">{w:,} words</span></summary><pre>{esc}</pre></details>')

    CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
background:#fcfcfc;color:#111;line-height:1.5;padding:2rem 1.4rem;max-width:900px;margin:0 auto}
h1{font-size:1.55rem;font-weight:800;margin-bottom:.2rem;letter-spacing:-.02em}
.meta{color:#777;font-size:.82rem;text-transform:uppercase;letter-spacing:.05em;margin-bottom:1.4rem}
h2{font-size:1.1rem;margin-top:2.4rem;margin-bottom:.6rem;padding-bottom:.25rem;border-bottom:2px solid #ddd}
p{margin-bottom:.8rem}a{color:#0366d6;text-decoration:none}a:hover{text-decoration:underline}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.8em;
background:#f2f2ee;padding:.08em .3em;border-radius:3px}
.how{background:#f5f5f0;border-left:3px solid #999;padding:.9rem 1.1rem;margin:1.2rem 0;font-size:.9rem}
.warn{background:#fff8e6;border-left:3px solid #d99a00;padding:.9rem 1.1rem;margin:1.2rem 0;font-size:.9rem}
details.tr{border:1px solid #e0e0d8;border-left:4px solid #2a7d2a;border-radius:4px;
margin-bottom:.5rem;background:#fff}
details.rd{border:1px solid #e0e0d8;border-radius:4px;margin-bottom:.5rem;background:#fff}
details summary{cursor:pointer;padding:.55rem .8rem;font-size:.86rem;user-select:none}
details[open] summary{border-bottom:1px solid #eee;background:#fafaf7}
.mach{border:1px solid #eee;border-left:4px solid #b03030;border-radius:4px;background:#fdfdfd;
padding:.5rem .8rem;margin-bottom:.5rem;font-size:.82rem;color:#666}
.tag{font-size:.68rem;font-weight:700;padding:.1em .45em;border-radius:3px;letter-spacing:.04em}
.tag.h{background:#e8f3e8;color:#2a7d2a}.tag.m{background:#fdeaea;color:#b03030}
.stat{display:block;color:#777;font-size:.76rem;margin-top:.2rem;font-family:ui-monospace,Menlo,monospace}
.fl{color:#999;font-size:.75rem}
.note{font-size:.78rem;color:#777;padding:.45rem .8rem;margin:0}
.sp{border-top:1px solid #f0f0ea;padding:.5rem .8rem}
.sp .b{background:#fff6f6;padding:.3rem .45rem;border-radius:3px;font-size:.87rem;margin-bottom:.22rem}
.sp .a{background:#f4fbf4;padding:.3rem .45rem;border-radius:3px;font-size:.87rem}
.sp .t{font-size:.68rem;color:#aaa;font-family:ui-monospace,Menlo,monospace;margin-top:.22rem}
del{background:#ffd7d5;text-decoration:line-through;padding:0 .1em}
ins{background:#ccecd4;text-decoration:none;padding:0 .1em}
pre{background:#fafaf7;padding:1rem;overflow-x:auto;font-size:.84rem;line-height:1.6;
white-space:pre-wrap;border-top:1px solid #eee;margin:0}
"""
    n_h = sum(1 for c in commits if c[1] == "jhave")
    n_m = len(commits) - n_h
    out = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Crepuscular — diff lineage (unmerged branch)</title><style>{CSS}</style></head><body>

<h1>Crepuscular</h1>
<div class="meta">Diff lineage &nbsp;|&nbsp; unmerged branch &nbsp;|&nbsp; 5 acts, {total_w:,} words</div>

<div class="warn">
<strong>This story is not published and not on <code>main</code>.</strong> It lives complete on the branch
<a href="{GH}/tree/{BR}" target="_blank"><code>{BR}</code></a>, absent from <code>metadata.md</code> and
<code>index.html</code>, with no built <code>index.html</code> of its own. Last touched 2 July 2026.
<br><br>
<a href="{GH}/tree/{BR}/Stories%20written%20with%20Narracode/25-06-2026_Crepuscular" target="_blank">Browse the story folder</a> ·
<a href="{GH}/tree/{BR}/Stories%20written%20with%20Narracode/25-06-2026_Crepuscular/drafts" target="_blank">drafts/</a> ·
<a href="{GH}/compare/main...{BR}" target="_blank">full branch diff</a>
</div>

<div class="how">
<strong>Why this is the cleanest provenance in the corpus.</strong> Every commit is separated by git
<em>author</em>: <span class="tag m">MACHINE</span> commits are authored by Claude,
<span class="tag h">JHAVE</span> commits by you, each carrying the GitHub web editor's default message
<code>Update &lt;file&gt;.md</code>. No naming convention to interpret, no ambiguity.
{n_m} machine commits, {n_h} yours.
<br><br>
Below, each of your commits is diffed against its parent — the machine state immediately before you touched
it. <del>Red</del> is what you removed, <ins>green</ins> what you added.
Totals: <strong>{n_edit} sentences edited, {n_cut} cut, {n_add} added</strong>.
</div>

<h2>Lineage, in order</h2>
{''.join(blocks)}

<h2>Read the story — final state</h2>
<p class="note">Text as it stands on the branch, after your last edit.</p>
{''.join(reads)}

</body></html>"""
    open("2026-08-06_crepuscular-diff-review.html", "w").write(out)
    print(f"commits {len(commits)} (machine {n_m}, jhave {n_h})")
    print(f"edited {n_edit}  cut {n_cut}  added {n_add}  total {n_edit+n_cut+n_add}")
    print(f"words {total_w:,}  bytes {os.path.getsize('2026-08-06_crepuscular-diff-review.html'):,}")


if __name__ == "__main__":
    main()
