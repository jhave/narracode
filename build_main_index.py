import os
import sys
import re
from build_helpers import (
    get_story_projects,
    RELATED_WORKS_HTML
)

def build_main_index():
    base_dir = "Stories written with Narracode"
    root_index = "index.html"
    projects = get_story_projects(base_dir)

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
            display: grid;
            grid-template-columns: 128px 1fr;
            gap: 1.25rem;
            align-items: start;
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
        .story-link.no-image {{
            grid-template-columns: 1fr;
        }}
        .story-link:hover {{
            border-color: var(--accent);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transform: translateY(-2px);
        }}
        .story-icon {{
            display: block;
            width: 128px;
            height: 128px;
            aspect-ratio: 1;
            object-fit: cover;
            border-radius: 6px;
            border: 1px solid #e6e1da;
            background: #f8f6f1;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
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
        .structure-diagram {{
            display: block;
            width: 100%;
            max-width: 680px;
            margin: 1.5rem auto;
            border-radius: 8px;
            border: 1px solid #e6e1da;
            background: #fbfaf7;
        }}
        .memory-list {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.45rem 1rem;
            margin: 1rem 0 1.3rem;
            padding: 0;
            list-style: none;
            font-size: 0.95rem;
            color: #555;
        }}
        .memory-list li {{
            padding-left: 0.85rem;
            border-left: 2px solid #d9d5cc;
        }}
        @media (max-width: 620px) {{
            .story-link {{
                grid-template-columns: 88px 1fr;
                gap: 1rem;
                padding: 1rem;
            }}
            .story-link.no-image {{
                grid-template-columns: 1fr;
            }}
            .story-icon {{
                width: 88px;
                height: 88px;
            }}
            .story-title {{
                font-size: 1.35rem;
                line-height: 1.25;
            }}
            .story-synopsis {{
                font-size: 0.98rem;
            }}
            .memory-list {{
                grid-template-columns: 1fr;
            }}
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
        <p style="margin-bottom: 1.5rem; font-size: 1.05rem;">As the system advances, it runs in the background to auto-refine a <strong>layered symbolic working memory</strong>. Beyond character graphs, time-constants, and history, the harness now tracks obligations, motifs, scene function, character interiority, and reader-state. The goal is not just factual coherence, but preserving accumulated literary pressure across scenes.</p>

        <img src="img/narracode-structural-loop.webp" alt="Diagram of the Narracode scene cycle: natural language request, agents, layered structural memory, scene draft, check file, and human decision." class="structure-diagram" loading="lazy">

        <ul class="memory-list">
            <li><strong>Obligations</strong>: unresolved promises, withheld information, emotional debts.</li>
            <li><strong>Motifs</strong>: recurring images, gestures, objects, symbolic pressures.</li>
            <li><strong>Scene ledger</strong>: scene function, turn, aftermath, open questions.</li>
            <li><strong>Character interiority</strong>: private states, arcs, cathartic inflection points.</li>
            <li><strong>Reader state</strong>: reader memory, expectations, plausible defiance paths.</li>
            <li><strong>critiques/check-*.md</strong>: concise post-draft checks without rewriting.</li>
        </ul>
        
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

    <div style="text-align: center; margin-top: 2rem; margin-bottom: 0;">
        <img src="img/Narracode harness system schematic view.png" alt="Narracode" style="max-width: 100%;">
    </div>

    <div style="text-align: center; margin-top: 2rem; margin-bottom: 0;">
        <h1>📚 Example Stories</h1>
    </div>
"""
    
    for p in projects:
        meta_line = f"≈ {p['word_count']:,} words · {p['reading_minutes']} min read" if p['word_count'] else ""
        icon_html = f'<img src="{p["icon"]}" alt="" class="story-icon" loading="lazy" width="640" height="640">' if p["icon"] else ""
        link_class = "story-link" if p["icon"] else "story-link no-image"
        html += f"""    <a href="{p['path']}" class="{link_class}">
        {icon_html}
        <div class="story-copy">
            <div class="story-title">{p['title']}</div>
            <div class="story-authors">{p['author_info']}</div>
            <div class="story-meta">{meta_line}</div>
            <div class="story-synopsis">{p['synopsis']}</div>
        </div>
    </a>
"""

    html += "\n    \n" + RELATED_WORKS_HTML + """

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
    build_main_index()
