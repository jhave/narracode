"""Render the current draft as a standalone reading page (standard library only)."""
from pathlib import Path
from html import escape
import math
import re

HERE = Path(__file__).resolve().parent
draft = (HERE / "drafts/3-mouth-on-loan.md").read_text()
body = draft.split("\n", 1)[1].strip()
paragraphs = re.split(r"\n[ \t]*\n", body)
word_count = sum(len(p.split()) for p in paragraphs if p != "***")
minutes = math.ceil(word_count / 250)
prompt_sections = (HERE / "PROMPTS.md").read_text().strip().split("\n\n")[2:]
prompt_html = "\n".join(f"<h3>{escape(p[3:])}</h3>" if p.startswith("## ") else f"<p>{escape(p)}</p>" for p in prompt_sections)
def inline(text):
    # The story uses underscore emphasis. Escape HTML before adding these tags.
    return re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"<em>\1</em>", escape(text))

prose = "\n".join(
    '<hr aria-label="Scene break">' if p == "***" else f"<p>{inline(p)}</p>"
    for p in paragraphs
)
page = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Dorrie rents her sense of taste to an intelligence called Thursday. Then she invites it to cook dinner. A story written with Narracode.">
  <title>Mouth on Loan — Narracode</title>
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
    .intro { font-size: 1.1rem; line-height: 1.6; }
    details { margin-top: 1.5rem; font: 14px/1.7 system-ui, sans-serif; }
    summary { cursor: pointer; color: #644426; }
    details h3 { font-size: .9rem; margin: 1.2rem 0 .4rem; }
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
      <h1>Mouth on Loan</h1>
      <p class="intro">Dorrie rents her sense of taste to an artificial intelligence. She asks it to cook her dinner for a change.</p>
      <p class="meta">September 7, 2026 · WORD_COUNT words · MINUTES min read · Draft 3</p>
      <p class="meta">David Jhave Johnston — premise, direction and substantial hand edits<br>OpenAI GPT-6 (Codex) — initial drafts, revised continuation and page · Narracode</p>
      <details>
        <summary>Read the initial prompt and writing direction</summary>
PROMPT_HTML
      </details>
    </header>
    <article aria-label="Mouth on Loan">
PROSE
    </article>
  </main>
  <footer>
    <p>Draft 3 retains the author’s revised opening and first three scenes, with limited copy corrections, and continues from that hand edit. Earlier versions and review notes are preserved.</p>
    <nav aria-label="Story files">
      <a href="drafts/3-mouth-on-loan.md">Plain-text draft</a>
      <a href="drafts/2-the-mouth-on-loan.md">Author’s hand-edited draft 2</a>
      <a href="POETICS.md">Poetics</a>
      <a href="ATTRIBUTION.md">Attribution</a>
      <a href="critiques/check-3-mouth-on-loan.md">Draft review</a>
      <a href="versions/v5-2026-09-07-hand-edit-continuation/loop-notes.md">Version notes</a>
    </nav>
  </footer>
</body>
</html>
"""
page = page.replace("PROMPT_HTML", prompt_html)
page = page.replace("WORD_COUNT", f"{word_count:,}").replace("MINUTES", str(minutes)).replace("PROSE", prose)
(HERE / "index.html").write_text(page)
print(f"Rendered {word_count:,} words; {minutes} min read.")
