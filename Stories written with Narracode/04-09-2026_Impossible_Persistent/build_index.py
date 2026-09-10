"""Rebuild the human-edited morning chapter in the existing seven-chapter page.

Chapters 0–5 and their custom layout remain in index.html unchanged.
Run with Python 3; no dependencies or network required.
"""
from pathlib import Path
from html import escape
import re

HERE = Path(__file__).resolve().parent
SHARED = HERE.parents[1] / 'templates'
blocks = re.split(r'\n\s*\n', (HERE / 'drafts/6-morning.md').read_text().strip())
rendered = []
for block in blocks:
    block = block.strip()
    if block.startswith('#'):
        continue
    if block == '---':
        if rendered:
            rendered.append('<div class="break">§</div>')
        continue
    text = escape(block, quote=False)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    tag = 'div class="system-notice"' if re.fullmatch(r'\*\*.+\*\*', block) else 'p'
    rendered.append(f'<{tag}>{text}</{tag.split()[0]}>')
page = (HERE / 'index.html').read_text()
pattern = r'(<section class="chapter">\s*<h3 class="chapter-heading">6 — morning</h3>\s*<img[^>]+>)(.*?)(\s*</section>)'
page, count = re.subn(pattern, lambda m: m[1] + '\n\n' + '\n\n'.join('            ' + p for p in rendered) + '\n        </section>', page, flags=re.S)
assert count == 1, 'Expected exactly one morning chapter; index.html was not written.'
footer = (SHARED / 'story-footer.html').read_text()
page, count = re.subn(r'</main>.*?</body>', lambda m: '</main>\n\n    <footer>' + footer + '</footer>\n</body>', page, flags=re.S)
assert count == 1, 'Expected exactly one main element; index.html was not written.'
css = (SHARED / 'story-footer.css').read_text()
marker = '/* Shared story catalogue and acknowledgements. */'
if marker in page:
    page = re.sub(re.escape(marker) + r'.*?(?=</style>)', lambda m: css + '\n    ', page, count=1, flags=re.S)
else:
    page = page.replace('</style>', css + '\n    </style>', 1)
(HERE / 'index.html').write_text(page)
print(f'Rendered chapter 6 from the current human-edited draft ({len(rendered)} blocks).')
