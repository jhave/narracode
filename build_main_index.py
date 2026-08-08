#!/usr/bin/env python3
"""
build_main_index.py — Dedicated script to generate ONLY the root library index.html.

This script reads metadata.md from "Stories written with Narracode" and generates
the root index.html library page. It NEVER modifies any story index.html files.
"""

import sys
from build_site import build_library_index

def main():
    print("Building main library index at ./index.html...")
    build_library_index()
    print("Successfully generated root library at ./index.html")

if __name__ == "__main__":
    main()
