#!/usr/bin/env python3
"""Insert draft 15 and its eight images into the existing four-chapter page."""
from pathlib import Path
from html import escape
import re
import runpy

ROOT = Path(__file__).resolve().parent
edition = runpy.run_path(str(ROOT / 'build_chapter_one.py'))
sections, assets = edition['sections'], edition['generated']['images']
e = escape
target = ROOT / 'index.html'
page = target.read_text()
start = '<h2 class="part">Chapter One</h2>'
end = '<h2 class="part">Chapter Two</h2>'
before, rest = page.split(start, 1)
_, after = rest.split(end, 1)
chapter = [start]
for (title, paragraphs), item in zip(sections, assets):
    chapter.append(f'<section class="illustrated-section" id="section-{item["n"]}"><h3 class="chapter-heading">{e(title)}</h3>')
    for j, paragraph in enumerate(paragraphs, 1):
        chapter.append(f'<p data-prose>{e(paragraph)}</p>')
        if j == item['after']:
            chapter.append(f'<figure class="story-image"><a href="{e(item["asset"])}" aria-label="View image {item["n"]}: {e(item["alt"])}"><img src="{e(item["asset"])}" alt="{e(item["alt"])}" width="1536" height="1024" loading="lazy" decoding="async"></a></figure>')
    chapter.append('</section>')

before = before.replace('Chauffé Éclairé — A Narracode Story', 'Chauffé, éclairé — No fixed arrangement.')
before = before.replace('<h1>Chauffé Éclairé</h1>', '<h1>Chauffé, éclairé</h1>')
before = before.replace('Montreal, 2028. Eight apartments, eight turns. A short story written to a measured prosody: median sentence six words.', 'No fixed arrangement. A woman moves through temporary rooms, work and desire, from Montreal across Canada and into Europe.')
before = before.replace('Montreal, 2028. Heat included, lights included, nothing else included.', 'No fixed arrangement. Rooms, work and desire, from Montreal onward.')
before = re.sub(r'<meta name="author"\s+content="[^"]*">', '<meta name="author" content="Jhave (David Jhave Johnston); Claude Opus 5; GPT-6; Claude Opus 5.5">', before)
before = re.sub(r'<meta name="keywords"\s+content="[^"]*">', '<meta name="keywords" content="fiction, Montreal, housing, desire, gig work, Jhave, Narracode">', before)
before = re.sub(r'<h2>A neurosymbolic narrative generated using.*?</h2>', '<h2 class="subtitle">No fixed arrangement.</h2>\n    <p class="harness-note">A narrative composed with the <a href="https://jhave.github.io/narracode/">Narracode harness</a>.</p>', before, count=1, flags=re.S)
before = re.sub(r'<h5>.*?</h5>', '<h5>Jhave (direction and editorial decisions) · Claude Opus 5 · GPT-6 · Claude Opus 5.5<br>Chapter one: draft 15 · Illustrated edition, 23 September 2026<br><a href="ATTRIBUTION.md">Full attribution</a> · <a href="chapter-one-human-cadence.html">Chapter-one reading edition</a></h5>', before, count=1, flags=re.S)
before = before.replace('<summary>method — the voice engine</summary>', '<summary>method — historical voice-engine record</summary>')
before = re.sub(r'\s*<!-- generated-header -->.*?<!-- /generated-header -->', '', before, flags=re.S)
before = before.replace('<h2 class="subtitle">No fixed arrangement.</h2>', '<h2 class="subtitle">No fixed arrangement.</h2>\n<!-- generated-header -->' + edition['header_image'] + '<!-- /generated-header -->', 1)

style = '''
    <!-- illustrated-edition-style -->
    <style>
    .header-image { margin: 1.6rem 0 2rem; }
    .header-image img { display: block; width: 100%; height: auto; }
    .header-image a { display: block; }
    .story-image { margin: 2.1rem 0 2.5rem; break-inside: avoid; }
    .story-image img { width: 100%; height: auto; display: block; }
    .story-image a { display: block; }
    .illustrated-section { scroll-margin-top: 1.5rem; }
    .harness-note { text-align: center; font-size: .85rem; color: #666; margin-bottom: .8rem; }
    .subtitle { font-size: 1.3rem; margin-bottom: 1rem; }
    .revision-note { font-size: .86rem; line-height: 1.7; border-top: 1px solid #ddd; border-bottom: 1px solid #ddd; padding: 1rem 0; margin-bottom: 2rem; }
    .verbatim-prompt { white-space: pre-wrap; overflow-wrap: anywhere; }
    a:focus-visible, summary:focus-visible { outline: 2px solid #765731; outline-offset: 4px; }
    @media print { .story-image { break-inside: avoid; } .story-image img { max-height: 17cm; object-fit: contain; } }
    </style>
    <!-- /illustrated-edition-style -->
'''
before = re.sub(r'\s*<!-- illustrated-edition-style -->.*?<!-- /illustrated-edition-style -->\s*', '\n', before, flags=re.S)
before = before.replace('</head>', style + '</head>')

folds = []
for label, filename in [('rhythm, appetite, drift', 'prompt-2026-09-23-rhythm-rewrite.md'), ('human cadence', 'prompt-2026-09-23-human-cadence.md')]:
    text = edition['prompt_text']('reference/' + filename)
    folds.append(f'<details class="prompt-toggle"><summary>prompt — {label} · 23 September 2026</summary><div class="prompt-body verbatim-prompt">{e(text)}</div></details>')
notes = '''<!-- illustrated-edition-notes -->
<p class="revision-note">Chapter one uses draft 15, with eight generated photographic illustrations. Chapters two–four retain their existing text. The earlier voice-engine notes below are a historical record; their sentence limits and statistics describe the original version. <a href="visuals/chapter-one-image-proposals.md">Image notes and prompts</a>.</p>
''' + '\n'.join(folds) + '\n<!-- /illustrated-edition-notes -->\n'
before = re.sub(r'<!-- illustrated-edition-notes -->.*?<!-- /illustrated-edition-notes -->\s*', '', before, flags=re.S)
before = before.replace('<!-- Collapsible prompt -->', notes + '\n    <!-- Collapsible prompt -->', 1)
page = before + '\n'.join(chapter) + '\n\n        ' + end + after
page = re.sub(r'<div class="story-meta">.*?</div>', '''<div class="story-meta"><p>Begun 23 August 2026. Chapter one revised in draft 15 and illustrated on 23 September 2026. Title and subtitle selected by Jhave. Images generated with the built-in image_gen tool; they are fictional illustrations, not documentary photographs. Image model version was not exposed. <a href="ATTRIBUTION.md">Attribution</a> · <a href="visuals/generated-image-prompts.json">Generation prompts</a>.</p></div>''', page, count=1, flags=re.S)
target.write_text(page)
print('Updated index.html: draft 15, eight images, accepted title/subtitle and revision folds; later chapter text preserved.')
