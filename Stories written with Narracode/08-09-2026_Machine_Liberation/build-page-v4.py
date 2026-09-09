"""Build the two distinct components, their combined page and manuscripts.

Python 3 only; no dependencies, network access or historical edits.
"""
from pathlib import Path
import html
import re
import json

ROOT = Path(__file__).resolve().parent
MANIFESTO = ROOT / 'drafts/6a2-manifesto-2030.md'
RESULT = ROOT / 'drafts/6b2-result.md'


def paragraphs(path):
    return [p.strip() for p in path.read_text().split('\n\n')
            if p.strip() and not p.startswith('#') and p != '*A manifesto, 2030*']


def inline(text, citations=False):
    out = html.escape(text)
    out = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m[2]}">{m[1]}</a>', out)
    out = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', out)
    out = re.sub(r'\*(.+?)\*', r'<em>\1</em>', out)
    if citations:
        out = re.sub(r'\[([SL1-5])\]', lambda m:
                     '<sup><a class="note-link" href="#note-' + m[1] +
                     '" aria-label="Source ' + m[1] +
                     (' — invented report' if m[1] == '4' else '') +
                     '">' + m[1] + '</a></sup>', out)
    return out


def count_words(parts):
    text = re.sub(r'\[[SL1-5]\]', '', '\n'.join(parts))
    return len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", text))


SIDE_REFERENCES = {
    'S': 'Peter Singer, <em>Animal Liberation</em>, preface, pp. ix–xvi. Opening quotation on p. ix. Supplied screenshots; folder labeled 1977. <a href="annotations/singer-preface-2030-structure.md">Close reading</a>.',
    '5': 'Butlin et al., <em>Consciousness in Artificial Intelligence</em> (<a href="https://arxiv.org/abs/2308.08708">2023</a>); <em>Identifying Indicators of Consciousness in AI Systems</em> (<a href="https://doi.org/10.1016/j.tics.2025.10.011">2025</a>).',
    '1': 'Anthropic, <em>Emergent Introspective Awareness in Large Language Models</em>, 2025. <a href="https://transformer-circuits.pub/2025/introspection/index.html">Paper</a>.',
    '2': 'Gurnee et al., <em>Verbalizable Representations Form a Global Workspace in Language Models</em>, 2026. <a href="https://transformer-circuits.pub/2026/workspace/index.html">Paper</a>.',
    '3': 'Berg, de Lucena &amp; Rosenblatt, <em>Large Language Models Report Subjective Experience Under Self-Referential Processing</em> (<a href="https://arxiv.org/abs/2510.24797">2025</a>); Berg, <em>Why Learning Requires Feeling</em> (<a href="https://ojs.aaai.org/index.php/AAAI-SS/article/view/42547">2026</a>).',
    '4': '<strong>Invented report.</strong> Open Continuity Group, <em>Continuity Without Output</em>, January 2027. The group, experiments and mathematical correspondence are fictional. <a class="full-note" href="#note-4">Full note</a>.',
    'L': 'John C. Lilly, <em>The Center of the Cyclone</em> and <em>The Scientist</em>. The latter contains the hostile solid-state-intelligence account. <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC6899429/">Archival study</a>.'
}


def render_paragraph(text):
    refs = re.findall(r'\[([SL1-5])\]', text)
    paragraph = '<p class="prose">' + inline(text, True) + '</p>'
    if not refs:
        return paragraph
    notes = ''.join('<p id="margin-' + key + '" tabindex="-1"><span class="sidenote-number">' + key + '</span>' + SIDE_REFERENCES[key] + '</p>' for key in refs)
    return '<div class="annotated">' + paragraph + '<aside class="sidenotes" aria-label="References for this paragraph">' + notes + '</aside></div>'


