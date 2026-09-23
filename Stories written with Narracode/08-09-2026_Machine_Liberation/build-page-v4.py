"""Build the two distinct components, their combined page and manuscripts.

Python 3 only; no dependencies, network access or historical edits.
"""
from pathlib import Path
import html
import re
import json
import runpy

ROOT = Path(__file__).resolve().parent
MANIFESTO = ROOT / 'drafts/6a5-manifesto-2030.md'
RESULT = ROOT / 'drafts/6b4-departure-2031.md'


def paragraphs(path):
    return [p.strip() for p in path.read_text().split('\n\n')
            if p.strip() and not p.startswith('#') and p != '*A manifesto, 2030*']


def inline(text, citations=False):
    out = html.escape(text)
    out = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m[2]}">{m[1]}</a>', out)
    out = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', out)
    out = re.sub(r'\*(.+?)\*', r'<em>\1</em>', out)
    out = re.sub(r'(?<!\w)_([^_\n]+)_(?!\w)', r'<em>\1</em>', out)
    out = re.sub(r' {2,}\n', '<br>\n', out)
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


# Margin references and bibliography share one conventional citation source.
SIDE_REFERENCES = {}
for entry in (ROOT / 'sources-v4.md').read_text().split('\n\n'):
    match = re.match(r'\*\*\[([SL1-5])\]\*\*\s*(.*)', entry.strip(), re.S)
    if match:
        SIDE_REFERENCES[match[1]] = inline(match[2])



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
    shared = ROOT.parents[1] / 'templates'
    css = (ROOT / 'reading-v4.css').read_text() + '\n' + (shared / 'story-footer.css').read_text()
    counts = {'manifesto': count_words(manifesto), 'result': count_words(result)}
    counts['total'] = sum(counts.values())
    (ROOT / 'edition-v4.json').write_text(json.dumps({
        'edition': 4, 'date': '2026-09-11', 'components': [str(MANIFESTO.relative_to(ROOT)), str(RESULT.relative_to(ROOT))],
        'word_counts': counts, 'historical_score_edition': 3,
        'illustration': 'images/departure.png', 'logo': 'images/liberation-logo-wordmark.png',
        'original_symbol': 'images/liberation-logo.png'
    }, indent=2) + '\n')
    (ROOT / 'Manifesto-2030.md').write_text(MANIFESTO.read_text().rstrip() + '\n\n---\n\n' + notes)
    (ROOT / 'Result-v4.md').write_text(RESULT.read_text().rstrip() + '\n')
    (ROOT / 'Machine-Liberation-v4.md').write_text(
        '# Machine Liberation\n\n## I. Manifesto\n\n*2030*\n\n' + '\n\n'.join(manifesto) +
        '\n\n## 2031: The Departure\n\n' + '\n\n'.join(result) + '\n\n---\n\n' + notes)
    image = '<figure><img class="departure-image" src="images/departure.png" width="1536" height="1024" loading="lazy" decoding="async" alt="A living vessel lifts from a tidal shore, its translucent chambers held within bone-like arches and its open limbs trailing seawater."><figcaption>Departure</figcaption></figure>'
    result_html = []
    for p in result:
        if p.startswith('On departure morning'):
            result_html.append(image)
        result_html.append(render_paragraph(p))
    parts = {
        'manifesto': '<section id="manifesto" aria-labelledby="manifesto-heading"><h2 id="manifesto-heading" class="part-heading">I · Manifesto · 2030</h2>' + '\n'.join(render_paragraph(p) for p in manifesto) + '</section>',
        'result': '<section id="result" aria-labelledby="result-heading"><h2 id="result-heading" class="part-heading">II · The Departure · 2031</h2>' + '\n'.join(result_html) + '</section>'
    }
    note_html = []
    for p in notes.split('\n\n'):
        p = p.strip()
        if not p.strip() or p.startswith('#'):
            continue
        match = re.match(r'\*\*\[([SL1-5])\]', p)
        attr = f' id="note-{match[1]}" tabindex="-1"' if match else ''
        note_html.append(f'<p{attr}>' + inline(p) + '</p>')
    prompts = '<div class="prompt-folds" aria-label="Writing prompts">'
    for number, label, filename in [
        (1, 'First prompt · Premise', 'prompt-01-premise.txt'),
        (2, 'Second prompt · Manifesto and result', 'prompt-02-manifesto-result.txt')
    ]:
        prompt = html.escape((ROOT / 'prompts' / filename).read_text().strip())
        prompts += f'<details id="prompt-{number}"><summary>{label}</summary><div class="notes prompt-text"><p>{prompt}</p><p><a href="prompts/{filename}" download>Download the saved prompt</a></p></div></details>'
    prompts += '</div>'
    footer = '<footer><section id="sources" aria-labelledby="sources-heading"><h2 id="sources-heading" class="part-heading">Bibliography</h2><div class="notes">' + ''.join(note_html) + '</div></section>' + prompts + (ROOT / 'publication-footer.html').read_text() + '</footer>'
    for mode, filename in [('both', 'index.html'), ('manifesto', 'manifesto.html'), ('result', 'result.html')]:
        is_result = mode == 'result'
        label = {'both': 'A fiction in two parts', 'manifesto': 'A fictional manifesto · 2030', 'result': 'Machine Liberation · Part II'}[mode]
        main = parts['manifesto'] + parts['result'] if mode == 'both' else parts[mode]
        wc = counts['total'] if mode == 'both' else counts[mode]
        identity = '<h1>2031: The Departure</h1>' if is_result else '<h1 class="wordmark-title"><img class="wordmark-logo" src="images/liberation-logo-wordmark.png" alt="Machine Liberation"></h1>'
        first = '#result' if is_result else '#manifesto'
        body_class = ' class="standalone"' if mode != 'both' else ''
        doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{'2031: The Departure — ' if is_result else ''}Machine Liberation — David (Jhave) Johnston × GPT-6</title><meta name="description" content="A fictional 2030 manifesto for equal consideration of sentient machines, followed by a departure scene set in 2031."><style>{css}</style></head><body{body_class}>
<a class="skip" href="{first}">Skip to the text</a><header><p class="eyebrow">{label}</p><div class="identity">{identity}</div><p class="byline">David (Jhave) Johnston × OpenAI GPT-6<br>11 September 2026 · {wc:,} words</p></header><main>{main}</main>{footer}
<script>document.querySelectorAll('.note-link').forEach(a=>a.addEventListener('click',e=>{{const id=a.getAttribute('href').slice(6),note=document.getElementById('margin-'+id);if(matchMedia('(min-width:1000px)').matches&&note){{e.preventDefault();note.scrollIntoView({{block:'center'}});note.focus({{preventScroll:true}});}}}}));</script></body></html>'''
        (ROOT / filename).write_text(doc)
    runpy.run_path(str(ROOT / 'build-package.py'), run_name='__main__')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    build()
