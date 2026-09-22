"""Render only the main index from explicitly curated story/report records.

New folders never auto-publish. Add an approved entry to library.json, with an
explicit edition/report date, then run build_main_index.py. Keep card HTML here
rather than deriving it from drafts: published editorial descriptions survive.
"""
import json
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parent


def read_entries(root=ROOT):
    entries = json.loads((root / 'library.json').read_text())['entries']
    seen = set()
    for entry in entries:
        date.fromisoformat(entry['date'])
        if entry['kind'] not in ('story', 'report'):
            raise ValueError(f"Unknown entry kind: {entry['kind']}")
        href = entry['href']
        if href in seen:
            raise ValueError(f'Duplicate library entry: {href}')
        seen.add(href)
        if urlsplit(href).scheme or not (root / unquote(href)).exists():
            raise ValueError(f'Missing local library destination: {href}')
        if entry['kind'] == 'story':
            date.fromisoformat(entry['started_date'])
            if not (root / unquote(href) / 'index.html').is_file():
                raise ValueError(f'Story has no reading page: {href}')
        if f'href="{href}"' not in entry['card_html']:
            raise ValueError(f'Card destination disagrees with manifest: {href}')
    return sorted(entries, key=lambda entry: entry['date'], reverse=True)


def build_library_index(root=ROOT):
    template = (root / 'library-template.html').read_text()
    marker = '<!-- LIBRARY_CARDS -->'
    if template.count(marker) != 1:
        raise ValueError('Library template must contain exactly one card marker')
    cards = []
    for entry in read_entries(root):
        card = re.sub(r'\sdata-date="[^"]*"', '', entry['card_html'], count=1)
        card = card.replace('<a ', f'<a data-date="{entry["date"]}" ', 1)
        cards.append(card)
    output = template.replace(marker, '\n\n    '.join(cards))
    (root / 'index.html').write_text(output)
    print(f'Generated root library with {len(cards)} dated entries')


if __name__ == '__main__':
    build_library_index()
