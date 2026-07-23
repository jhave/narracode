import re

file_path = "/Users/jhave/Sites/2026/narracode/Stories written with Narracode/15-06-2026_TheCompulsionLoop/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_story = False
updated_lines = []

for i, line in enumerate(lines):
    line_num = i + 1
    
    # We detect boundaries using identical conditions as find_markers.py
    if '<div class="story">' in line:
        in_story = True
    
    if in_story:
        # Perform replacements for _WORD_ and *WORD*
        new_line = re.sub(r'_([^_]+)_', r'<em>\1</em>', line)
        new_line = re.sub(r'\*([^*]+)\*', r'<b>\1</b>', new_line)
        if new_line != line:
            print(f"Line {line_num} modified:")
            print(f"  Old: {line.strip()}")
            print(f"  New: {new_line.strip()}")
        line = new_line
        
    if '<!-- Other Works by Narracode -->' in line:
        in_story = False
        
    updated_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(updated_lines)

print("Find and replace completed.")
