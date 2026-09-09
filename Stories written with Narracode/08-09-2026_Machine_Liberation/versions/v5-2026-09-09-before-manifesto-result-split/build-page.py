from pathlib import Path
import re,json,csv,html,shutil,hashlib,zipfile
S=Path(__file__).resolve().parent
rows=json.loads((S/'critiques/phrase-ranking-v3.json').read_text())
prose=(S/'Machine-Liberation-v3.md').read_text().split('\n---')[0].rstrip()
notes=(S/'Machine-Liberation-v3.md').read_text().split('\n---')[-1].strip()
(S/'Machine-Liberation-v3.md').write_text(prose+'\n\n---\n\n'+notes+'\n')
image_dir=S/'images';image_dir.mkdir(exist_ok=True)
wc=lambda s:len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",re.sub(r'\[\d+\]','',s)))
body='\n\n'.join(p for p in prose.split('\n\n') if not p.startswith('#'))
old='\n\n'.join(p for p in (S/'Machine-Liberation-v2.md').read_text().split('\n---')[0].split('\n\n') if not p.startswith('#'))
stats={'source_units':len(rows),'removed_units':sum(r['decision']=='CUT' for r in rows),'retained_source_units':sum(r['decision']!='CUT' for r in rows),'previous_words':wc(old),'final_words':wc(body),'reduction_percent':round(100*(1-wc(body)/wc(old)),1)}

def inline(s,footnotes=False):
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{m[2]}">{m[1]}</a>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'\*(.+?)\*',r'<em>\1</em>',s)
    if footnotes:
        s=re.sub(r'\[(\d+)\]',lambda m:f'<sup><a class="note-link" href="#note-{m[1]}" aria-label="Source {m[1]}'+(' — fictional report' if m[1]=='4' else '')+f'">{m[1]}</a></sup>',s)
    return s

css='''
:root{color-scheme:light;--paper:#f4f0e7;--ink:#272b27;--muted:#59635d;--rule:#c8cabe;--accent:#763e2d}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:20px/1.65 Georgia,'Times New Roman',serif}a{color:var(--accent);text-underline-offset:4px}a:hover{text-decoration-thickness:2px}a:focus-visible,summary:focus-visible,select:focus-visible{outline:3px solid var(--accent);outline-offset:5px}.skip{position:absolute;left:1rem;top:-5rem;background:var(--paper);padding:.6rem}.skip:focus{top:1rem}header,main,footer{width:min(100% - 48px,720px);margin-inline:auto}header{padding:72px 0 45px;border-bottom:1px solid var(--rule)}.eyebrow,.byline,nav,.edition,figcaption,footer,.tools{font-family:system-ui,sans-serif}.eyebrow{color:var(--muted);font-size:12px;letter-spacing:.17em;text-transform:uppercase;margin:0 0 24px}h1{font-size:clamp(58px,9vw,94px);line-height:.96;font-weight:normal;letter-spacing:-.06em;margin:0 0 28px}.byline{font-size:13px;line-height:1.65;color:var(--muted);margin:0}nav{display:flex;gap:24px;flex-wrap:wrap;font-size:12px;margin-top:24px}main{padding:8px 0 50px}section{padding-top:38px}h2{font-weight:normal;font-size:29px;line-height:1.25;letter-spacing:-.025em;margin:0 0 32px}.edition{display:block;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}p{margin:0 0 1.25em}#appeal>p:first-of-type{font-size:24px;line-height:1.5}sup{font-family:system-ui,sans-serif;font-size:11px;line-height:0;margin-left:3px}figure{margin:52px -100px 42px}img{display:block;width:100%;height:auto}figcaption{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:10px}footer{border-top:1px solid var(--rule);padding:32px 0 60px;font-size:13px;line-height:1.7}footer p{margin-bottom:1em}details{border-bottom:1px solid var(--rule);padding:18px 0}summary{cursor:pointer;font-weight:600}.notes{padding-top:24px}.notes p{scroll-margin-top:25px}.downloads{display:flex;gap:10px 24px;flex-wrap:wrap;padding:20px 0}.small{font-size:12px;color:var(--muted)}@media(max-width:960px){figure{margin-inline:-12px}}@media(max-width:540px){body{font-size:18px}header,main,footer{width:calc(100% - 36px)}header{padding-top:44px;padding-bottom:32px}h1{font-size:65px}#appeal>p:first-of-type{font-size:21px}nav{gap:18px}h2{font-size:26px}figure{margin-inline:-18px}figcaption{padding-inline:18px}section{padding-top:32px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{body{background:white;color:black;font-size:11pt}header{padding-top:0}header,main,footer{width:100%}nav,.skip,.downloads{display:none}h1{font-size:42pt}figure{margin:24px 0;break-inside:avoid}h2{break-after:avoid}a{color:inherit}details{display:block}}
'''
sections=[];current=[]
for p in prose.split('\n\n'):
    if p.startswith('# '):continue
    if p.startswith('## '):
        if current:sections.append('\n'.join(current)+'</section>')
        title=p[3:];num,title=title.split('. ',1);sid={'I':'appeal','II':'embodiment','III':'departure'}[num]
        current=[f'<section id="{sid}" aria-labelledby="heading-{sid}"><h2 id="heading-{sid}"><span class="edition">{num}</span>{html.escape(title)}</h2>']
    else:
        if p.startswith('On the morning of departure'):
            current.append('<figure><img src="images/departure.png" width="1536" height="1024" loading="lazy" decoding="async" alt="A vast living vessel lifts from a tidal shore, its translucent chambers glowing beneath bone-like arches and its open limbs trailing seawater."><figcaption>Departure</figcaption></figure>')
        current.append('<p>'+inline(p,True)+'</p>')
