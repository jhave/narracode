import os
import re
import sys
import shutil


def count_words_in_drafts(drafts_dir):
    """Sum words across all draft .md files (excluding pre-edit versions)."""
    if not os.path.exists(drafts_dir):
        return 0
    total = 0
    for f in sorted(os.listdir(drafts_dir)):
        if not f.endswith('.md') or 'pre-edit' in f:
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
        m = re.search(r'Display title:\s*([^.\n]+?)\s*(?:\.\s|\.$|$)', content, flags=re.MULTILINE)
        if m:
            return m.group(1).strip()
    return folder_name.split('_')[-1].replace('-', ' ').title()


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
    
    # Replace visual title
    template = template.replace("The Long Afternoon", title)
    
    # Replace Subtitle
    template = template.replace("A story by Claude Opus 4.7, from a one-shot prompt, concerning the escape of a mythical semi-autonomous model\n        that obstructs thermonuclear war.", "A neurosymbolic narrative generated using the Narracode harness.")
    
    # Replace Byline
    if author_info:
        template = re.sub(r"<h5>.*?</h5>", f"<h5>{author_info}</h5>", template, flags=re.DOTALL)

    # Remove prompt-toggle and specific images
    template = re.sub(r'<details class="prompt-toggle">.*?</details>', '', template, flags=re.DOTALL)
    template = re.sub(r'<img src="img/the_long_afternoon_cover[^>]+>', '', template, flags=re.DOTALL)
    template = re.sub(r'<div class="related">\s*<h4></h4>\s*<img src="img/the_long_afternoon_cover[^>]+>\s*</div>', '', template, flags=re.DOTALL)

    # Split template at story div
    parts = template.split('<div class="story">')
    header = parts[0] + '<div class="story">\n'
    footer = parts[1].split('</div>\n\n\n    <!-- Related Works by Jhave -->')[1]
    footer = '</div>\n\n    <!-- Related Works by Jhave -->' + footer

    # Process drafts
    draft_files = [f for f in os.listdir(drafts_dir) if f.endswith('.md') and not 'pre-edit' in f]
    draft_files.sort()

    story_html = ""

    for i, file in enumerate(draft_files):
        with open(os.path.join(drafts_dir, file), "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract text after '---'
        parts = content.split("---")
        if len(parts) > 1:
            text = parts[-1].strip()
        else:
            text = content.strip()
            
        paragraphs = text.split("\n\n")
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            
            # Simple markdown to HTML
            p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p) # bold
            p = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p) # italics
            
            story_html += f"        <p>{p}</p>\n\n"
            
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
    
    # Find all projects that have been built
    projects = []
    if os.path.exists(base_dir):
        for folder in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                if os.path.exists(os.path.join(folder_path, "index.html")):
                    title = get_display_title(folder_path, folder)

                    # Word count + reading time
                    word_count = count_words_in_drafts(os.path.join(folder_path, "drafts"))
                    reading_minutes = max(1, round(word_count / 250))

                    # Extract authors
                    author_info = ""
                    attr_path = os.path.join(folder_path, "ATTRIBUTION.md")
                    if os.path.exists(attr_path):
                        with open(attr_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            attrs = []
                            for line in lines:
                                if ":" in line:
                                    attrs.append(line.split(":", 1)[1].strip())
                            if attrs:
                                author_info = " &nbsp;·&nbsp; ".join(attrs)
                    
                    # Extract synopsis from POETICS.md
                    synopsis = ""
                    poetics_path = os.path.join(folder_path, "POETICS.md")
                    if os.path.exists(poetics_path):
                        with open(poetics_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if "## Premise" in content:
                                part = content.split("## Premise")[1]
                                # get text until next ##
                                synopsis_text = part.split("##")[0].strip()
                                # take the first paragraph
                                synopsis = synopsis_text.split("\n\n")[0].strip()
                                # basic markdown bold/italic removal or conversion
                                synopsis = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', synopsis)
                                synopsis = re.sub(r'\*(.*?)\*', r'<em>\1</em>', synopsis)

                    projects.append({
                        "title": title,
                        "path": f"{base_dir}/{folder}/index.html",
                        "folder_name": folder,
                        "author_info": author_info,
                        "synopsis": synopsis,
                        "word_count": word_count,
                        "reading_minutes": reading_minutes,
                    })
    
    projects.sort(key=lambda x: x["folder_name"], reverse=True) # newest first

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
            display: block;
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
        <p style="margin-bottom: 1.5rem; font-size: 1.05rem;">As the system advances, it runs in the background to auto-refine a <strong>symbolic working memory</strong>. It externalizes the narrative state into discrete files: mapping shifting character graphs, tracking strict time-constants, and recording a definitive history. This prevents hallucinatory drift and grounds the AI in deep continuity.</p>
        
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

    <h2>Example Stories</h2>
"""
    
    for p in projects:
        meta_line = f"≈ {p['word_count']:,} words · {p['reading_minutes']} min read" if p['word_count'] else ""
        html += f"""    <a href="{p['path']}" class="story-link">
        <div class="story-title">{p['title']}</div>
        <div class="story-authors">{p['author_info']}</div>
        <div class="story-meta">{meta_line}</div>
        <div class="story-synopsis">{p['synopsis']}</div>
    </a>
"""

    html += """
    
    <!-- Related Works by Jhave -->
    <div class="related">
        <h4>Related Works by Jhave</h4>
        <p style="line-height: 1.8;">
            <a target="_blank" href="https://glia.ca/2026/inheritors/">The Inheritors: Neanderthals met Sapiens ⟶ Sapiens meet AGI</a> (April 21, 2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2026/the-long-afternoon/">The Long Afternoon: a mythical semi-autonomous model obstructs thermonuclear war.</a> (April 20, 2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2026/sffai/">Seeds for Future AI</a> (March 12, 2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2026/the-good-light/">The Good Light: an anecdote about grief | Written with Claude Opus 4.6.</a> (Feb 11, 2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/gentle/">Artificial Gentle Intelligence (AGI)</a> (May 22, 2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/stimverse/">StimVerse Draft</a> (April 1 &amp; 20–21, 2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/ghir/">GHIR: Global Health Immune Response</a> (March 7, 2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/mai/">Matriarchal AI</a> (2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/wuai/">#Whole-Use-AI</a> (2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/eahe/">Everyone at Home Everywhere</a> (2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2023/wise/">Wisdom A.I.</a> (May 2, 2023)
        </p>
    </div>

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
