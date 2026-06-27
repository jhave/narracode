import os
import sys
import shutil
import re
import html
from build_helpers import (
    count_words_in_drafts,
    get_display_title,
    get_story_icon,
    get_display_synopsis,
    inline_markdown,
    is_story_draft,
    draft_to_html,
    build_related_footer,
    get_story_projects
)

def build_story_index(project_dir):
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
    story_icon_path = ""
    if story_icon:
        prefix = f"Stories written with Narracode/{folder_name}/"
        if story_icon.startswith(prefix):
            story_icon_path = story_icon[len(prefix):]
        else:
            story_icon_path = f"../../{story_icon}"
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

    if folder_name == "12-06-2026_Post_Everything":
        word_count = count_words_in_drafts(drafts_dir)
        author_info = f"Human: Jhave &nbsp;·&nbsp; Text: Gemini 2.5 Flash (Antigravity) &nbsp;·&nbsp; Images: GPT Images-2 &nbsp;·&nbsp; Date: June 12, 2026 &nbsp;·&nbsp; Length: {word_count:,} words"
    elif folder_name == "14-06-2026_Dissolution":
        word_count = count_words_in_drafts(drafts_dir)
        author_info = f"Human: Jhave &nbsp;·&nbsp; Words: {word_count:,} &nbsp;·&nbsp; Editing and Images: Gemini Flash 3.5 &nbsp;·&nbsp; Date: June 14, 2026"
    elif folder_name == "15-06-2026_TheCompulsionLoop":
        word_count = count_words_in_drafts(drafts_dir)
        author_info = f"Human: Jhave &nbsp;·&nbsp; Words: {word_count:,} &nbsp;·&nbsp; Editing and Images: Gemini Flash 3.5 &nbsp;·&nbsp; Date: June 15, 2026"
    elif folder_name == "20-06-2026_Project_A-0":
        word_count = count_words_in_drafts(drafts_dir)
        author_info = f"Human: Jhave &nbsp;·&nbsp; Words: {word_count:,} &nbsp;·&nbsp; Editing and Images: Gemini 3.5 Flash &nbsp;·&nbsp; Date: June 20, 2026"
    elif folder_name == "26-06-2026_The_First_Water_Molecule":
        word_count = count_words_in_drafts(drafts_dir)
        author_info = f"Human: Jhave &nbsp;·&nbsp; Words: {word_count:,} &nbsp;·&nbsp; Composition &amp; editing: Claude Opus 4.8 &nbsp;·&nbsp; Narracode harness (AUTO_MODE) &nbsp;·&nbsp; Date: June 26, 2026"

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read().replace("\r\n", "\n")

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
        img_width, img_height = "640", "640"
        if folder_name in ("12-06-2026_Post_Everything", "20-06-2026_Project_A-0"):
            img_width, img_height = "900", "480"
        template = template.replace(
            "    <!-- Title -->\n    <h1>",
            f'    <img src="{story_icon_path}" class="story-page-icon" width="{img_width}" height="{img_height}">\n\n    <!-- Title -->\n    <h1>',
            1
        )

    if folder_name in ("12-06-2026_Post_Everything", "20-06-2026_Project_A-0"):
        template = template.replace(
            "    </style>",
            """        .back-link {
            margin-bottom: 2rem;
            text-align: left;
        }

        .back-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--muted);
            text-decoration: none;
            transition: color 0.2s ease;
        }

        .back-btn:hover {
            color: var(--text);
        }

        .prompt-toggle summary::before {
            content: "▸";
            display: inline-block;
            transition: transform 0.25s ease;
            color: var(--muted);
            font-size: 0.85rem;
            animation: chevron-flash 1s infinite alternate;
        }

        @keyframes chevron-flash {
            0% { opacity: 0.2; }
            100% { opacity: 1; }
        }

        .story-page-icon {
            width: 100%;
            max-width: 100%;
            height: auto;
            aspect-ratio: 15 / 8;
            object-fit: cover;
        }
    </style>"""
        )
        template = template.replace(
            "<body>",
            """<body>
    <!-- Back Link -->
    <div class="back-link">
        <a href="../../index.html" class="back-btn">← Back to Narracode</a>
    </div>"""
        )
    
    # Replace Subtitle
    subtitle_html = 'A neurosymbolic narrative generated using the <a href="https://jhave.github.io/narracode/">Narracode harness</a>.'
    if folder_name in ("12-06-2026_Post_Everything", "20-06-2026_Project_A-0"):
        subtitle_html = 'A narrative generated using the <a href="https://jhave.github.io/narracode/">Narracode harness</a>.'
    template = template.replace("A story by Claude Opus 4.7, from a one-shot prompt, concerning the escape of a mythical semi-autonomous model\n        that obstructs thermonuclear war.", subtitle_html)
    
    # Replace Byline
    if author_info:
        template = re.sub(r"<h5>.*?</h5>", lambda m: f"<h5>{author_info}</h5>", template, flags=re.DOTALL)

    # Insert or remove prompt-toggle
    prompt_toggle_html = ""
    if os.path.exists(attr_path):
        with open(attr_path, "r", encoding="utf-8") as f:
            attr_content = f.read()
        m = re.search(r'## Seed Prompt\s*\n```text\s*\n(.*?)\n```', attr_content, flags=re.DOTALL)
        if m:
            prompt_text = m.group(1).strip()
            prompt_paragraphs = "".join(f"            <p>{html.escape(p)}</p>\n" for p in prompt_text.split("\n\n") if p.strip())
            prompt_toggle_html = f"""    <details class="prompt-toggle">
        <summary>prompt</summary>
        <div class="prompt-body">
{prompt_paragraphs}        </div>
    </details>"""

    # Generate synopsis-toggle if folder is Post_Everything or Project_A-0
    synopsis_toggle_html = ""
    if folder_name in ("12-06-2026_Post_Everything", "20-06-2026_Project_A-0"):
        synopsis_text = get_display_synopsis(project_dir)
        if synopsis_text:
            synopsis_formatted = inline_markdown(synopsis_text)
            synopsis_paragraphs = "".join(f"            <p>{p}</p>\n" for p in synopsis_formatted.split("\n\n") if p.strip())
            synopsis_toggle_html = f"""\n    <details class="prompt-toggle">
        <summary>synopsis</summary>
        <div class="prompt-body">
{synopsis_paragraphs}        </div>
    </details>"""

    if prompt_toggle_html:
        template = re.sub(r'<details class="prompt-toggle">.*?</details>', lambda m: prompt_toggle_html + synopsis_toggle_html, template, flags=re.DOTALL)
    else:
        template = re.sub(r'<details class="prompt-toggle">.*?</details>', '', template, flags=re.DOTALL)
    template = re.sub(r'\s*<!-- Related Works by Jhave -->\s*<div class="related">\s*<h4></h4>.*?</div>\s*', '\n', template, flags=re.DOTALL)
    template = re.sub(r'<img src="img/the_long_afternoon_cover[^>]+>', '', template, flags=re.DOTALL)
    template = re.sub(r'<div class="related">\s*<h4></h4>\s*<img src="img/the_long_afternoon_cover[^>]+>\s*</div>', '', template, flags=re.DOTALL)

    # Split template at story div
    parts = template.split('<div class="story">')
    header = parts[0] + '<div class="story">\n'
    footer = parts[1].split('<!-- Related Works by Jhave -->', 1)[1]
    footer = '</div>\n\n    <!-- Related Works by Jhave -->' + footer
    footer = re.sub(
        r'    <!-- Related Works by Jhave -->\s*<div class="related">.*?</div>',
        lambda m: build_related_footer(get_story_projects(), current_folder=folder_name, for_story_page=True),
        footer,
        count=1,
        flags=re.DOTALL,
    )

    # Process drafts
    draft_files = [f for f in os.listdir(drafts_dir) if is_story_draft(f)]
    draft_files.sort(key=lambda fn: int(re.match(r'^(\d+)', fn).group(1)) if re.match(r'^(\d+)', fn) else 9999)

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
    else:
        for f in os.listdir(img_src):
            src_f = os.path.join(img_src, f)
            dest_f = os.path.join(img_dest, f)
            if os.path.isfile(src_f) and not os.path.exists(dest_f):
                shutil.copy2(src_f, dest_f)

    print(f"Generated HTML successfully for {title} at {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        build_story_index(sys.argv[1])
    else:
        print("Usage:")
        print("  python build_story_index.py <project_folder_path>")
