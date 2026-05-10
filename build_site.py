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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        build_site(sys.argv[1])
    else:
        print("Usage: python build_site.py <project_folder_path>")