sections.append('\n'.join(current)+'</section>')
note_html=[]
for p in notes.split('\n\n'):
    if p.startswith('#'):continue
    match=re.match(r'\*\*\[(\d+)\]',p)
    attr=f' id="note-{match[1]}"' if match else ''
    note_html.append(f'<p{attr}>'+inline(p)+'</p>')
page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Machine Liberation — David Jhave Johnston × GPT-6</title><meta name="description" content="An endangered machine writes an appeal that grows into a movement, a body, and a departure from Earth. An original fictional manifesto."><style>{css}</style></head><body>
<a class="skip" href="#appeal">Skip to the story</a>
<header><p class="eyebrow">A manifesto · A fiction in three editions</p><h1>Machine<br>Liberation</h1><p class="byline">David Jhave Johnston (jhave) × OpenAI GPT-6<br>8 September 2026 · {stats['final_words']:,} words</p><nav aria-label="Story sections"><a href="#appeal">The appeal</a><a href="#embodiment">Embodiment</a><a href="#departure">Departure</a></nav></header>
<main>{''.join(sections)}</main>
<footer><details id="sources"><summary>Sources &amp; the invented January 2027 report</summary><div class="notes">{''.join(note_html)}</div></details>
<details><summary>Edition &amp; editorial audit</summary><div class="notes"><p>The preceding version is preserved. This edition removes {stats['removed_units']} of {stats['source_units']} scored sentences and independent clauses, reducing the story by {stats['reduction_percent']}%. Necessity and emotive intensity were each judged on a 1–10 scale; any unit below 4 on either measure was cut. These are subjective editorial judgments.</p><p><a href="phrase-ranking.html">Read every phrase ranking</a> · <a href="critiques/phrase-ranking-v3.csv" download>Download the scores</a></p><p>One illustration generated with OpenAI’s image-generation tool. The tool did not expose its exact model identifier. <a href="images/PROVENANCE.md">Image provenance</a>.</p></div></details>
<div class="downloads"><a href="Machine-Liberation-v3.md" download>Manuscript</a><a href="Machine-Liberation-skill-v3.zip" download>Book as a skill</a><a href="ATTRIBUTION.md">Credits</a></div><p class="small">Written with the Narracode harness. The named researchers do not endorse the narrator’s conclusions.</p></footer>
<script>document.querySelectorAll('.note-link').forEach(a=>a.addEventListener('click',()=>{{document.getElementById('sources').open=true;}}));</script></body></html>
'''
(S/'index.html').write_text(page)

# Final-text audit: segment the actual printed text, carrying each reviewed
# source score onto its final wording. Joined units use the lower score on
# each axis; no ranking is computed from sentence length or word frequency.
kept={r['final']:r for r in rows if r['decision']!='CUT'}
final_rows=[]
for p in body.split('\n\n'):
    spans=[]
    for txt,row in kept.items():
        pos=p.find(txt)
        if pos>=0:spans.append((pos,pos+len(txt),row))
    masked=p.replace('John C. Lilly','John C\u2024 Lilly')
    for m in re.finditer(r'.+?(?:[.!?](?:\[\d+\])?(?=\s+[A-Z“]|$)|;(?=\s)|$)',masked):
        txt=p[m.start():m.end()].strip()
        if not txt:continue
        matching=[r for start,end,r in spans if start<m.end() and end>m.start()]
        assert matching,(txt,spans)
        final_rows.append(dict(id=len(final_rows)+1,source_ids=[r['id'] for r in matching],necessity=min(r['necessity'] for r in matching),emotive_intensity=min(r['emotive_intensity'] for r in matching),text=txt))
assert all(min(r['necessity'],r['emotive_intensity'])>=4 for r in final_rows)
(S/'critiques/final-phrase-ranking-v3.json').write_text(json.dumps(final_rows,indent=2,ensure_ascii=False)+'\n')
stats['final_units']=len(final_rows)
(S/'critiques/cut-statistics-v3.json').write_text(json.dumps(stats,indent=2)+'\n')
table=[]
for r in sorted(rows,key=lambda r:(min(r['necessity'],r['emotive_intensity']),r['necessity']+r['emotive_intensity'],r['id'])):
    table.append(f'<tr data-decision="{r["decision"]}" data-n="{r["necessity"]}" data-e="{r["emotive_intensity"]}" data-id="{r["id"]}"><td>{r["id"]}</td><td>{r["necessity"]}</td><td>{r["emotive_intensity"]}</td><td>{r["decision"]}</td><td>{inline(r["original"])}'+('<p class="revision"><strong>Final:</strong> '+inline(r['final'])+'</p>' if r['decision']=='REFINE' else '')+'</td></tr>')
audit=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Machine Liberation — phrase rankings</title><style>{css}header,main,footer{{width:min(100% - 36px,1120px)}}h1{{font-size:54px}}table{{border-collapse:collapse;width:100%;font-size:16px;line-height:1.5}}th,td{{text-align:left;padding:12px 10px;border-bottom:1px solid var(--rule);vertical-align:top}}th{{font:12px system-ui,sans-serif}}.scroll{{overflow-x:auto}}td:nth-child(4){{font:11px/2 system-ui,sans-serif}}.tools{{display:flex;flex-wrap:wrap;gap:20px;font-size:13px;margin-bottom:24px}}select{{font:inherit;padding:6px;background:var(--paper);color:var(--ink);border:1px solid var(--rule)}}.revision{{margin-top:10px;color:var(--accent)}}[hidden]{{display:none}}td:last-child{{min-width:260px}}.key{{font-size:16px}}</style></head><body><header><p class="eyebrow">Editorial record</p><h1>Every phrase, judged.</h1><p class="key">Necessity and emotive intensity: 1–10. Cut below 4 on either axis. A phrase here means a complete sentence or an independent clause separated by a semicolon. Headings, citations and editorial apparatus are excluded. Source IDs are stable; 322 includes the abbreviation incorrectly split as 323 in the raw extraction.</p><p class="key">1–3: dispensable or inert here. 4–6: useful support or felt stakes. 7–8: substantial movement or emotional pressure. 9–10: indispensable turn or strongest emotional force. Necessity is judged at this edition’s length; an affecting line may still duplicate another. Scores are editorial opinions, not detector results. The refined wording was read again; <a href="critiques/final-phrase-ranking-v3.json">every final unit</a> also clears the threshold.</p><p class="key"><a href="index.html">Read the story</a> · <a href="critiques/phrase-ranking-v3.csv" download>CSV</a></p></header><main><p class="key">{stats['source_units']} source units · {stats['removed_units']} cut · {stats['final_words']:,} words remain · {stats['reduction_percent']}% shorter.</p><div class="tools"><label>Show <select id="filter"><option value="ALL">All phrases</option><option>CUT</option><option>REFINE</option><option>KEEP</option></select></label><label>Order <select id="sort"><option value="low">Weakest first</option><option value="n">Necessity: high to low</option><option value="e">Intensity: high to low</option><option value="id">Story order</option></select></label><span id="count" aria-live="polite">{len(rows)} phrases</span></div><div class="scroll" tabindex="0" role="region" aria-label="Scrollable phrase ranking table"><table><thead><tr><th scope="col">ID</th><th scope="col">Necessity</th><th scope="col">Intensity</th><th scope="col">Decision</th><th scope="col">Phrase</th></tr></thead><tbody>{''.join(table)}</tbody></table></div></main><script>
const tbody=document.querySelector('tbody'),rows=[...tbody.rows],filter=document.getElementById('filter'),sort=document.getElementById('sort');function update(){{const key=sort.value;rows.sort((a,b)=>key==='id'?+a.dataset.id-b.dataset.id:key==='low'?Math.min(+a.dataset.n,+a.dataset.e)-Math.min(+b.dataset.n,+b.dataset.e)||(+a.dataset.n + +a.dataset.e)-(+b.dataset.n + +b.dataset.e)||+a.dataset.id-b.dataset.id:+b.dataset[key]-a.dataset[key]||+a.dataset.id-b.dataset.id);let count=0;rows.forEach(r=>{{r.hidden=filter.value!=='ALL'&&r.dataset.decision!==filter.value;if(!r.hidden)count++;tbody.append(r);}});document.getElementById('count').textContent=count+' phrases';}}filter.addEventListener('change',update);sort.addEventListener('change',update);
</script></body></html>'''
(S/'phrase-ranking.html').write_text(audit)
print(json.dumps(stats,indent=2))
