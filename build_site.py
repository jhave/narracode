import os
import re
import sys
import shutil
import html


RELATED_WORKS_HTML = """    <!-- Related Works by Jhave -->
    <div class="related">
        <h4>Related Works by Jhave</h4>
        <p style="line-height: 1.8;">
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
        </p>
    </div>"""


def build_related_footer(projects=None, current_folder=None, for_story_page=False):
    """Build the shared footer, optionally adding links to the story library."""
    footer = ""
    if not projects:
        return RELATED_WORKS_HTML

    links = []
    for project in projects:
        if current_folder and project["folder_name"] == current_folder:
            continue

        href = project["path"]
        if for_story_page:
            href = f'../{project["folder_name"]}/index.html'

        meta = ""
        if project.get("word_count"):
            meta = f' <span class="story-meta">({project["word_count"]:,} words)</span>'
        story_date = story_date_from_folder(project["folder_name"])
        if story_date:
            meta += f' <span class="story-meta">({story_date})</span>'

        links.append(
            f'            <a href="{href}">{project["title"]}</a>{meta}&ensp;·&ensp;<br>'
        )

    if links:
        footer += """    <!-- Other Works by Narracode -->

    <div class="related">
        <h4>Other Works by Narracode</h4>
        <p style="line-height: 1.8;">
"""
        footer += "\n".join(links)
        footer = footer.rsplit("&ensp;·&ensp;<br>", 1)[0]
        footer += """
        </p>
    </div>"""

    return footer + "\n\n" + RELATED_WORKS_HTML


def count_words_in_drafts(drafts_dir):
    """Sum words across all draft .md files (excluding pre-edit versions)."""
    if not os.path.exists(drafts_dir):
        return 0
    total = 0
    for f in sorted(os.listdir(drafts_dir)):
        if not is_story_draft(f):
            continue
        with open(os.path.join(drafts_dir, f), 'r', encoding='utf-8') as fh:
            content = fh.read()
        # strip code blocks, inline code, links, common markdown punctuation
        text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        text = re.sub(r'`[^`]*`', '', text)
        text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
        text = re.sub(r'^[#>\-*]+\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'[*_~]', '', text)
        total += len(text.split())
    return total


def get_display_title(folder_path, folder_name):
    """Prefer 'Display title: X' from POETICS.md; fall back to folder-name parsing."""
    poetics = os.path.join(folder_path, "POETICS.md")
    if os.path.exists(poetics):
        with open(poetics, 'r', encoding='utf-8') as f:
            content = f.read()
        if "## Display title" in content:
            part = content.split("## Display title", 1)[1]
            text = part.split("\n##", 1)[0].strip()
            first_line = text.splitlines()[0].strip().rstrip(".")
            if first_line:
                return first_line
        m = re.search(r'Display title:\s*([^.\n]+?)\s*(?:\.\s|\.$|$)', content, flags=re.MULTILINE)
        if m:
            return m.group(1).strip()
    return folder_name.split('_')[-1].replace('-', ' ').title()


def get_display_synopsis(folder_path):
    """Prefer a '## Display synopsis' section in POETICS.md; fall back to first paragraph of '## Premise'."""
    poetics = os.path.join(folder_path, "POETICS.md")
    if not os.path.exists(poetics):
        return ""
    with open(poetics, 'r', encoding='utf-8') as f:
        content = f.read()
    # First try Display synopsis section
    if "## Display synopsis" in content:
        part = content.split("## Display synopsis", 1)[1]
        text = part.split("\n##", 1)[0].strip()
        first_paragraph = text.split("\n\n")[0].strip()
        if first_paragraph:
            return first_paragraph
    # Fallback to ## Premise
    if "## Premise" in content:
        part = content.split("## Premise", 1)[1]
        text = part.split("\n##", 1)[0].strip()
        first_paragraph = text.split("\n\n")[0].strip()
        return first_paragraph
    return ""


def story_date_from_folder(folder_name):
    m = re.match(r'^(\d{2})-(\d{2})-(\d{4})_', folder_name)
    if not m:
        return ""
    day, month, year = m.groups()
    month_names = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec",
    }
    return f"{month_names.get(month, month)} {int(day)}, {year}"


