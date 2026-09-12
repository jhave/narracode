"""Render the September 12 story and report; never rebuild the library or older stories."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / 'Stories written with Narracode/12-09-2026_You_inc'
REPORT = ROOT / 'plans/2026-09-12_harness-after-the-double.md'

CSS = '''
:root{color-scheme:light;--ink:#252823;--muted:#62675e;--paper:#faf9f5;--line:#d8dbd1;--accent:#3b594c}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:19px/1.75 Georgia,'Times New Roman',serif}
main{max-width:820px;margin:auto;padding:44px 28px 90px}a{color:var(--accent);text-underline-offset:4px}a:hover{color:#152f24}
nav,.meta,summary,th,.eyebrow,footer{font-family:system-ui,sans-serif}nav{font-size:14px;display:flex;gap:22px;flex-wrap:wrap;margin-bottom:54px}
h1{font-size:clamp(34px,6vw,52px);font-weight:500;line-height:1.13;letter-spacing:-.035em;margin:12px 0 22px}h2{font-size:28px;font-weight:500;line-height:1.3;margin:54px 0 20px}h3{font-size:22px}
p{margin:0 0 1.15em}.meta{font-size:13px;line-height:1.7;color:var(--muted)}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted)}
header{border-bottom:1px solid var(--line);padding-bottom:28px;margin-bottom:34px}details{border-block:1px solid var(--line);padding:17px 0;margin:30px 0;font-size:16px}summary{cursor:pointer;font-size:14px}details>div{padding-top:20px}details h1{font-size:24px}
.table-wrap{overflow:auto;margin:28px 0}table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.55}th,td{border-bottom:1px solid var(--line);padding:13px 12px;text-align:left;vertical-align:top}th{background:#eeefe8;font-size:13px}td:first-child{min-width:160px}
code{font:13px/1.6 ui-monospace,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow:auto}blockquote{margin:25px 0;padding-left:20px;border-left:2px solid var(--line)}li{margin-bottom:10px}
.story{max-width:720px}.story article{font-size:20px;line-height:1.65}.story article p{margin-bottom:1em}footer{border-top:1px solid var(--line);margin-top:50px;padding-top:22px;font-size:13px;color:var(--muted)}
:focus-visible{outline:3px solid #608775;outline-offset:5px}.skip{position:absolute;left:-9999px}.skip:focus{left:20px;top:10px;background:white;padding:10px}
@media(max-width:520px){main{padding:28px 20px 60px}nav{margin-bottom:34px}.story article{font-size:19px}h2{font-size:25px}table{min-width:620px}}
@media print{nav,.skip,details{display:none}body{background:white;font-size:12pt}main{max-width:none;padding:0}h2{break-after:avoid}.table-wrap{overflow:visible}table{min-width:0}a{color:inherit}}
'''

def inline(s, report=False):
    s=escape(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    def link(m):
        label,url=m.groups()
        if report and not re.match(r'https?://|#',url):
            url=url[3:] if url.startswith('../') else 'plans/'+url
        return f'<a href="{url}">{label}</a>'
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
    return s

def render(md, report=False):
    blocks=md.strip().split('\n\n'); out=[]
    for b in blocks:
        lines=b.splitlines()
        if lines[0].startswith('|') and len(lines)>1:
            rows=[]
            for i,l in enumerate(lines):
                if re.fullmatch(r'[| :\-]+',l):continue
                tag='th' if i==0 else 'td'
                rows.append('<tr>'+''.join(f'<{tag}>'+inline(c.strip(),report)+f'</{tag}>' for c in l.strip('|').split('|'))+'</tr>')
            out.append('<div class="table-wrap" tabindex="0" role="region" aria-label="Comparison table"><table><thead>'+rows[0]+'</thead><tbody>'+''.join(rows[1:])+'</tbody></table></div>')
        elif lines[0].startswith('#'):
            m=re.match(r'(#{1,6}) (.*)',lines[0]); level=len(m[1]); text=m[2]
            out.append(f'<h{level}>'+inline(text,report)+f'</h{level}>')
        elif all(l.startswith('- ') for l in lines):
            out.append('<ul>'+''.join('<li>'+inline(l[2:],report)+'</li>' for l in lines)+'</ul>')
        else:out.append('<p>'+inline(' '.join(lines),report)+'</p>')
    return '\n'.join(out)

def page(title,desc,body,nav,kind='report'):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — Narracode</title><meta name="description" content="{escape(desc,quote=True)}">
<meta name="author" content="David Jhave Johnston (concept and direction); GPT-6 Astra (writing and report)">
<style>{CSS}</style></head><body><a class="skip" href="#content">Skip to content</a><main class="{kind}">
<nav aria-label="Publication navigation">{nav}</nav><div id="content">{body}</div>
<footer>David Jhave Johnston · GPT-6 Astra · September 12, 2026<br><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a></footer>
</main></body></html>'''

story= (STORY/'drafts/1-the-appointment.md').read_text()
bodytext=story.split('\n\n',1)[1]
words=len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*",bodytext))
minutes=(words+249)//250
body=f'''<header><div class="eyebrow">You.inc · A story</div><h1>The Appointment</h1>
<p class="meta">Concept and direction: David Jhave Johnston<br>Story written by GPT-6 Astra, without running the Narracode recursive harness<br>September 12, 2026 · {words:,} words · {minutes} min read</p></header>
<article aria-label="The Appointment">{render(bodytext)}</article>
<details><summary>Attribution and composition record</summary><div>{render((STORY/'ATTRIBUTION.md').read_text()).replace('<h1>', '<h2>').replace('</h1>', '</h2>')}<p><a href="POETICS.md">Preparation notes</a> · <a href="drafts/1-the-appointment.md">Original Markdown draft</a></p></div></details>
<p><a href="../../2026-09-12_harness-after-the-double.html">Read the accompanying report: After the Double</a></p>'''
(STORY/'index.html').write_text(page('The Appointment','An observer meets their AI AR double at You.inc, Aldea, Bergen, August 2027.',body,'<a href="../../index.html">← Narracode library</a><a href="../../2026-09-12_harness-after-the-double.html">Harness report</a>','story'))
report=REPORT.read_text()
body=render(report,True)
nav='<a href="index.html">← Narracode library</a><a href="Stories%20written%20with%20Narracode/12-09-2026_You_inc/">Read the story</a><a href="plans/2026-09-12_harness-after-the-double.md">Report Markdown</a>'
(ROOT/'2026-09-12_harness-after-the-double.html').write_text(page('After the Double: What I Need from a Harness','GPT-6 Astra assesses Narracode, current frontier capabilities, instruction reduction, and a compact candidate protocol.',body,nav))
print(f'Story: {words} words, {minutes} minutes. Rendered story and report.')
