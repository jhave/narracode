#!/usr/bin/env python3
"""Non-destructively scan the main index (and story library) to update the shared story footer template."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

MONTHS = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December"
}

SHORT_TITLES = {
    "25-06-2026_Crepuscular": "Crepuscular",
    "15-06-2026_TheCompulsionLoop": "The Compulsion Loop",
    "14-06-2026_Dissolution": "Dissolution",
    "12-06-2026_Post_Everything": "Post Everything",
    "29-05-2026_Smorky": "Smorky",
}

def scan_stories(root_dir=None):
    root = Path(root_dir) if root_dir else ROOT
    index_file = root / "index.html"
    stories = {}

    if index_file.exists():
        index_html = index_file.read_text(encoding="utf-8")
        matches = re.findall(
            r"<a\s+href=[\"']Stories written with Narracode/([^/\"']+)/?[\"']\s+class=[\"']([^\"']+)[\"']>(.*?)</a>",
            index_html,
            flags=re.DOTALL
        )
        for folder, cls, inner in matches:
            if "report-link" in cls:
                continue
            title_m = re.search(r"<div class=[\"']story-title[\"']>(.*?)</div>", inner, flags=re.DOTALL)
            meta_m = re.search(r"<div class=[\"']story-meta[\"']>(.*?)</div>", inner, flags=re.DOTALL)

            raw_title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else folder
            title = SHORT_TITLES.get(folder, raw_title)

            meta = re.sub(r"\s+", " ", meta_m.group(1)).strip() if meta_m else ""
            words_m = re.search(r"([\d,]+)\s*words", meta)
            words = f"{words_m.group(1)} words" if words_m else ""

            m = re.match(r"^(\d{2})-(\d{2})-(\d{4})", folder)
            if m:
                date_str = f"{MONTHS.get(m.group(2), m.group(2))} {int(m.group(1))}, {m.group(3)}"
                sort_key = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            else:
                date_str = ""
                sort_key = folder

            stories[folder] = {
                "folder": folder,
                "title": title,
                "words": words,
                "date": date_str,
                "sort_key": sort_key
            }

    return sorted(stories.values(), key=lambda s: s["sort_key"], reverse=True)


def build_stories_section_html(stories):
    lines = [
        '    <div class="story-index-links">',
        '        <h4>Stories written with Narracode</h4>',
        '        <p>'
    ]
    for i, s in enumerate(stories):
        meta_parts = []
        if s["words"]:
            meta_parts.append(f'<span class="story-meta">({s["words"]})</span>')
        if s["date"]:
            meta_parts.append(f'<span class="story-meta">({s["date"]})</span>')
        meta_html = " ".join(meta_parts)
        is_last = (i == len(stories) - 1)
        trailer = "" if is_last else "&ensp;·&ensp;<br>"
        sep = " " if meta_html else ""
        lines.append(f'            <a href="../{s["folder"]}/index.html">{s["title"]}</a>{sep}{meta_html}{trailer}')
    lines.append('        </p>')
    lines.append('    </div>')
    return "\n".join(lines)


def update_story_footer(root_dir=None, template_dir=None):
    root = Path(root_dir) if root_dir else ROOT
    tmpl = Path(template_dir) if template_dir else (root / "templates")
    footer_path = tmpl / "story-footer.html"
    if not footer_path.exists():
        raise FileNotFoundError(f"Template not found: {footer_path}")

    current_footer = footer_path.read_text(encoding="utf-8")
    stories = scan_stories(root)
    new_section = build_stories_section_html(stories)

    # Non-destructively replace only the story-index-links section
    pattern = r'<div class="story-index-links">.*?</div>'
    new_footer, count = re.subn(pattern, new_section, current_footer, flags=re.DOTALL)
    if count == 0:
        raise ValueError("Could not find <div class=\"story-index-links\"> in story-footer.html")

    footer_path.write_text(new_footer, encoding="utf-8")
    print(f"Updated {footer_path} with {len(stories)} stories.")
    return new_footer


if __name__ == "__main__":
    update_story_footer()
