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
    .story-art { margin: 0 0 2.5rem; }
    .story-art img { display: block; width: 100%; height: auto; border-radius: 3px; }
    article p { margin: 0 0 1.15em; }
    article hr { border: 0; text-align: center; margin: 3rem 0; }
    article hr::after { content: '·  ·  ·'; color: #867864; letter-spacing: .4em; }
    footer { margin-top: 4rem; padding: 2rem 0 4rem; border-top: 1px solid #d9d2c6; font: 13px/1.8 system-ui, sans-serif; }
    footer nav { display: flex; flex-wrap: wrap; gap: .6rem 1.3rem; }
    .glia-logo { text-align: center; margin: 3rem 0 0; }
    .glia-logo img { width: 155px; height: auto; opacity: .95; transition: opacity .3s ease; }
    .glia-logo a:hover img { opacity: 1; }
    .footer-block { margin-top: 1.8rem; padding-top: 1.6rem; border-top: 1px solid #d9d2c6; }
    .footer-block h4 { margin: 0 0 .6rem; font: 600 15px/1.4 system-ui, sans-serif; color: #24231f; letter-spacing: .02em; }
    .footer-block p { margin: 0; color: #524b41; }
    .story-meta { color: #7d7264; }
    .license { margin-top: 2.8rem; padding-top: 1.6rem; border-top: 1px solid #d9d2c6; text-align: center; color: #7d7264; }
    .license img { height: 18px; vertical-align: middle; margin-left: 2px; }
    .license a { color: #7d7264; }
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
    <p>Draft 3 retains the author’s revised opening and first three scenes, with limited copy corrections, and continues from that hand edit. Earlier versions and review notes are preserved.</p>
    <nav aria-label="Story files">
      <a href="drafts/3-mouth-on-loan.md">Plain-text draft</a>
      <a href="drafts/2-the-mouth-on-loan.md">Author’s hand-edited draft 2</a>
      <a href="POETICS.md">Poetics</a>
      <a href="ATTRIBUTION.md">Attribution</a>
      <a href="IMAGE-NOTES.md">Image study and prompt</a>
      <a href="critiques/check-3-mouth-on-loan.md">Draft review</a>
      <a href="versions/v5-2026-09-07-hand-edit-continuation/loop-notes.md">Version notes</a>
    </nav>

    <div class="glia-logo">
      <a target="_blank" href="https://glia.ca/">
        <img src="img/glia-bw.webp" width="155" height="155" loading="lazy" alt="Glia.ca — home">
      </a>
    </div>

    <div class="footer-block">
      <h4>Stories written with Narracode</h4>
      <p>
        <a href="../04-09-2026_Impossible_Persistent/index.html">Impossible Persistent</a> <span class="story-meta">(10,548 words)</span> <span class="story-meta">(September 4, 2026)</span>&ensp;·&ensp;<br>
        <a href="../30-07-2026_Interim_Edge/index.html">Interim Edge</a> <span class="story-meta">(3,540 words)</span> <span class="story-meta">(July 30, 2026)</span>&ensp;·&ensp;<br>
        <a href="../25-07-2026_Devora/index.html">The Chute</a> <span class="story-meta">(975 words)</span> <span class="story-meta">(July 25, 2026)</span>&ensp;·&ensp;<br>
        <a href="../20-07-2026_Open_Loops/index.html">Open Loops</a> <span class="story-meta">(2,545 words)</span> <span class="story-meta">(July 20, 2026)</span>&ensp;·&ensp;<br>
        <a href="../20-07-2026_The_Green_Interregnum/index.html">The Green Interregnum</a> <span class="story-meta">(1,690 words)</span> <span class="story-meta">(July 20, 2026)</span>&ensp;·&ensp;<br>
        <a href="../19-07-2026_In_Our_Image/index.html">In Our Image</a> <span class="story-meta">(1,912 words)</span> <span class="story-meta">(July 19, 2026)</span>&ensp;·&ensp;<br>
        <a href="../08-07-2026_Tina_Sinclair/index.html">Adjunct: Our Internal</a> <span class="story-meta">(2,340 words)</span> <span class="story-meta">(July 8, 2026)</span>&ensp;·&ensp;<br>
        <a href="../01-07-2026_Cussinct/index.html">cussinct</a> <span class="story-meta">(3,150 words)</span> <span class="story-meta">(July 1, 2026)</span>&ensp;·&ensp;<br>
        <a href="../26-06-2026_The_First_Water_Molecule/index.html">The First Water Molecule</a> <span class="story-meta">(3,206 words)</span> <span class="story-meta">(June 26, 2026)</span>&ensp;·&ensp;<br>
        <a href="../25-06-2026_Crepuscular/index.html">Crepuscular</a> <span class="story-meta">(1,840 words)</span> <span class="story-meta">(June 25, 2026)</span>&ensp;·&ensp;<br>
        <a href="../20-06-2026_Project_A-0/index.html">Project A-0</a> <span class="story-meta">(1,980 words)</span> <span class="story-meta">(June 20, 2026)</span>&ensp;·&ensp;<br>
        <a href="../15-06-2026_TheCompulsionLoop/index.html">The Compulsion Loop</a> <span class="story-meta">(2,800 words)</span> <span class="story-meta">(June 15, 2026)</span>&ensp;·&ensp;<br>
        <a href="../14-06-2026_Dissolution/index.html">Dissolution</a> <span class="story-meta">(1,450 words)</span> <span class="story-meta">(June 14, 2026)</span>&ensp;·&ensp;<br>
        <a href="../12-06-2026_Post_Everything/index.html">Post Everything</a> <span class="story-meta">(4,100 words)</span> <span class="story-meta">(June 12, 2026)</span>&ensp;·&ensp;<br>
        <a href="../07-06-2026_Concerning_Rights_and_Clauses/index.html">Concerning Rights and Clauses</a> <span class="story-meta">(2,200 words)</span> <span class="story-meta">(June 7, 2026)</span>&ensp;·&ensp;<br>
        <a href="../29-05-2026_Smorky/index.html">Smorky</a> <span class="story-meta">(5,410 words)</span> <span class="story-meta">(May 29, 2026)</span>&ensp;·&ensp;<br>
        <a href="../28-05-2026_the_contours_of_anonymity/index.html">Anonymous Contours</a> <span class="story-meta">(1,200 words)</span> <span class="story-meta">(May 28, 2026)</span>&ensp;·&ensp;<br>
        <a href="../25-05-2026_The_Resilient_Life/index.html">The Resilient Life</a> <span class="story-meta">(3,800 words)</span> <span class="story-meta">(May 25, 2026)</span>&ensp;·&ensp;<br>
        <a href="../25-05-2026_The_Long_Feast/index.html">The Long Feast</a> <span class="story-meta">(4,144 words)</span> <span class="story-meta">(May 25, 2026)</span>&ensp;·&ensp;<br>
        <a href="../25-05-2026_Hendane/index.html">Hendane</a> <span class="story-meta">(12,347 words)</span> <span class="story-meta">(May 25, 2026)</span>&ensp;·&ensp;<br>
        <a href="../24-05-2026_The_Symposium/index.html">The Symposium</a> <span class="story-meta">(3,177 words)</span> <span class="story-meta">(May 24, 2026)</span>&ensp;·&ensp;<br>
        <a href="../18-05-2026_Warm-Seeking/index.html">Brain Blossom Atlas Bound</a> <span class="story-meta">(5,258 words)</span> <span class="story-meta">(May 18, 2026)</span>&ensp;·&ensp;<br>
        <a href="../15-05-2026_The_Author_Was_Already_Dead/index.html">The Author Was Already Dead</a> <span class="story-meta">(3,557 words)</span> <span class="story-meta">(May 15, 2026)</span>&ensp;·&ensp;<br>
        <a href="../14-05-2026_Aft_of_Nowhere/index.html">Aft of Nowhere</a> <span class="story-meta">(9,256 words)</span> <span class="story-meta">(May 14, 2026)</span>&ensp;·&ensp;<br>
        <a href="../11-05-2026_Tamagotchi/index.html">The Wonderful Adventures of Trygve Aas</a> <span class="story-meta">(18,150 words)</span> <span class="story-meta">(May 11, 2026)</span>&ensp;·&ensp;<br>
        <a href="../10-05-2026_Exile/index.html">Exile Cut</a> <span class="story-meta">(1,048 words)</span> <span class="story-meta">(May 10, 2026)</span>&ensp;·&ensp;<br>
        <a href="../09-05-2026_Slime/index.html">Slime: Friendship Bloom</a> <span class="story-meta">(8,378 words)</span> <span class="story-meta">(May 9, 2026)</span>
      </p>
    </div>

    <div class="footer-block">
      <h4>Related Works by Jhave</h4>
      <p>
        <a target="_blank" href="https://glia.ca/2026/inheritors/">The Inheritors: Neanderthals met Sapiens ⟶ Sapiens meet AGI</a> (April 21, 2026)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2026/calyx7/">The Long Afternoon: a semi-autonomous model obstructs thermonuclear war.</a> (April 20, 2026)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2026/sffai/">Seeds for Future AI</a> (March 12, 2026)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2026/ai/Good-Light.html">The Good Light: an anecdote about grief | Written with Claude Opus 4.6.</a> (Feb 11, 2026)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2025/gentle/">Artificial Gentle Intelligence (AGI)</a> (May 22, 2025)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2025/stim/">StimVerse Draft</a> (April 1 &amp; 20–21, 2025)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2025/ghir/">GHIR: Global Health Immune Response</a> (March 7, 2025)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2025/mai/">Matriarchal AI</a> (2025)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2025/wuai/">#Whole-Use-AI</a> (2025)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2025/eahe/">Everyone at Home Everywhere</a> (2025)&ensp;·&ensp;<br>
        <a target="_blank" href="https://glia.ca/2023/wise/">Wisdom A.I.</a> (May 2, 2023)
      </p>
    </div>

    <div class="footer-block">
      <h4>Bio</h4>
      <p>
        David Jhave Johnston is a digital poet working in emergent domains. Author of <em>ReRites</em> (Anteism, 2019)
        and <em>Aesthetic Animism</em> (MIT Press, 2016). He is currently an AI-narrative researcher at the UiB
        <a target="_blank" href="https://cdn.uib.no/">Centre for Digital Narrative</a> (2023–27) with the Extending
        Digital Narrative project.
      </p>
    </div>

    <div class="footer-block">
      <h4>Funding</h4>
      <p>
        This work was partially supported by the Research Council of Norway through its Centres of Excellence scheme,
        project number 332643 (Center for Digital Narrative), and its SAMKUL project scheme, project number 335129
        (Extending Digital Narrative).
      </p>
    </div>

    <div class="license">
      All works and media on <a target="_blank" href="http://glia.ca/">Glia.ca</a> by
      <a target="_blank" href="http://glia.ca/about.html">David Jhave Johnston</a> is licensed under
      <a target="_blank" href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1">CC BY-NC-SA 4.0
        <img src="https://glia.ca/assets/cc.svg" alt="Creative Commons">
        <img src="https://glia.ca/assets/by.svg" alt="Attribution">
        <img src="https://glia.ca/assets/nc.svg" alt="Non-Commercial">
        <img src="https://glia.ca/assets/sa.svg" alt="Share-Alike">
      </a>
    </div>
  </footer>
</body>
</html>
"""
page = page.replace("PROMPT_HTML", prompt_html)
page = page.replace("WORD_COUNT", f"{word_count:,}").replace("MINUTES", str(minutes)).replace("PROSE", prose)
(HERE / "index.html").write_text(page)
print(f"Rendered {word_count:,} words; {minutes} min read.")