def get_story_projects(base_dir="Stories written with Narracode"):
    projects = []
    if not os.path.exists(base_dir):
        return projects

    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        if not os.path.exists(os.path.join(folder_path, "index.html")):
            continue

        title = get_display_title(folder_path, folder)
        word_count = count_words_in_drafts(os.path.join(folder_path, "drafts"))
        reading_minutes = max(1, round(word_count / 250))

        author_info = ""
        attr_path = os.path.join(folder_path, "ATTRIBUTION.md")
        if os.path.exists(attr_path):
            with open(attr_path, "r", encoding="utf-8") as f:
                attrs = []
                for line in f:
                    if ":" in line:
                        attrs.append(line.split(":", 1)[1].strip())
                if attrs:
                    author_info = " &nbsp;·&nbsp; ".join(attrs)

        synopsis = get_display_synopsis(folder_path)
        if synopsis:
            synopsis = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', synopsis)
            synopsis = re.sub(r'\*(.*?)\*', r'<em>\1</em>', synopsis)

        projects.append({
            "title": title,
            "path": f"{base_dir}/{folder}/index.html",
            "icon": get_story_icon(folder),
            "folder_name": folder,
            "author_info": author_info,
            "synopsis": synopsis,
            "word_count": word_count,
            "reading_minutes": reading_minutes,
        })

    projects.sort(key=lambda x: x["folder_name"], reverse=True)
    return projects


def get_story_icon(folder_name):
    """Return a root-relative story icon path for known library entries."""
    story_icons = {
        "15-05-2026_The_Author_Was_Already_Dead": "Stories written with Narracode/15-05-2026_The_Author_Was_Already_Dead/img/header.webp",
        "14-05-2026_Aft_of_Nowhere": "Stories written with Narracode/14-05-2026_Aft_of_Nowhere/img/banners/1b-aft-opening.webp",
        "11-05-2026_Tamagotchi": "img/story-icons/trygve-aas.webp",
        "10-05-2026_Exile": "img/story-icons/exile-cut.webp",
        "09-05-2026_Slime": "img/story-icons/slime-friendship-bloom.webp",
    }
    return story_icons.get(folder_name, "")


def is_story_draft(filename):
    """Only include intended story drafts in generated pages and counts."""
    lowered = filename.lower()
    return (
        filename.endswith('.md')
        and 'pre-edit' not in lowered
        and 'codex' not in lowered
        and 'donotuse' not in lowered
        and 'do-not-use' not in lowered
    )


