#!/usr/bin/env python3
"""Build the standalone draft-15 reading edition; never replace index.html."""
from pathlib import Path
from html import escape
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
source = json.loads((ROOT / 'reference/draft-15-source.json').read_text())
plan = json.loads((ROOT / 'visuals/chapter-one-image-proposals.json').read_text())
generated = json.loads((ROOT / 'visuals/generated-image-prompts.json').read_text())
draft = (ROOT / 'drafts/15-chapter-one-human-cadence.md').read_text()
chunks = re.split(r'^## (.+)$', draft, flags=re.M)
sections = [(chunks[i], chunks[i+1].strip().split('\n\n')) for i in range(1, len(chunks), 2)]
assert len(sections) == len(plan['images']) == 8
e = escape
header = generated['header']
header_image = f'<figure class="header-image"><a href="{e(header["asset"])}" aria-label="View header image"><img src="{e(header["asset"])}" alt="{e(header["alt"])}" width="{header["width"]}" height="{header["height"]}" fetchpriority="high" decoding="async"></a></figure>'
source_url = source['repository'] + '/blob/' + source['commit'] + '/' + quote(source['file'])

def prompt_text(path):
    return (ROOT / path).read_text().split('```text\n', 1)[1].split('\n```', 1)[0]

nav = ''.join(f'<a href="#section-{i}"><span>{i:02}</span>{e(title.split(". ",1)[1].rsplit(", ",1)[0])}</a>' for i,(title,_) in enumerate(sections,1))
body = []
for i, ((title, paragraphs), idea) in enumerate(zip(sections, plan['images']), 1):
    place, month = title.split('. ', 1)[1].rsplit(', ', 1)
    asset = generated['images'][i-1]
    rendered = []
    for j, paragraph in enumerate(paragraphs, 1):
        rendered.append(f'<p data-prose>{e(paragraph)}</p>')
        if j == asset['after']:
            rendered.append(f'<figure class="story-image"><a href="{e(asset["asset"])}" aria-label="View image {i}: {e(asset["alt"])}"><img src="{e(asset["asset"])}" alt="{e(asset["alt"])}" width="1536" height="1024" loading="lazy" decoding="async"></a></figure>')
    prose = '\n'.join(rendered)
    body.append(f'''<section class="story-section" id="section-{i}" aria-labelledby="heading-{i}">
<header class="section-head"><span class="section-number">{i:02}</span><div><p class="month">{e(month)}</p><h2 id="heading-{i}">{e(place)}</h2></div></header>
<div class="prose">{prose}</div>
<details class="image-idea"><summary><span>Image notes {i:02}</span><strong>{e(idea['title'])}</strong></summary>
<div class="idea-body"><p class="concept">{e(idea['concept'])}</p><p>{e(idea['reason'])}</p>
<p><b>Placement</b><br>{e(idea['placement'])}</p>
<details class="production"><summary>Image prompt &amp; alternative text</summary><div><p>{e(asset['prompt'])}</p><p><b>Alternative text</b><br>{e(asset['alt'])}</p></div></details></div></details>
</section>''')