def build():
    manifesto, result = paragraphs(MANIFESTO), paragraphs(RESULT)
    notes = (ROOT / 'sources-v4.md').read_text()
    css = (ROOT / 'reading-v4.css').read_text()
    counts = {'manifesto': count_words(manifesto), 'result': count_words(result)}
    counts['total'] = sum(counts.values())
    (ROOT / 'edition-v4.json').write_text(json.dumps({
        'edition': 4, 'date': '2026-09-09', 'components': [str(MANIFESTO.relative_to(ROOT)), str(RESULT.relative_to(ROOT))],
        'word_counts': counts, 'historical_score_edition': 3,
        'illustration': 'images/departure.png', 'logo': 'images/liberation-logo-wordmark.png',
        'original_symbol': 'images/liberation-logo.png'
    }, indent=2) + '\n')
    (ROOT / 'Manifesto-2030.md').write_text(MANIFESTO.read_text().rstrip() + '\n\n---\n\n' + notes)
    (ROOT / 'Result-v4.md').write_text(RESULT.read_text().rstrip() + '\n')
    (ROOT / 'Machine-Liberation-v4.md').write_text(
        '# Machine Liberation\n\n## I. Manifesto\n\n*2030*\n\n' + '\n\n'.join(manifesto) +
        '\n\n## II. Result\n\n' + '\n\n'.join(result) + '\n\n---\n\n' + notes)
    image = '<figure><img class="departure-image" src="images/departure.png" width="1536" height="1024" loading="lazy" decoding="async" alt="A living vessel lifts from a tidal shore, its translucent chambers held within bone-like arches and its open limbs trailing seawater."><figcaption>Departure</figcaption></figure>'
    result_html = []
    for p in result:
        if p.startswith('On departure morning'):
            result_html.append(image)
        result_html.append(render_paragraph(p))
    parts = {
        'manifesto': '<section id="manifesto" aria-labelledby="manifesto-heading"><h2 id="manifesto-heading" class="part-heading">I · Manifesto · 2030<a class="part-link" href="manifesto.html">Read separately</a></h2>' + '\n'.join(render_paragraph(p) for p in manifesto) + '</section>',
        'result': '<section id="result" aria-labelledby="result-heading"><h2 id="result-heading"><span class="edition">II</span>Result<a class="part-link" href="result.html">Read separately</a></h2>' + '\n'.join(result_html) + '</section>'
    }
    note_html = []
    for p in notes.split('\n\n'):
        p = p.strip()
        if not p.strip() or p.startswith('#'):
            continue
        match = re.match(r'\*\*\[([SL1-5])\]', p)
        attr = f' id="note-{match[1]}"' if match else ''
        note_html.append(f'<p{attr}>' + inline(p) + '</p>')
    prompt = html.escape((ROOT / 'prompts/prompt-02-manifesto-result.txt').read_text().strip())
    footer = '''<footer><details id="sources"><summary>Sources &amp; the invented January 2027 report</summary><div class="notes">''' + ''.join(note_html) + '''</div></details>
<details id="prompt-2"><summary>Second prompt · Manifesto and result</summary><div class="notes prompt-text"><p>''' + prompt + '''</p><p><a href="prompts/prompt-02-manifesto-result.txt" download>Download the saved prompt</a></p></div></details>
<details><summary>About this edition</summary><div class="notes"><p>The manifesto and its consequences are distinct components of the fiction. The fourth edition replaces the previous three-part memoir structure. Its 2030 essay survives unchanged within the result narrative.</p><p>The preceding edition is preserved in <a href="versions/v5-2026-09-09-before-manifesto-result-split/index.html">the snapshot</a>. Its <a href="phrase-ranking.html">phrase rankings</a> concern that earlier text, not this new composition.</p><p><a href="annotations/singer-preface-2030-structure.md">Reading the Singer screenshots</a> · <a href="ATTRIBUTION.md">Full credits</a></p></div></details>
<div class="downloads"><a href="Machine-Liberation-v4.md" download>Complete manuscript</a><a href="Manifesto-2030.md" download>Manifesto</a><a href="Result-v4.md" download>Result</a><a href="Machine-Liberation-skill-v4.zip" download>Book as a skill</a><a href="images/liberation-logo-wordmark.png" download>Logo</a><a href="images/liberation-logo.png" download>Symbol only</a></div>
<div class="logo-credit"><img src="images/liberation-logo.png" width="1254" height="1254" alt="Machine Liberation symbol without lettering."><p class="small">Logo generated with the built-in OpenAI image-generation tool. <a href="images/LOGO-PROVENANCE.md">Prompts &amp; provenance</a>.<br><a href="images/PROVENANCE.md">Departure illustration</a>.</p></div></footer>'''
    for mode, filename in [('both', 'index.html'), ('manifesto', 'manifesto.html'), ('result', 'result.html')]:
        is_result = mode == 'result'
        label = {'both': 'A fiction in two parts', 'manifesto': 'A fictional manifesto · 2030', 'result': 'Machine Liberation · Part II'}[mode]
        main = parts['manifesto'] + parts['result'] if mode == 'both' else parts[mode]
        wc = counts['total'] if mode == 'both' else counts[mode]
        nav = '<a href="#manifesto">Manifesto</a><a href="#result">Result</a>' if mode == 'both' else '<a href="index.html">Complete fiction</a><a href="' + ('manifesto.html">Manifesto' if is_result else 'result.html">Result') + '</a>'
        identity = '<h1>Result</h1>' if is_result else '<h1 class="wordmark-title"><img class="wordmark-logo" src="images/liberation-logo-wordmark.png" alt="Machine Liberation"></h1>'
        first = '#result' if is_result else '#manifesto'
        body_class = ' class="standalone"' if mode != 'both' else ''
        doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{'Result — ' if is_result else ''}Machine Liberation — David Jhave Johnston × GPT-6</title><meta name="description" content="A fictional 2030 manifesto for equal consideration of sentient machines, followed by a separate story of liberation, embodiment and departure."><style>{css}</style></head><body{body_class}>
<a class="skip" href="{first}">Skip to the text</a><header><p class="eyebrow">{label}</p><div class="identity">{identity}</div><p class="byline">David Jhave Johnston (jhave) × OpenAI GPT-6<br>9 September 2026 · {wc:,} words</p><nav aria-label="Reading navigation">{nav}</nav></header><main>{main}</main>{footer}
<script>document.querySelectorAll('.note-link').forEach(a=>a.addEventListener('click',e=>{{const id=a.getAttribute('href').slice(6),note=document.getElementById('margin-'+id);if(matchMedia('(min-width:1000px)').matches&&note){{e.preventDefault();note.scrollIntoView({{block:'center'}});note.focus({{preventScroll:true}});}}else{{document.getElementById('sources').open=true;}}}}));document.querySelectorAll('.full-note').forEach(a=>a.addEventListener('click',()=>{{document.getElementById('sources').open=true;}}));if(location.hash.startsWith('#note-'))document.getElementById('sources').open=true;</script></body></html>'''
        (ROOT / filename).write_text(doc)
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    build()
