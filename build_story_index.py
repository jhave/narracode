#!/usr/bin/env python3
"""
build_story_index.py — Dedicated script to generate a single story index.html.

Safety Protection:
If index.html already exists in the target story directory, this script will NOT
overwrite it unless the --force flag is explicitly passed. This prevents accidentally
wiping out custom HTML formatting, manual image wiring, or custom details folds.
"""

import os
import sys
import argparse
from build_site import build_site

def main():
    parser = argparse.ArgumentParser(description="Build a single story index.html page.")
    parser.add_argument("folder", help="Path to the story project folder (e.g. 'Stories written with Narracode/25-06-2026_Crepuscular')")
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite if index.html already exists in the story directory")

    args = parser.parse_args()
    folder_path = os.path.abspath(args.folder)

    if not os.path.exists(folder_path):
        print(f"Error: Directory '{folder_path}' does not exist.")
        sys.exit(1)

    target_html = os.path.join(folder_path, "index.html")
    if os.path.exists(target_html) and not args.force:
        print(f"SAFETY ABORT: '{target_html}' already exists!")
        print("To protect your custom HTML edits, manual images, and folds, build_story_index.py will NOT overwrite it.")
        print("If you truly want to regenerate and overwrite this story HTML file, re-run with --force:")
        print(f"  python3 build_story_index.py \"{args.folder}\" --force")
        sys.exit(1)

    print(f"Building story index for '{args.folder}'...")
    build_site(folder_path)
    print(f"Successfully generated story index at '{target_html}'")

if __name__ == "__main__":
    main()
