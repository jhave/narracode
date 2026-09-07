"""Render the first draft as a standalone reading page (standard library only)."""
from pathlib import Path
from html import escape
import math

HERE = Path(__file__).resolve().parent
draft = (HERE / "drafts/1-the-mouth-on-loan.md").read_text()
body = draft.split("\n", 1)[1].strip()
paragraphs = body.split("\n\n")
word_count = sum(len(p.split()) for p in paragraphs if p != "***")
minutes = math.ceil(word_count / 250)
prose = "\n".join(
    '<hr aria-label="Scene break">' if p == "***" else f"<p>{escape(p)}</p>"
    for p in paragraphs
)
page = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Dorrie rents her sense of taste to an intelligence called Thursday. Then she invites it to cook dinner. A story written with Narracode.">
  <title>The Mouth on Loan — Narracode</title>
  <style>
    :root { color-scheme: light; }
    * { box-sizing: border-box; }
    body { margin: 0; background: #faf8f3; color: #24231f; font: 20px/1.75 Georgia, 'Times New Roman', serif; }
    main, body > nav, footer { width: calc(100% - 3rem); max-width: 700px; margin: auto; }
    body > nav { padding-top: 2rem; font: 14px/1.6 system-ui, sans-serif; }
    a { color: #644426; text-underline-offset: .2em; }
    a:hover { color: #21150b; }
    a:focus-visible { outline: 2px solid #644426; outline-offset: 5px; }
    header { padding: 4rem 0 2.5rem; border-bottom: 1px solid #d9d2c6; margin-bottom: 2.5rem; }
    h1 { font-size: clamp(2.5rem, 7vw, 4rem); line-height: 1.08; font-weight: normal; letter-spacing: -.04em; margin: 0 0 1.3rem; }
    .meta { font: 13px/1.7 system-ui, sans-serif; color: #645c50; margin: .5rem 0; }
    article p { margin: 0 0 1.15em; }
    article hr { border: 0; text-align: center; margin: 3rem 0; }
    article hr::after { content: '·  ·  ·'; color: #867864; letter-spacing: .4em; }
    footer { margin-top: 4rem; padding: 2rem 0 4rem; border-top: 1px solid #d9d2c6; font: 13px/1.8 system-ui, sans-serif; }
    footer nav { display: flex; flex-wrap: wrap; gap: .6rem 1.3rem; }
    @media (max-width: 480px) { body { font-size: 18px; } header { padding-top: 2.5rem; } }
    @media print { body { background: white; font-size: 11pt; } body > nav, footer { display: none; } header { padding-top: 0; } }
  </style>
</head>
<body>
  <nav aria-label="Breadcrumb"><a href="../../index.html">← Narracode / Stories</a></nav>
  <main>
    <header>
      <h1>The Mouth on Loan</h1>
      <p class="meta">September 7, 2026 · WORD_COUNT words · MINUTES min read · First draft</p>
      <p class="meta">David Jhave Johnston — premise, direction and constraints<br>OpenAI GPT-6 (Codex) — writing and page · Narracode AUTO_MODE</p>
    </header>
    <article aria-label="The Mouth on Loan">
PROSE
    </article>
  </main>
  <footer>
    <p>A complete first draft, awaiting human edits. Its contextual review is saved separately.</p>
    <nav aria-label="Story files">
      <a href="drafts/1-the-mouth-on-loan.md">Plain-text draft</a>
      <a href="POETICS.md">Poetics</a>
      <a href="ATTRIBUTION.md">Attribution</a>
      <a href="critiques/critique-all-acts.md">Draft review</a>
      <a href="versions/v1-2026-09-07-auto-mode/loop-notes.md">Version notes</a>
    </nav>
  </footer>
</body>
</html>
"""
page = page.replace("WORD_COUNT", f"{word_count:,}").replace("MINUTES", str(minutes)).replace("PROSE", prose)
(HERE / "index.html").write_text(page)
print(f"Rendered {word_count:,} words; {minutes} min read.")
