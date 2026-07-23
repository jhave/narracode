import re

file_path = "/Users/jhave/Sites/2026/narracode/Stories written with Narracode/15-06-2026_TheCompulsionLoop/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_story = False
for i, line in enumerate(lines):
    line_num = i + 1
    if '<div class="story">' in line:
        in_story = True
    if '<!-- Other Works by Narracode -->' in line:
        in_story = False
    
    if in_story:
        # Search for _something_
        under_matches = re.findall(r'_[^_]+_', line)
        # Search for *something*
        star_matches = re.findall(r'\*[^*]+\*', line)
        if under_matches or star_matches:
            print(f"Line {line_num}: {line.strip()}")
            if under_matches:
                print(f"  Underline matches: {under_matches}")
            if star_matches:
                print(f"  Star matches: {star_matches}")
