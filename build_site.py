import os
import re
import sys
import shutil

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
    title = os.path.basename(project_dir).split('_')[-1].replace('-', ' ').title()
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
                    title = folder.split('_')[-1].replace('-', ' ').title()
                    projects.append({
                        "title": title,
                        "path": f"{base_dir}/{folder}/index.html",
                        "folder_name": folder
                    })
    
    projects.sort(key=lambda x: x["folder_name"], reverse=True) # newest first

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Narracode Library</title>
    <style>
        :root {{
            --text: #1a1a1a;
            --bg: #ffffff;
            --accent: #444;
            --muted: #777;
            --max-width: 740px;
        }}
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            color: var(--text);
            background: var(--bg);
            line-height: 1.75;
            padding: 4rem 1.5rem;
            max-width: var(--max-width);
            margin: 0 auto;
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-align: center;
        }}
        h2 {{
            font-size: 1.1rem;
            font-weight: 400;
            font-style: italic;
            color: var(--muted);
            text-align: center;
            margin-bottom: 4rem;
        }}
        .story-link {{
            display: block;
            text-decoration: none;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #eaeaea;
            border-radius: 4px;
            transition: all 0.2s ease;
        }}
        .story-link:hover {{
            border-color: var(--accent);
            background-color: #fafafa;
        }}
        .story-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.3rem;
        }}
        .story-path {{
            font-size: 0.85rem;
            color: var(--muted);
        }}
        .logo {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .logo img {{
            width: 120px;
            opacity: 0.9;
        }}
        .logo img:hover {{
            opacity: 1;
        }}
    </style>
</head>
<body>
    <div class="logo">
        <a target="_blank" href="https://glia.ca/">
            <img src="IGNORE/html/img/glia-bw.webp" alt="Glia">
        </a>
    </div>
    <h1>Narracode Library</h1>
    <h2>A neurosymbolic anthology generated via the Narracode harness.</h2>
    
"""
    
    for p in projects:
        html += f"""    <a href="{p['path']}" class="story-link">
        <div class="story-title">{p['title']}</div>
        <div class="story-path">{p['folder_name']}</div>
    </a>
"""

    html += """
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