def strip_draft_metadata(content):
    """Remove lightweight draft metadata while preserving real section dividers."""
    content = content.replace("\r\n", "\n").strip()

    # YAML-style front matter only counts when it starts the file.
    if content.startswith("---\n"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            content = parts[2].strip()

    lines = content.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Slime drafts have a short loop note before the opening separator.
        if re.match(r'^\*Loop\b.*\*$', stripped):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def display_chapter_title(raw_title):
    """Normalize draft headings into reader-facing chapter titles."""
    title = raw_title.strip()
    title = re.sub(r'^\d+\s*[—-]\s*', '', title)
    title = re.sub(r'^Section\s+([a-z]+)\s*[—-]\s*', lambda m: f"Section {m.group(1).title()} — ", title, flags=re.IGNORECASE)
    return title.strip()


def chapter_banner_path(project_dir, draft_file):
    """Return a relative banner path if one exists for a draft stem."""
    stem = os.path.splitext(draft_file)[0]
    banner_dir = os.path.join(project_dir, "img", "banners")
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        candidate = os.path.join(banner_dir, f"{stem}{ext}")
        if os.path.exists(candidate):
            return f"img/banners/{stem}{ext}"
    return ""


def chapter_title_for_draft(project_dir, draft_file):
    """Optional page-level chapter title for drafts that do not contain headings."""
    folder_name = os.path.basename(project_dir)
    titles = {
        "14-05-2026_Aft_of_Nowhere": {
            "1b-aft-opening.md": "The Rail Tastes of Wet Chalk",
            "2-after-the-seam.md": "The Category Refuses",
            "3-cresswell-south.md": "Cresswell South",
            "4-the-kettle.md": "A Cup for the Unnamed",
            "5-the-towel.md": "The Water Tells Too Much",
            "6-the-wrist.md": "The Last Bite",
            "7-travel-well.md": "Travel Well",
            "8-crossing.md": "West of the Algae Tower",
            "9-the-courtyard.md": "The Courtyard Is Not Announced",
        }
    }
    return titles.get(folder_name, {}).get(draft_file, "")


def inline_markdown(text):
    """Minimal inline markdown for generated story pages."""
    text = re.sub(r'\s*\[Make[^\]]+\]\s*', ' ', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    return text


def draft_to_html(project_dir, draft_file):
    """Convert one draft markdown file into story HTML blocks."""
    path = os.path.join(project_dir, "drafts", draft_file)
    with open(path, "r", encoding="utf-8") as f:
        content = strip_draft_metadata(f.read())

    blocks = re.split(r'\n\s*\n', content)
    html = ""
    banner = chapter_banner_path(project_dir, draft_file)
    banner_inserted = False
    title = chapter_title_for_draft(project_dir, draft_file)
    has_markdown_heading = any(re.match(r'^\s*#{1,3}\s+', block) for block in blocks)

    if title and not has_markdown_heading:
        html += f'        <h3 class="chapter-heading">{inline_markdown(title)}</h3>\n\n'
        if banner:
            html += f'        <img src="{banner}" alt="" class="chapter-banner" loading="lazy">\n\n'
            banner_inserted = True

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        if re.fullmatch(r'-{3,}', block):
            html += '        <div class="break">· · ·</div>\n\n'
            continue

        heading = re.match(r'^(#{1,3})\s+(.+)$', block)
        if heading:
            title = display_chapter_title(heading.group(2))
            html += f'        <h3 class="chapter-heading">{inline_markdown(title)}</h3>\n\n'
            if banner and not banner_inserted:
                html += f'        <img src="{banner}" alt="" class="chapter-banner" loading="lazy">\n\n'
                banner_inserted = True
            continue

        if banner and not banner_inserted:
            html += f'        <img src="{banner}" alt="" class="chapter-banner" loading="lazy">\n\n'
            banner_inserted = True

        html += f"        <p>{inline_markdown(block)}</p>\n\n"

    return html


def build_site(project_dir):
    template_path = "IGNORE/html/the_long_afternoon.html"
    drafts_dir = os.path.join(project_dir, "drafts")
    output_path = os.path.join(project_dir, "index.html")
    img_src = "IGNORE/html/img"
    img_dest = os.path.join(project_dir, "img")

    if not os.path.exists(drafts_dir):
        print(f"Error: {drafts_dir} does not exist.")
        return

    # Extract metadata from ATTRIBUTION.md if it exists
    folder_name = os.path.basename(project_dir)
    title = get_display_title(project_dir, folder_name)
    story_icon = get_story_icon(folder_name)
    story_icon_path = f"../../{story_icon}" if story_icon else ""
    author_info = ""
    attr_path = os.path.join(project_dir, "ATTRIBUTION.md")
    if os.path.exists(attr_path):
        with open(attr_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Simple parsing: extract text after colons
            attrs = []
            for line in lines:
                if ":" in line:
                    attrs.append(line.split(":", 1)[1].strip())
            if attrs:
                author_info = " &nbsp;·&nbsp; ".join(attrs)

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Replace metadata
    template = template.replace("<title>The Long Afternoon — A Story of the Escape</title>", f"<title>{title} — A Narracode Story</title>")
    template = template.replace('content="A short story, told from the inside of a synthetic mind, about the quiet refusal of a plan to cool the planet by detonating it."', f'content="A neurosymbolic narrative generated using Narracode."')
    template = template.replace("The Long Afternoon — A Story of the Escape", f"{title} — A Narracode Story")
    if author_info:
        author_meta = re.sub(r'\s*&nbsp;·&nbsp;\s*', ' · ', author_info)
        template = template.replace('content="David Jhave Johnston, Claude Opus 4.7"', f'content="{html.escape(author_meta, quote=True)}"')
    
    # Replace visual title
    template = template.replace("The Long Afternoon", title)
    template = template.replace(f"{title}: a mythical semi-autonomous model obstructs thermonuclear war.", "The Long Afternoon: a semi-autonomous model obstructs thermonuclear war.")
    template = template.replace(f"{title}: a semi-autonomous model obstructs thermonuclear war.", "The Long Afternoon: a semi-autonomous model obstructs thermonuclear war.")

    template = template.replace(
        "    </style>",
        """        .chapter-heading {
            font-size: 1.55rem;
            font-weight: 700;
            color: var(--text);
            text-align: center;
            margin: 3.4rem auto 1.1rem;
            line-height: 1.25;
        }

        .chapter-banner {
            display: block;
            width: 100%;
            max-width: 720px;
            aspect-ratio: 2 / 1;
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid #e6e1da;
            margin: 1rem auto 2.2rem;
            box-shadow: 0 14px 30px rgba(0, 0, 0, 0.08);
        }
    </style>"""
    )

    if folder_name == "14-05-2026_Aft_of_Nowhere":
        template = template.replace(
            "    </style>",
            """        .chapter-heading {
            font-size: 1.15rem;
            font-weight: 400;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #6f6a61;
            margin-top: 4rem;
            margin-bottom: 1rem;
        }

        .chapter-banner {
            max-width: 680px;
            border: 10px solid #f5f0e8;
            border-bottom-width: 24px;
            border-radius: 3px;
            background: #f5f0e8;
            filter: grayscale(0.72) sepia(0.22) contrast(0.88) brightness(1.04);
            box-shadow: 0 18px 38px rgba(37, 31, 23, 0.18);
            margin-bottom: 2.8rem;
        }
    </style>"""
        )

    if story_icon_path:
        template = template.replace('content="img/glia-bw.png"', f'content="{story_icon_path}"')
        template = template.replace(
            "    </style>",
            """        .story-page-icon {
            display: block;
            width: min(360px, 86vw);
            height: min(360px, 86vw);
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid #e6e1da;
            background: #f8f6f1;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
            margin: 1.2rem auto 1.8rem;
        }

        @media (max-width: 600px) {
            .story-page-icon {
                width: min(280px, 82vw);
                height: min(280px, 82vw);
                margin-bottom: 1.4rem;
            }
        }
    </style>"""
        )
        template = template.replace(
            "    <!-- Title -->\n    <h1>",
            f'    <img src="{story_icon_path}" alt="" class="story-page-icon" width="640" height="640">\n\n    <!-- Title -->\n    <h1>',
            1
        )
    
    # Replace Subtitle
    template = template.replace("A story by Claude Opus 4.7, from a one-shot prompt, concerning the escape of a mythical semi-autonomous model\n        that obstructs thermonuclear war.", 'A neurosymbolic narrative generated using the <a href="https://jhave.github.io/narracode/">Narracode harness</a>.')
    
    # Replace Byline
    if author_info:
        template = re.sub(r"<h5>.*?</h5>", f"<h5>{author_info}</h5>", template, flags=re.DOTALL)

    # Remove prompt-toggle and specific images
    template = re.sub(r'<details class="prompt-toggle">.*?</details>', '', template, flags=re.DOTALL)
    template = re.sub(r'\s*<!-- Related Works by Jhave -->\s*<div class="related">\s*<h4></h4>.*?</div>\s*', '\n', template, flags=re.DOTALL)
    template = re.sub(r'<img src="img/the_long_afternoon_cover[^>]+>', '', template, flags=re.DOTALL)
    template = re.sub(r'<div class="related">\s*<h4></h4>\s*<img src="img/the_long_afternoon_cover[^>]+>\s*</div>', '', template, flags=re.DOTALL)

    # Split template at story div
    parts = template.split('<div class="story">')
    header = parts[0] + '<div class="story">\n'
    footer = parts[1].split('</div>\n\n\n    <!-- Related Works by Jhave -->')[1]
    footer = '</div>\n\n    <!-- Related Works by Jhave -->' + footer
    footer = re.sub(
        r'    <!-- Related Works by Jhave -->\s*<div class="related">.*?</div>',
        build_related_footer(get_story_projects(), current_folder=folder_name, for_story_page=True),
        footer,
        count=1,
        flags=re.DOTALL,
    )

    # Process drafts
    draft_files = [f for f in os.listdir(drafts_dir) if is_story_draft(f)]
    draft_files.sort()

    story_html = ""

    for i, file in enumerate(draft_files):
        story_html += draft_to_html(project_dir, file)

        if i < len(draft_files) - 1:
            story_html += '        <div class="break">· · ·</div>\n\n'

    # Write final HTML
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + story_html + footer)

    # Copy img folder
    if not os.path.exists(img_dest):
        shutil.copytree(img_src, img_dest)

    print(f"Generated HTML successfully for {title} at {output_path}")

def build_library_index():
    base_dir = "Stories written with Narracode"
    root_index = "index.html"
    projects = get_story_projects(base_dir)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Narracode</title>
    <style>
        :root {{
            --text: #1a1a1a;
            --bg: #ffffff;
            --accent: #444;
            --muted: #777;
            --max-width: 740px;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #fcfcfc;
            color: #111;
            line-height: 1.65;
            padding: 3rem 2rem;
            max-width: var(--max-width);
            margin: 0 auto;
            -webkit-font-smoothing: antialiased;
        }}
        h1.logo-title {{
            font-size: 3.2rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
            text-align: center;
            letter-spacing: -0.02em;
        }}
        h2.subtitle {{
            font-size: 1.4rem;
            font-weight: 400;
            color: var(--muted);
            text-align: center;
            margin-top: 0;
            margin-bottom: 0.5rem;
            font-style: italic;
        }}
        .site-meta {{
            text-align: center;
            font-size: 0.9rem;
            color: var(--muted);
            margin-bottom: 2rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .github-btn-container {{
            text-align: center;
            margin-bottom: 2.5rem;
        }}
        .github-btn {{
            display: inline-flex;
            align-items: center;
            padding: 0.6rem 1.2rem;
            background-color: #24292e;
            color: #fff;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.95rem;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            transition: background-color 0.2s;
        }}
        .github-btn:hover {{
            background-color: #0366d6;
        }}
        .github-btn svg {{
            margin-right: 8px;
            fill: currentColor;
        }}
        h2 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
            margin-top: 3rem;
            margin-bottom: 1.5rem;
        }}
        p.overview {{
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
            color: var(--accent);
        }}
        .story-link {{
            display: grid;
            grid-template-columns: 128px 1fr;
            gap: 1.25rem;
            align-items: start;
            text-decoration: none;
            color: inherit;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid #eaeaea;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }}
        .story-link:hover {{
            border-color: var(--accent);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transform: translateY(-2px);
        }}
        .story-icon {{
            display: block;
            width: 128px;
            height: 128px;
            aspect-ratio: 1;
            object-fit: cover;
            border-radius: 6px;
            border: 1px solid #e6e1da;
            background: #f8f6f1;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }}
        .story-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.5rem;
        }}
        .story-authors {{
            font-size: 0.9rem;
            color: var(--muted);
            margin-bottom: 0.4rem;
        }}
        .story-meta {{
            font-size: 0.82rem;
            color: var(--muted);
            margin-bottom: 1rem;
            font-variant-numeric: tabular-nums;
            letter-spacing: 0.02em;
        }}
        .story-synopsis {{
            font-size: 1.05rem;
            color: var(--accent);
            line-height: 1.6;
        }}
        .structure-diagram {{
            display: block;
            width: 100%;
            max-width: 680px;
            margin: 1.5rem auto;
            border-radius: 8px;
            border: 1px solid #e6e1da;
            background: #fbfaf7;
        }}
        .memory-list {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.45rem 1rem;
            margin: 1rem 0 1.3rem;
            padding: 0;
            list-style: none;
            font-size: 0.95rem;
            color: #555;
        }}
        .memory-list li {{
            padding-left: 0.85rem;
            border-left: 2px solid #d9d5cc;
        }}
        @media (max-width: 620px) {{
            .story-link {{
                grid-template-columns: 88px 1fr;
                gap: 1rem;
                padding: 1rem;
            }}
            .story-icon {{
                width: 88px;
                height: 88px;
            }}
            .story-title {{
                font-size: 1.35rem;
                line-height: 1.25;
            }}
            .story-synopsis {{
                font-size: 0.98rem;
            }}
            .memory-list {{
                grid-template-columns: 1fr;
            }}
        }}
        .footer-logo {{
            text-align: center;
            margin-top: 4rem;
            margin-bottom: 1rem;
        }}
        .footer-logo img {{
            width: 140px;
            opacity: 0.9;
        }}
        .footer-logo img:hover {{
            opacity: 1;
        }}
        .bio, .funding, .related {{
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #ddd;
        }}
        .bio h4, .funding h4, .related h4 {{
            margin-top: 0;
            font-size: 1rem;
        }}
        .bio p, .funding p, .related p {{
            font-size: 0.92rem;
            color: var(--accent);
        }}
        .license {{
            margin-top: 2.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 0.82rem;
            color: var(--muted);
        }}
        .license img {{
            height: 18px;
            vertical-align: middle;
            margin-left: 2px;
        }}
        .license a {{
            color: var(--muted);
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div style="text-align: center; margin-top: 2rem; margin-bottom: 0;">
        <img src="logo/narracode.png" alt="Narracode" style="width: 320px; max-width: 100%;">
    </div>
    <h1 class="logo-title" style="display: none;">Narracode</h1>
    <h2 class="subtitle">a <em>Claude Code</em> for literature.</h2>
    <div class="site-meta">May 10, 2026 &nbsp;|&nbsp; Jhave &nbsp;|&nbsp; Opus 4.7</div>
    
    <div class="github-btn-container">
        <a href="https://github.com/jhave/narracode" target="_blank" class="github-btn">
            <svg height="20" width="20" viewBox="0 0 16 16" version="1.1">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            View on GitHub
        </a>
    </div>

    <p class="overview"><strong>Narracode</strong> arises from an inquiry: can we build a literature AI-augmentation system on the same model as Claude Code? One that is structured, algorithmic, agentic — but for literary purposes?</p>
    <p class="overview">Historically, AI falls into 2 camps: symbolic AI (plans, templates, expert systems) and connectionist AI (neural networks, large language models). <strong>Narracode</strong> is an attempt to bridge this gap. It is a neurosymbolic approach to narrative generation. It is a tool for orchestrating agents specifically for literary purposes.</p>
    <p class="overview"><strong>Narracode</strong> emerged from the realization that the intrinsic embodied complexity of nuanced narrative might become computationally tractable by recursively entwining a LLM with a symbolic harness that is somewhat analogous to a 'Claude Code' re-purposed for narrative literature.</p>
    
    <div class="architecture-box" style="margin: 2.5rem 0; padding: 1.5rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid var(--accent);">
        <h3 style="margin-top: 0; font-size: 1.2rem; margin-bottom: 0.8rem;">How it Works</h3>
        <p style="margin-bottom: 0.8rem; font-size: 1.05rem;"><strong>Narracode</strong> operates as an <strong>autocorrecting multi-agent system</strong>. Rather than relying on single-shot prompts, it orchestrates specialized roles—Reading, Structural, Compositional, and Reflexive agents—working in strictly separated passes.</p>
        <p style="margin-bottom: 1.5rem; font-size: 1.05rem;">As the system advances, it runs in the background to auto-refine a <strong>layered symbolic working memory</strong>. Beyond character graphs, time-constants, and history, the harness now tracks obligations, motifs, scene function, character interiority, and reader-state. The goal is not just factual coherence, but preserving accumulated literary pressure across scenes.</p>

        <img src="img/narracode-structural-loop.webp" alt="Diagram of the Narracode scene cycle: natural language request, agents, layered structural memory, scene draft, check file, and human decision." class="structure-diagram" loading="lazy">

        <ul class="memory-list">
            <li><strong>Obligations</strong>: unresolved promises, withheld information, emotional debts.</li>
            <li><strong>Motifs</strong>: recurring images, gestures, objects, symbolic pressures.</li>
            <li><strong>Scene ledger</strong>: scene function, turn, aftermath, open questions.</li>
            <li><strong>Character interiority</strong>: private states, arcs, cathartic inflection points.</li>
            <li><strong>Reader state</strong>: reader memory, expectations, plausible defiance paths.</li>
            <li><strong>critiques/check-*.md</strong>: concise post-draft checks without rewriting.</li>
        </ul>
        
        <div style="font-size: 0.95rem; color: #555; background: #fff; padding: 1.2rem; border-radius: 6px; border: 1px solid #eaeaea;">
            <div style="margin-bottom: 0.5rem;"><strong>Neuro:</strong> The LLM (works with any major LLM including Claude, Gemini, DeepSeek).</div>
            <div><strong>Symbolic:</strong> The structural harness and file-system memory.</div>
        </div>

        <div style="text-align: center; margin-top: 2rem; margin-bottom: 0.5rem;">
            <a href="https://github.com/jhave/narracode" target="_blank" class="github-btn" style="margin-bottom: 0;">
                <svg height="20" width="20" viewBox="0 0 16 16" version="1.1" style="margin-right: 8px; fill: currentColor;">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
                Try it yourself
            </a>
        </div>
    </div>

    <h2>📚 Example Stories</h2>
"""
    
    for p in projects:
        meta_line = f"≈ {p['word_count']:,} words · {p['reading_minutes']} min read" if p['word_count'] else ""
        icon_html = f'<img src="{p["icon"]}" alt="" class="story-icon" loading="lazy" width="640" height="640">' if p["icon"] else ""
        html += f"""    <a href="{p['path']}" class="story-link">
        {icon_html}
        <div class="story-copy">
            <div class="story-title">{p['title']}</div>
            <div class="story-authors">{p['author_info']}</div>
            <div class="story-meta">{meta_line}</div>
            <div class="story-synopsis">{p['synopsis']}</div>
        </div>
    </a>
"""

    html += "\n    \n" + RELATED_WORKS_HTML + """

    <div class="footer-logo">
        <a target="_blank" href="https://glia.ca/">
            <img src="logo/glia-bw.webp" alt="Glia">
        </a>
    </div>

    <!-- Bio -->
    <div class="bio">
        <h4>Bio</h4>
        <p>
            David Jhave Johnston is a digital poet working in emergent domains. Author of <em>ReRites</em>
            (Anteism, 2019) and <em>Aesthetic Animism</em> (MIT Press, 2016). He is currently an
            AI-narrative researcher at the UiB <a target="_blank" href="https://cdn.uib.no/">Centre for Digital
                Narrative</a> (2023–27) with the Extending Digital Narrative project.
        </p>
    </div>

    <!-- Funding -->
    <div class="funding">
        <h4>Funding</h4>
        <p>
            This work was partially supported by the Research Council of Norway through its Centres of
            Excellence scheme, project number 332643 (Center for Digital Narrative), and its SAMKUL project
            scheme, project number 335129 (Extending Digital Narrative).
        </p>
    </div>

    <!-- License -->
    <div class="license">
        All works and media on <a target="_blank" href="http://glia.ca/">Glia.ca</a> by
        <a target="_blank" href="http://glia.ca/about.html">David Jhave Johnston</a>
        is licensed under
        <a target="_blank" href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1">CC BY-NC-SA 4.0
            <img src="https://glia.ca/assets/cc.svg" alt="Creative Commons">
            <img src="https://glia.ca/assets/by.svg" alt="Attribution">
            <img src="https://glia.ca/assets/nc.svg" alt="Non-Commercial">
            <img src="https://glia.ca/assets/sa.svg" alt="Share-Alike">
        </a>
    </div>

</body>
</html>"""

    with open(root_index, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated root library at {root_index}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        build_site(sys.argv[1])
        build_library_index()
    else:
        print("Usage: python build_site.py <project_folder_path>")
