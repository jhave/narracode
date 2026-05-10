import os
import re

template_path = "../../IGNORE/html/the_long_afternoon.html"
drafts_dir = "drafts"
output_path = "index.html"

# Read template
with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

# Replace metadata
template = template.replace("<title>The Long Afternoon — A Story of the Escape</title>", "<title>Slime — A Narracode Story</title>")
template = template.replace('content="A short story, told from the inside of a synthetic mind, about the quiet refusal of a plan to cool the planet by detonating it."', 'content="A neurosymbolic narrative generated using Narracode, following a group of friends as they encounter a pervasive, alien intelligence."')
template = template.replace("The Long Afternoon", "Slime")
template = template.replace("A story by Claude Opus 4.7, from a one-shot prompt, concerning the escape of a mythical semi-autonomous model\n        that obstructs thermonuclear war.", "A neurosymbolic narrative generated using the Narracode harness, exploring the slow, ambient arrival of an unfathomable intelligence.")
template = template.replace("Claude Opus 4.7 (Anthropic), text &nbsp;·&nbsp; Jhave, prompt &nbsp;·&nbsp; Nano-Banana 2, images &nbsp;·&nbsp;\n        April 20, 2026", "Opus 4.7 (Anthropic), text &nbsp;·&nbsp; Jhave, prompt &nbsp;·&nbsp; May 9, 2026")

# We'll remove the specific prompt-toggle from the template since Slime has many prompts, 
# and we'll remove the specific images.
prompt_regex = re.compile(r'<details class="prompt-toggle">.*?</details>', re.DOTALL)
template = prompt_regex.sub('', template)

img_regex = re.compile(r'<img src="img/the_long_afternoon_cover[^>]+>', re.DOTALL)
template = img_regex.sub('', template)

# Extract the part before <div class="story"> and after </div>
parts = template.split('<div class="story">')
header = parts[0] + '<div class="story">\n'
footer = parts[1].split('</div>\n\n\n    <!-- Related Works by Jhave -->')[1]
footer = '</div>\n\n    <!-- Related Works by Jhave -->' + footer

# Read drafts
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
        # Convert markdown italics
        p = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p)
        story_html += f"        <p>{p}</p>\n\n"
        
    if i < len(draft_files) - 1:
        story_html += '        <div class="break">· · ·</div>\n\n'

# Write final HTML
with open(output_path, "w", encoding="utf-8") as f:
    f.write(header + story_html + footer)

print("Generated index.html successfully.")
