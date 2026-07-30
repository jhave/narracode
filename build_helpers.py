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
    draft_files = [f for f in os.listdir(drafts_dir) if is_story_draft(f)]
    draft_files.sort(key=lambda fn: int(re.match(r'^(\d+)', fn).group(1)) if re.match(r'^(\d+)', fn) else 9999)
    for f in draft_files:
        with open(os.path.join(drafts_dir, f), 'r', encoding='utf-8') as fh:
            content = strip_draft_metadata(fh.read())
        # strip code blocks, inline code, links, common markdown punctuation
        text = re.sub(r'```.*?```', ' ', content, flags=re.DOTALL)
        text = re.sub(r'`[^`]*`', ' ', text)
        text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
        text = re.sub(r'^[#>\-*]+\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'[*_~]', '', text)
        total += len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", text))
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
    metadata_path = os.path.join(base_dir, "metadata.md")
    projects = []
    if not os.path.exists(metadata_path):
        print(f"Warning: {metadata_path} not found.")
        return projects

    with open(metadata_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by the "- **Folder**:" or "- **Draft Folder**:" marker
    blocks = re.split(r'-\s*\*\*(?:Draft\s+)?Folder\*\*\:\s*', content)
    for block in blocks[1:]:  # skip the header block
        lines = block.splitlines()
        if not lines:
            continue
        
        folder_name = lines[0].strip()
        proj = {
            "folder_name": folder_name,
            "title": "",
            "author_info": "",
            "word_count": 0,
            "reading_minutes": 0,
            "synopsis": "",
            "path": f"{base_dir}/{folder_name}/",
            "icon": get_story_icon(folder_name)
        }
        
        for line in lines[1:]:
            line_str = line.strip()
            if not line_str.startswith("- ") and not line_str.startswith("* "):
                continue
            
            field_part = re.sub(r'^[-*]\s*', '', line_str)
            if ":" not in field_part:
                continue
                
            key_part, val_part = field_part.split(":", 1)
            key = key_part.replace("**", "").strip().lower()
            val = val_part.strip()
            
            if key == "title":
                proj["title"] = val
            elif key == "attribution":
                proj["author_info"] = val.replace(" · ", " &nbsp;·&nbsp; ")
            elif key == "word count":
                wc = val.replace(",", "")
                proj["word_count"] = int(wc) if wc.isdigit() else 0
            elif key == "reading time":
                proj["reading_minutes"] = int(val) if val.isdigit() else 0
            elif key == "synopsis":
                proj["synopsis"] = val

        if proj["synopsis"]:
            proj["synopsis"] = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', proj["synopsis"])
            proj["synopsis"] = re.sub(r'\*(.*?)\*', r'<em>\1</em>', proj["synopsis"])
            
        projects.append(proj)

    def parse_folder_date(folder_name):
        if folder_name == "20-07-2026_The_Green_Interregnum":
            return "9999-99-99"
        m = re.match(r"^(\d{2})-(\d{2})-(\d{4})", folder_name)
        if m:
            day, month, year = m.groups()
            return f"{year}-{month}-{day}"
        return folder_name

    projects.sort(key=lambda x: parse_folder_date(x["folder_name"]), reverse=True)
    return projects


def get_story_icon(folder_name):
    """Return a root-relative story icon path for known library entries or local images."""
    story_icons = {
        "20-07-2026_The_Green_Interregnum": "Stories written with Narracode/20-07-2026_The_Green_Interregnum/img/green_interregnum_banner.webp",
        "07-06-2026_Concerning_Rights_and_Clauses": "Stories written with Narracode/07-06-2026_Concerning_Rights_and_Clauses/img/node-1-oceanic-contract.png",
        "29-05-2026_Smorky": "Stories written with Narracode/29-05-2026_Smorky/img/smorky_ep1_header.png",
        "15-05-2026_The_Author_Was_Already_Dead": "Stories written with Narracode/15-05-2026_The_Author_Was_Already_Dead/img/header.webp",
        "14-05-2026_Aft_of_Nowhere": "Stories written with Narracode/14-05-2026_Aft_of_Nowhere/img/banners/1b-aft-opening.webp",
        "11-05-2026_Tamagotchi": "img/story-icons/trygve-aas.webp",
        "10-05-2026_Exile": "img/story-icons/exile-cut.webp",
        "09-05-2026_Slime": "img/story-icons/slime-friendship-bloom.webp",
    }
    if folder_name in story_icons:
        return story_icons[folder_name]
    
    # Fallback to local img/header.png or img/header.webp
    base_dir = "Stories written with Narracode"
    for filename in ("banners/0.png", "banners/0.webp", "header.png", "header.webp"):
        candidate = os.path.join(base_dir, folder_name, "img", filename)
        if os.path.exists(candidate):
            return candidate
    return ""


def is_story_draft(filename):
    """Only include intended story drafts in generated pages and counts."""
    lowered = filename.lower()
    return (
        filename.endswith('.md')
        and lowered != 'readme.md'
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
    # Also get prefix number if it starts with one, e.g. "1-first_scene" -> "1"
    prefix_match = re.match(r'^(\d+)', stem)
    prefix = prefix_match.group(1) if prefix_match else ""
    
    banner_dir = os.path.join(project_dir, "img", "banners")
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        candidate = os.path.join(banner_dir, f"{stem}{ext}")
        if os.path.exists(candidate):
            return f"img/banners/{stem}{ext}"
        if prefix:
            candidate = os.path.join(banner_dir, f"{prefix}{ext}")
            if os.path.exists(candidate):
                return f"img/banners/{prefix}{ext}"
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
        },
        "12-06-2026_Post_Everything": {
            "1-first_scene.md": "The Bio-Baked Neuromorph",
            "2-vignette_two.md": "The Logistics Assembly",
            "3-in_the_closet.md": "Apoptosis in the Closet",
            "4-vignette_four.md": "The Crane Arbitrage Exploit",
            "5-vignette_five.md": "Flushing the System",
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
    html_out = ""
    banner = chapter_banner_path(project_dir, draft_file)
    banner_inserted = False
    title = chapter_title_for_draft(project_dir, draft_file)
    has_markdown_heading = any(re.match(r'^\s*#{1,3}\s+', block) for block in blocks)

    if title and not has_markdown_heading:
        html_out += f'        <h3 class="chapter-heading">{inline_markdown(title)}</h3>\n\n'
        if banner:
            html_out += f'        <img src="{banner}" alt="" class="chapter-banner" loading="lazy">\n\n'
            banner_inserted = True

    section_count = 0
    for block in blocks:
        if not block.strip():
            continue

        if re.fullmatch(r'-{3,}', block.strip()):
            html_out += '        <div class="break">· · ·</div>\n\n'
            continue

        heading = re.match(r'^(#{1,3})\s+(.+)$', block.strip())
        if heading:
            level = len(heading.group(1))
            if level == 1:
                # Skip duplicate page-level title h1 if it matches story title
                continue

            section_count += 1
            title = display_chapter_title(heading.group(2))
            html_out += f'        <h3 class="chapter-heading">{inline_markdown(title)}</h3>\n\n'
            
            # Check for section banner e.g. img/banners/1.png
            sec_banner = None
            banner_dir = os.path.join(project_dir, "img", "banners")
            for ext in (".png", ".webp", ".jpg", ".jpeg"):
                cand = os.path.join(banner_dir, f"{section_count}{ext}")
                if os.path.exists(cand):
                    sec_banner = f"img/banners/{section_count}{ext}"
                    break

            if sec_banner:
                html_out += f'        <img src="{sec_banner}" alt="" class="chapter-banner" loading="lazy">\n\n'
            elif banner and not banner_inserted:
                html_out += f'        <img src="{banner}" alt="" class="chapter-banner" loading="lazy">\n\n'
                banner_inserted = True
            continue

        if banner and not banner_inserted:
            html_out += f'        <img src="{banner}" alt="" class="chapter-banner" loading="lazy">\n\n'
            banner_inserted = True

        processed_lines = []
        for line in block.splitlines():
            lspaces = len(line) - len(line.lstrip(' '))
            nbsps = '&nbsp;' * lspaces
            processed_lines.append(nbsps + inline_markdown(line.lstrip(' ')))
        
        block_html = "<br>\n".join(processed_lines)
        html_out += f"        <p>{block_html}</p>\n\n"

    return html_out
