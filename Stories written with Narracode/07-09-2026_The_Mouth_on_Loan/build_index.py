"""Render the current draft as a standalone reading page (standard library only)."""
from pathlib import Path
from html import escape
import math
import re

HERE = Path(__file__).resolve().parent
draft = (HERE / "drafts/4-mouth-on-loan.md").read_text()
body = draft.split("\n", 1)[1].strip()
paragraphs = re.split(r"\n[ \t]*\n", body)
word_count = sum(len(p.split()) for p in paragraphs if p != "***")
minutes = math.ceil(word_count / 250)
prompt_sections = (HERE / "PROMPTS.md").read_text().strip().split("\n\n")[2:]
prompt_html = "\n".join(f"<h3>{escape(p[3:])}</h3>" if p.startswith("## ") else f"<p>{escape(p)}</p>" for p in prompt_sections)
def inline(text):
    # The story uses underscore emphasis. Escape HTML before adding these tags.
    return re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"<em>\1</em>", escape(text))

illustrations = {
    "One Friday, Thursday's owners sold it in parts.": (
        "split-tanks-v1", "Separate businesses",
        "A tablet beside laundry and an open freezer shows fermentation tanks and a small mechanical hand in two panes."),
    "On Sunday I re-fitted the ear-contact": (
        "sunday-visitor-v1", "Sunday's guest",
        "A small worn machine in an oversized brown coat carries a fruitless young plum tree into the kitchen."),
    "We watched the fingers close.": (
        "bean-retrieval-v1", "Under the fridge",
        "A tiny cleaning hand reaches from beneath the refrigerator to collect a fallen kidney bean."),
    "Body leaned forward.": (
        "bread-and-contact-v2", "Beside the salt",
        "Bread and a removed ear contact lie beside the salt; a receiver glows near a young fruitless plum tree.")
}

def figure(name, caption, alt):
    for extension in ("jpg", "png"):
        if not (HERE / "img" / f"{name}.{extension}").is_file():
            raise FileNotFoundError(f"Missing illustration: {name}.{extension}")
    return (f'<figure class="story-art inset-art"><a href="img/{name}.png" '
            f'aria-label="{escape("Open full-resolution illustration: " + caption, quote=True)}">'
            f'<img src="img/{name}.jpg" width="1536" height="1024" loading="lazy" decoding="async" '
            f'alt="{escape(alt, quote=True)}"></a><figcaption>{escape(caption)}</figcaption></figure>')

rendered = []
used = set()
for paragraph in paragraphs:
    for anchor, illustration in illustrations.items():
        if paragraph.startswith(anchor):
            if anchor in used:
                raise ValueError(f"Duplicate illustration anchor: {anchor}")
            rendered.append(figure(*illustration))
            used.add(anchor)
    rendered.append('<hr aria-label="Scene break">' if paragraph == "***" else f"<p>{inline(paragraph)}</p>")
if used != set(illustrations):
    raise ValueError(f"Missing illustration anchors: {set(illustrations) - used}")
prose = "\n".join(rendered)
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
    .story-art { margin: 0 0 2.5rem; }
    .story-art img { display: block; width: 100%; height: auto; border-radius: 3px; }
    .inset-art { margin: 2.8rem 0; }
    .story-art figcaption { margin-top: .6rem; font: 12px/1.6 system-ui, sans-serif; color: #645c50; }
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
      <p class="meta">September 7, 2026 · WORD_COUNT words · MINUTES min read · Draft 4 · Five illustrations</p>
      <p class="meta">David Jhave Johnston — premise, direction and substantial hand edits<br>OpenAI GPT-6 (Codex) — initial drafts, revised continuation and page · Narracode</p>
      <details>
        <summary>Read the initial prompt and writing direction</summary>
PROMPT_HTML
      </details>
    </header>
    <figure class="story-art">
      <a href="img/pear-inspection-v1.png" aria-label="Open Pear inspection image at full resolution">
        <img src="img/pear-inspection-v1.jpg" width="1536" height="1024" fetchpriority="high" alt="From a glistening tasting chamber, a spoon offers a pear with an open inspection hatch. A tiny lens inside the pear looks back at us; faint process diagrams curve across wet taste buds and droplets.">
      </a>
    </figure>
    <article aria-label="Mouth on Loan">
PROSE
    </article>
  </main>
  <footer>
    <p>Draft 4 preserves David Jhave Johnston’s hand-edited text through “Yes, Dorrie, I would like some bread.” with a subsequent author-requested tense pass and sentence relocation, followed by a new Codex continuation. The preceding draft and reading page are preserved in the version archive.</p>
    <p>Illustrations generated with OpenAI’s image generation tool, extending Jhave’s original visual direction. Full prompts, source images and credits are available below.</p>
    <nav aria-label="Story files">
      <a href="drafts/4-mouth-on-loan.md">Plain-text draft</a>
      <a href="versions/v6-2026-09-07-human-edit-bread/drafts/3-mouth-on-loan.md">Human-edit checkpoint</a>
      <a href="drafts/2-the-mouth-on-loan.md">Author’s hand-edited draft 2</a>
      <a href="POETICS.md">Poetics</a>
      <a href="ATTRIBUTION.md">Attribution</a>
      <a href="IMAGE-NOTES.md">Images and prompts</a>
      <a href="critiques/check-4-mouth-on-loan.md">Draft review</a>
      <a href="critiques/human-edit-analysis-03f0920.md">Reading the human edits</a>
    </nav>
  </footer>
</body>
</html>
"""
page = page.replace("PROMPT_HTML", prompt_html)
page = page.replace("WORD_COUNT", f"{word_count:,}").replace("MINUTES", str(minutes)).replace("PROSE", prose)
(HERE / "index.html").write_text(page)
print(f"Rendered {word_count:,} words; {minutes} min read.")