css = '''
.header-image{margin:1.8rem 0 2rem}.header-image img{display:block;width:100%;height:auto}.header-image a{display:block}
.story-image{margin:2em 0 2.2em;break-inside:avoid}.story-image img{width:100%;height:auto;display:block}.story-image a{display:block}.story-image:nth-of-type(1){clear:both}
:root{--paper:#faf8f3;--ink:#25251f;--muted:#64655c;--line:#d9d7ce;--accent:#775b35;--wash:#f0eee6;--serif:Georgia,'Times New Roman',serif;--sans:Arial,Helvetica,sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:2rem}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif)}a{color:inherit;text-underline-offset:.23em}a:hover{color:var(--accent)}button,summary{cursor:pointer}button{font:inherit}a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:5px}.skip{position:absolute;left:1rem;top:-6rem;padding:1rem;background:var(--paper);z-index:5}.skip:focus{top:1rem}
.masthead{max-width:1260px;margin:auto;padding:26px 40px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:20px;font:11px/1.5 var(--sans);letter-spacing:.15em;text-transform:uppercase}.masthead a{text-decoration:none}.masthead span{color:var(--muted)}
.layout{max-width:1260px;margin:auto;display:grid;grid-template-columns:235px minmax(0,1fr);gap:64px;padding:0 40px}.rail{align-self:start;position:sticky;top:32px;padding-top:65px;font:12px/1.5 var(--sans)}.rail-label{color:var(--muted);text-transform:uppercase;font-size:10px;letter-spacing:.15em;margin:0 0 20px}.rail nav a{display:flex;gap:15px;padding:10px 0;text-decoration:none;color:var(--muted)}.rail nav a span{font-size:10px;color:var(--accent)}.rail nav a[aria-current=true]{color:var(--ink);font-weight:bold}.rail-bottom{border-top:1px solid var(--line);margin-top:25px;padding-top:20px;color:var(--muted);font-size:11px}.rail-bottom a{display:block;margin-bottom:12px}
main{min-width:0;max-width:760px}.title{padding:62px 0 40px;border-bottom:1px solid var(--line)}.eyebrow,.month,.edition,.tools{font-family:var(--sans)}.eyebrow{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);margin:0 0 23px}h1{font-size:clamp(52px,6.5vw,86px);line-height:1.02;font-weight:400;letter-spacing:-.05em;margin:0 0 27px}.subtitle{font-style:italic;color:var(--muted);font-size:22px;margin:0 0 30px}.edition{font-size:12px;line-height:1.7;color:var(--muted);margin:0}.edition strong{color:var(--ink);font-weight:400}.tools{display:flex;align-items:center;flex-wrap:wrap;gap:12px 24px;margin-top:25px;font-size:12px}.tools button{border:1px solid var(--line);background:transparent;border-radius:0;padding:11px 14px;color:var(--ink)}.tools button:hover{border-color:var(--accent)}.tools span{font-size:11px;color:var(--muted)}
.story-section{padding-top:55px;scroll-margin-top:20px}.section-head{display:flex;gap:22px;align-items:flex-start;margin-bottom:30px}.section-number{font:12px/1.3 var(--sans);color:var(--accent);padding-top:5px}.month{font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:var(--muted);margin:0 0 8px}h2{font-size:29px;line-height:1.2;font-weight:400;letter-spacing:-.025em;margin:0}.prose{font-size:20px;line-height:1.72}.prose p{margin:0 0 1.2em;overflow-wrap:break-word}.image-idea{font-family:var(--sans);margin:30px 0 8px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:transparent}.image-idea>summary{padding:17px 0;font-size:12px;line-height:1.7}.image-idea>summary span{color:var(--muted);font-size:10px;letter-spacing:.07em;text-transform:uppercase;margin-right:14px}.image-idea>summary strong{font-weight:400}.image-idea[open]{background:var(--wash)}.image-idea[open]>summary{padding-left:17px;padding-right:17px}.idea-body{padding:0 22px 20px;font-size:13px;line-height:1.8}.idea-body p{margin:0 0 16px}.idea-body .concept{font-family:var(--serif);font-size:20px;line-height:1.55}.production{border-top:1px solid var(--line);padding-top:12px;font-size:12px}.production>div{padding-top:15px}.shared{color:var(--muted)}
.endnote{margin-top:60px;border-top:1px solid var(--line);padding:32px 0 65px;font:12px/1.8 var(--sans);color:var(--muted)}.endnote h2{font:16px/1.5 var(--serif);color:var(--ink);margin-bottom:12px}.endnote details{border-bottom:1px solid var(--line);padding:16px 0}.endnote details>div{padding-top:15px}.verbatim{white-space:pre-wrap;font:14px/1.8 var(--serif);color:var(--ink);overflow-wrap:anywhere}.back{display:inline-block;margin-top:25px;font-size:11px}.progress{position:fixed;top:0;left:0;height:2px;width:0;background:var(--accent);z-index:3;pointer-events:none}
@media(min-width:1100px){main{padding-right:30px}.prose{max-width:690px}}
@media(max-width:920px){.layout{grid-template-columns:1fr;gap:0;max-width:790px;padding:0 26px}.rail{position:static;padding-top:24px}.rail-label,.rail-bottom{display:none}.rail nav{display:flex;gap:12px 19px;flex-wrap:wrap}.rail nav a{font-size:11px;padding:3px 0;gap:5px}.title{padding-top:42px}.masthead{padding:20px 26px}main{max-width:none}}
@media(max-width:480px){.masthead{padding:18px 20px;font-size:9px;letter-spacing:.08em}.layout{padding:0 20px}.rail nav{gap:7px 14px}.rail nav a{font-size:10px}.title{padding-top:38px}h1{font-size:60px}.subtitle{font-size:20px}.prose{font-size:18px;line-height:1.72}.story-section{padding-top:42px}h2{font-size:25px}.section-head{gap:15px}.image-idea>summary strong{display:block;margin-left:14px}.idea-body{padding:0 16px 15px}.idea-body .concept{font-size:18px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:white;color:black}.masthead,.rail,.tools,.image-idea,.endnote,.progress,.skip{display:none}.layout{display:block;padding:0;max-width:none}main{max-width:none;padding:0}.title{padding:0 0 20px}h1{font-size:38pt}.title br{display:none}.subtitle{font-size:14pt}.edition{font-size:9pt}.story-section{padding-top:25px}.section-head{break-after:avoid}.prose{max-width:none;font-size:11pt;line-height:1.55}.prose p{orphans:3;widows:3}h2{font-size:18pt}@page{margin:20mm}}
'''

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chauffé, éclairé — No fixed arrangement.</title>
<meta name="description" content="No fixed arrangement. Eight Montreal sections from Chauffé, éclairé, with eight generated photographic illustrations.">
<meta name="author" content="Jhave (David Jhave Johnston); Claude Opus 5; GPT-6; Claude Opus 5.5">
<meta name="robots" content="noindex"><style>{css}</style></head>
<body id="top"><a class="skip" href="#section-1">Skip to the story</a><div class="progress" aria-hidden="true"></div>
<header class="masthead"><a href="https://jhave.github.io/narracode/">Narracode / Reading room</a><span>Chapter one · Montréal</span></header>
<div class="layout"><aside class="rail"><p class="rail-label">Eight sections</p><nav aria-label="Story sections">{nav}</nav><div class="rail-bottom"><a href="#edition-notes">Edition &amp; prompts</a><a href="index.html">Read all four chapters ↗</a><a href="{e(source_url)}">Read the source draft ↗</a><p>Generated photographic illustrations.<br>The story text is unchanged.</p></div></aside>
<main><header class="title"><p class="eyebrow">Chauffé, éclairé / Chapter one</p><h1>Chauffé,<br>éclairé</h1><p class="subtitle">No fixed arrangement.</p>
{header_image}
<p class="edition"><strong>Jhave (David Jhave Johnston) · Narracode</strong><br>Draft 15 · Human cadence · 23 September 2026</p>
<div class="tools"><button type="button" id="ideas-toggle" aria-expanded="false">Show image notes</button><span>8 sections · {len(draft.split()):,} words</span></div></header>
<article aria-label="Chauffé, éclairé, chapter one">{''.join(body)}</article>
<footer class="endnote" id="edition-notes"><h2>About this reading edition</h2>
<p>The chapter is reproduced unchanged from <a href="{e(source_url)}">draft 15</a>, fetched from the author’s linked branch. The title and subtitle follow the author’s subsequent choice. A panoramic header and eight section illustrations were made with the built-in image generation tool. These are generated images, not documentary photographs.</p>
<details><summary>Direction for the images</summary><div><p>{e(plan['direction'])}</p><p>One image per section, with occasional awkward intimacy and ordinary private habits. Full image prompts and alternative text are preserved in the notes.</p><a href="visuals/chapter-one-image-proposals.md">Open the full image notes</a></div></details>
<details><summary>Prompt — human cadence · 23 September 2026</summary><div class="verbatim">{e(prompt_text('reference/prompt-2026-09-23-human-cadence.md'))}</div></details>
<details><summary>Prompt — rhythm, appetite, drift · 23 September 2026</summary><div class="verbatim">{e(prompt_text('reference/prompt-2026-09-23-rhythm-rewrite.md'))}</div></details>
<details><summary>Attribution &amp; source</summary><div><p>Jhave (David Jhave Johnston): human direction, title selection and editorial decisions. Claude Opus 5: original story, as credited in the project. GPT-6 in Codex: draft 14. Claude Opus 5.5 in Claude Code: draft 15, as credited on the source branch. GPT-6 in the local Codex desktop app: this HTML reading edition, image direction and integration. Images: built-in image_gen tool; its underlying model version was not exposed.</p><p><a href="ATTRIBUTION.md">Full attribution</a> · <a href="drafts/15-chapter-one-human-cadence.md">Local Markdown draft</a> · <a href="{e(source_url)}">Version on GitHub</a></p><p>Source commit: {e(source['commit'])}. Source branch: {e(source['branch'])}.</p></div></details>
<a class="back" href="#top">Back to the beginning ↑</a></footer></main></div>
<script>
const ideas=[...document.querySelectorAll('.image-idea')];
const toggle=document.querySelector('#ideas-toggle');
function syncIdeas(){{const all=ideas.every(d=>d.open);toggle.textContent=all?'Hide image notes':'Show image notes';toggle.setAttribute('aria-expanded',String(all));}}
toggle.addEventListener('click',()=>{{const open=!ideas.every(d=>d.open);ideas.forEach(d=>d.open=open);syncIdeas();}});
ideas.forEach(d=>d.addEventListener('toggle',syncIdeas));
const progress=document.querySelector('.progress');
let scheduled=false;
function updateReading(){{const range=document.documentElement.scrollHeight-innerHeight;progress.style.width=(range>0?scrollY/range*100:0)+'%';let active='section-1';document.querySelectorAll('.story-section').forEach(s=>{{if(s.getBoundingClientRect().top<innerHeight*.35)active=s.id;}});document.querySelectorAll('.rail nav a').forEach(a=>{{if(a.hash==='#'+active)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');}});scheduled=false;}}
addEventListener('scroll',()=>{{if(!scheduled){{scheduled=true;requestAnimationFrame(updateReading);}}}},{{passive:true}});addEventListener('resize',updateReading);updateReading();
</script></body></html>'''
(ROOT / 'chapter-one-human-cadence.html').write_text(html)

md = ['# Chauffé, éclairé — images for chapter one', '', '**Subtitle:** No fixed arrangement.', '', '**Source:** draft 15, fetched from `' + source['branch'] + '` at `' + source['commit'] + '`.', '', plan['direction'], '', '**Generation method:** built-in image_gen tool. Underlying image model version not exposed.', '']
md += ['## Header — No fixed arrangement', '', '**Asset:** `' + header['asset'] + '`', '', '**Image prompt:** ' + header['prompt'], '', '**Alternative text:** ' + header['alt'], '']
for idea, asset in zip(plan['images'], generated['images']):
    md += [f"## {idea['section']}. {idea['place']} — {idea['title']}", '', idea['concept'], '', '**Why:** ' + idea['reason'], '', '**Placement:** ' + idea['placement'], '', '**Asset:** `' + asset['asset'] + '`', '', '**Image prompt:** ' + asset['prompt'], '', '**Alternative text:** ' + asset['alt'], '']
(ROOT / 'visuals/chapter-one-image-proposals.md').write_text('\n'.join(md))
print(f'Built chapter-one-human-cadence.html with {len(sections)} sections and {len(plan["images"])} generated images.')
