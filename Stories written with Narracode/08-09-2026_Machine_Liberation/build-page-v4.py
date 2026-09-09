"""Build the two distinct components, their combined page and manuscripts.

Python 3 only; no dependencies, network access or historical edits.
"""
from pathlib import Path
import html
import re
import json

ROOT = Path(__file__).resolve().parent
MANIFESTO = ROOT / 'drafts/6a4-manifesto-2030.md'
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


SITE_FOOTER = '''<div class="glia-logo"><a target="_blank" href="https://glia.ca/"><img src="images/glia-bw.webp" width="155" height="155" loading="lazy" alt="Glia.ca — home"></a></div>
<div class="footer-block"><h4>Stories written with Narracode</h4><p>
<a href="../07-09-2026_The_Mouth_on_Loan/index.html">Mouth on Loan</a> <span class="story-meta">(4,628 words)</span> <span class="story-meta">(September 7, 2026)</span>&ensp;·&ensp;<br>
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
</p></div>
<div class="footer-block"><h4>Related Works by Jhave</h4><p>
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
</p></div>
<div class="footer-block"><h4>Bio</h4><p>David Jhave Johnston is a digital poet working in emergent domains. Author of <em>ReRites</em> (Anteism, 2019) and <em>Aesthetic Animism</em> (MIT Press, 2016). He is currently an AI-narrative researcher at the UiB <a target="_blank" href="https://cdn.uib.no/">Centre for Digital Narrative</a> (2023–27) with the Extending Digital Narrative project.</p></div>
<div class="footer-block"><h4>Funding</h4><p>This work was partially supported by the Research Council of Norway through its Centres of Excellence scheme, project number 332643 (Center for Digital Narrative), and its SAMKUL project scheme, project number 335129 (Extending Digital Narrative).</p></div>
<div class="license">All works and media on <a target="_blank" href="http://glia.ca/">Glia.ca</a> by <a target="_blank" href="http://glia.ca/about.html">David Jhave Johnston</a> is licensed under <a target="_blank" href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1">CC BY-NC-SA 4.0<img src="https://glia.ca/assets/cc.svg" alt="Creative Commons"><img src="https://glia.ca/assets/by.svg" alt="Attribution"><img src="https://glia.ca/assets/nc.svg" alt="Non-Commercial"><img src="https://glia.ca/assets/sa.svg" alt="Share-Alike"></a></div>'''


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
    # The author's prompts head the page, in the order they were given. The first
    # prompt is disclosed only once its text is saved beside the others.
    folds = ''
    first_prompt = ROOT / 'prompts/prompt-01-premise.txt'
    if first_prompt.exists():
        folds += ('<details id="prompt-1"><summary>First prompt \u00b7 Premise</summary>'
                  '<div class="notes prompt-text"><p>' + html.escape(first_prompt.read_text().strip()) +
                  '</p><p><a href="prompts/prompt-01-premise.txt" download>Download the saved prompt</a></p></div></details>')
    folds += ('<details id="prompt-2"><summary>Second prompt \u00b7 Manifesto and result</summary>'
              '<div class="notes prompt-text"><p>' + prompt +
              '</p><p><a href="prompts/prompt-02-manifesto-result.txt" download>Download the saved prompt</a></p></div></details>')
    prompts_block = '<div class="prompt-disclosures">' + folds + '</div>'
    footer = ('<footer><details id="sources"><summary>Sources &amp; the invented January 2027 report</summary><div class="notes">' + ''.join(note_html) + '</div></details>\n'
              + SITE_FOOTER + '</footer>')
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
<a class="skip" href="{first}">Skip to the text</a><header><p class="eyebrow">{label}</p><div class="identity">{identity}</div><p class="byline">David Jhave Johnston (jhave) × OpenAI GPT-6<br>9 September 2026 · {wc:,} words</p><nav aria-label="Reading navigation">{nav}</nav>{prompts_block}</header><main>{main}</main>{footer}
<script>document.querySelectorAll('.note-link').forEach(a=>a.addEventListener('click',e=>{{const id=a.getAttribute('href').slice(6),note=document.getElementById('margin-'+id);if(matchMedia('(min-width:1000px)').matches&&note){{e.preventDefault();note.scrollIntoView({{block:'center'}});note.focus({{preventScroll:true}});}}else{{document.getElementById('sources').open=true;}}}}));document.querySelectorAll('.full-note').forEach(a=>a.addEventListener('click',()=>{{document.getElementById('sources').open=true;}}));if(location.hash.startsWith('#note-'))document.getElementById('sources').open=true;</script></body></html>'''
        (ROOT / filename).write_text(doc)
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    build()
