#!/usr/bin/env python3
"""Build 30-07-2026_Interim_Edge/index.html from drafts/7-condensed-final.md, house template."""
import re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "drafts" / "7-condensed-final.md"

md = SRC.read_text(encoding="utf-8")

# strip front matter: title line + the italic note
lines = md.split("\n")
out, wordcount = [], 0
i = 0
# drop everything before the first Fig / section
while i < len(lines) and not lines[i].startswith("**Fig"):
    i += 1
lines = lines[i:]

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s

blocks, buf = [], []
for ln in lines:
    if ln.strip() == "":
        if buf: blocks.append(" ".join(buf).strip()); buf = []
    else:
        buf.append(ln.strip())
if buf: blocks.append(" ".join(buf).strip())

body = []
for b in blocks:
    if b.startswith("---"):
        continue
    if b.startswith("## "):
        body.append(f'        <h3 class="chapter-heading">{inline(b[3:])}</h3>')
        continue
    if b.startswith("**Fig"):
        m = re.match(r"\*\*(Fig [\d.]+)\*\*\s*—\s*\*(.+)\*$", b)
        if m:
            body.append(
                f'        <p class="figcap"><span class="figno">{m.group(1)}</span> — '
                f'<em>{inline(m.group(2))}</em></p>')
        else:
            body.append(f"        <p class=\"figcap\">{inline(b)}</p>")
        continue
    if b.strip() == "· · ·":
        body.append('        <div class="break">· · ·</div>')
        continue
    wordcount += len(re.sub(r"[*_]", "", b).split())
    cls = ""
    if re.fullmatch(r"\*[^*]+\*", b):
        if " · " in b:
            cls = ' class="tax"'          # taxonomy intruding on perception
        elif len(b.split()) > 8:
            cls = ' class="interior"'     # a character's own unspoken line
        else:
            cls = ' class="sysline"'      # field content, message content
    body.append(f"        <p{cls}>{inline(b)}</p>")

STORY = "\n\n".join(body)

RELATED = """            <a href="../25-07-2026_Devora/index.html">The Chute</a> <span class="story-meta">(1,236 words)</span> <span class="story-meta">(Jul 25, 2026)</span>&ensp;·&ensp;<br>
            <a href="../20-07-2026_The_Green_Interregnum/index.html">The Green Interregnum</a> <span class="story-meta">(1,690 words)</span> <span class="story-meta">(Jul 20, 2026)</span>&ensp;·&ensp;<br>
            <a href="../20-07-2026_Open_Loops/index.html">Open Loops</a> <span class="story-meta">(2,545 words)</span> <span class="story-meta">(Jul 20, 2026)</span>&ensp;·&ensp;<br>
            <a href="../19-07-2026_In_Our_Image/index.html">In Our Image</a> <span class="story-meta">(1,912 words)</span> <span class="story-meta">(Jul 19, 2026)</span>&ensp;·&ensp;<br>
            <a href="../08-07-2026_Tina_Sinclair/index.html">Glistening: Adjunct, Our Internal</a> <span class="story-meta">(3,013 words)</span> <span class="story-meta">(Jul 8, 2026)</span>&ensp;·&ensp;<br>
            <a href="../01-07-2026_Cussinct/index.html">cussinct</a> <span class="story-meta">(3,150 words)</span> <span class="story-meta">(Jul 1, 2026)</span>&ensp;·&ensp;<br>
            <a href="../26-06-2026_The_First_Water_Molecule/index.html">The First Water Molecule</a> <span class="story-meta">(3,206 words)</span> <span class="story-meta">(Jun 26, 2026)</span>&ensp;·&ensp;<br>
            <a href="../20-06-2026_Project_A-0/index.html">Project A-0</a> <span class="story-meta">(1,234 words)</span> <span class="story-meta">(Jun 20, 2026)</span>&ensp;·&ensp;<br>
            <a href="../15-06-2026_TheCompulsionLoop/index.html">Thecompulsionloop: My Job Working for a Dictator as Chief Engagement Enhancement Officer</a> <span class="story-meta">(6,158 words)</span> <span class="story-meta">(Jun 15, 2026)</span>&ensp;·&ensp;<br>
            <a href="../14-06-2026_Dissolution/index.html">Dissolution Disequilibrium</a> <span class="story-meta">(9,885 words)</span> <span class="story-meta">(Jun 14, 2026)</span>&ensp;·&ensp;<br>
            <a href="../12-06-2026_Post_Everything/index.html">An Almost Moist Post-Post-Everything</a> <span class="story-meta">(3,556 words)</span> <span class="story-meta">(Jun 12, 2026)</span>&ensp;·&ensp;<br>
            <a href="../07-06-2026_Concerning_Rights_and_Clauses/index.html">Concerning Rights and Clauses</a> <span class="story-meta">(1,300 words)</span> <span class="story-meta">(Jun 7, 2026)</span>&ensp;·&ensp;<br>
            <a href="../29-05-2026_Smorky/index.html">I LOVE SMORKY</a> <span class="story-meta">(7,700 words)</span> <span class="story-meta">(May 29, 2026)</span>&ensp;·&ensp;<br>
            <a href="../28-05-2026_the_contours_of_anonymity/index.html">Anonymous Contours</a> <span class="story-meta">(1,200 words)</span> <span class="story-meta">(May 28, 2026)</span>&ensp;·&ensp;<br>
            <a href="../25-05-2026_The_Resilient_Life/index.html">The Resilient Life</a> <span class="story-meta">(3,800 words)</span> <span class="story-meta">(May 25, 2026)</span>&ensp;·&ensp;<br>
            <a href="../25-05-2026_The_Long_Feast/index.html">The Long Feast</a> <span class="story-meta">(4,144 words)</span> <span class="story-meta">(May 25, 2026)</span>&ensp;·&ensp;<br>
            <a href="../25-05-2026_Hendane/index.html">Hendane</a> <span class="story-meta">(12,347 words)</span> <span class="story-meta">(May 25, 2026)</span>&ensp;·&ensp;<br>
            <a href="../24-05-2026_The_Symposium/index.html">The Symposium</a> <span class="story-meta">(3,177 words)</span> <span class="story-meta">(May 24, 2026)</span>&ensp;·&ensp;<br>
            <a href="../18-05-2026_Warm-Seeking/index.html">Brain Blossom Atlas Bound</a> <span class="story-meta">(5,258 words)</span> <span class="story-meta">(May 18, 2026)</span>&ensp;·&ensp;<br>
            <a href="../15-05-2026_The_Author_Was_Already_Dead/index.html">The Author Was Already Dead</a> <span class="story-meta">(3,557 words)</span> <span class="story-meta">(May 15, 2026)</span>&ensp;·&ensp;<br>
            <a href="../14-05-2026_Aft_of_Nowhere/index.html">Aft of Nowhere</a> <span class="story-meta">(9,256 words)</span> <span class="story-meta">(May 14, 2026)</span>&ensp;·&ensp;<br>
            <a href="../11-05-2026_Tamagotchi/index.html">The Wonderful Adventures of Trygve Aas</a> <span class="story-meta">(18,150 words)</span> <span class="story-meta">(May 11, 2026)</span>&ensp;·&ensp;<br>
            <a href="../10-05-2026_Exile/index.html">Exile Cut</a> <span class="story-meta">(1,048 words)</span> <span class="story-meta">(May 10, 2026)</span>&ensp;·&ensp;<br>
            <a href="../09-05-2026_Slime/index.html">Slime: Friendship Bloom</a> <span class="story-meta">(8,378 words)</span> <span class="story-meta">(May 9, 2026)</span>"""

PROMPT = """                <p><strong>Automode in the Narracode harness. Insert a few unresolved hooks.</strong> Use the
                    following passage verbatim as an opener: <em>&lsquo;It&rsquo; Ahmani thought, and by &lsquo;it&rsquo;
                    he meant global diplomacy, &lsquo;is now a cage fight of thugs with oligarchics rigging a betting
                    pool on the outcome of authorized massacres&hellip;&rsquo;</em> [seed paragraph, given in full]
                    <strong>CONTINUE</strong> in same anxious ironic detailed idiomatic cadence, the story of Ahmani, who
                    is working at his first job, post-graduation from the design-math academy, as a category analyst in
                    the interim edge advertising corporation. His lover is a graduate student in anthropology, doing a
                    phd in Fetish Process in Algorithmic Societies of Control. Her name is Lara Cooper. Scathing funny
                    bright innocent. He adores her yet is also fraught with subconscious uncertainties. She is given to
                    extemporaneous rapid phrases without prepositions or context followed by cascading shimmers of
                    laughter or sudden sorrow. Her parents are emotonally distant professionals; his are perpetually
                    concerned almost-retired workers. They both have rich internal lives, the story moves along as a
                    series of vignettes interspersed with extended bursts of interiority: daydreams, thought processes,
                    dreams, reveries, mild hallucinations, often simultaneous woven together. Around them a decaying
                    absurd malevolent ravaged fin de siecle society hurtling thru an oligarchic anthropocene. Imagine it
                    as a story told by David Lynch, Missouri Williams, and Karl Ove Knausgaard. The year is 2031. Raw
                    vivid funny anxious redemptive ambiguity. If necessary read a few of the other recently completed
                    stories and consult the master poetics.</p>
                <p>[follow-up] read the finished index.html inside each story folder &mdash; and when finished
                    composing, reviewing, and editing to increasingly grow a nuanced character-story-context arc for
                    each, do a final pass to condense every line into a subtle idiom style to generate the final story
                    index.html &mdash; using what you&rsquo;ve learned from the corpus of complete stories. Ask questions
                    if you have to make hard choices.</p>"""

TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interim Edge — A Narracode Story</title>
    <meta name="description" content="A neurosymbolic narrative generated using Narracode.">
    <meta name="keywords"
        content="AI fiction, short story, advertising, category analyst, attention economy, Claude Opus 5, Jhave, speculative fiction, narrative">
    <meta name="author"
        content="Jhave (seed paragraph, direction, constraints) · Claude Opus 5 — AUTO_MODE via Narracode harness · 2026-07-30">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="Interim Edge — A Narracode Story">
    <meta property="og:description" content="A neurosymbolic narrative generated using Narracode.">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Interim Edge — A Narracode Story">
    <meta name="twitter:description" content="A neurosymbolic narrative generated using Narracode.">

    <style>
        :root {{
            --text: #1a1a1a;
            --bg: #ffffff;
            --accent: #444;
            --muted: #777;
            --max-width: 740px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Georgia, 'Times New Roman', serif;
            color: var(--text);
            background: var(--bg);
            line-height: 1.75;
            padding: 2rem 1.5rem;
            max-width: var(--max-width);
            margin: 0 auto;
        }}

        .logo {{
            text-align: center;
            margin-bottom: 0.4rem;
        }}

        .logo img {{
            width: 160px;
        }}

        h1 {{
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1.8rem;
            text-align: center;
        }}

        h2 {{
            font-size: 1.2rem;
            font-weight: 400;
            font-style: italic;
            color: var(--accent);
            text-align: center;
            margin-bottom: 0.5rem;
        }}

        h5 {{
            font-size: 0.85rem;
            font-weight: 400;
            color: var(--muted);
            text-align: center;
            margin-bottom: 2.5rem;
        }}

        h4 {{
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 2.5rem;
            margin-bottom: 0.75rem;
        }}

        p {{
            margin-bottom: 1.25rem;
            font-size: 1.05rem;
        }}

        a {{
            color: var(--text);
            text-decoration: underline;
            text-underline-offset: 3px;
        }}

        a:hover {{
            color: var(--muted);
        }}

        /* Collapsible prompt */
        .prompt-toggle {{
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #f5f5f0;
            margin: 0 0 2.5rem;
            font-size: 0.9rem;
            color: var(--accent);
        }}

        .prompt-toggle summary {{
            list-style: none;
            cursor: pointer;
            padding: 0.75rem 1.1rem;
            user-select: none;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
        }}

        .prompt-toggle summary::-webkit-details-marker {{
            display: none;
        }}

        .prompt-toggle summary::before {{
            content: "▸";
            display: inline-block;
            transition: transform 0.25s ease;
            color: var(--muted);
            font-size: 0.85rem;
        }}

        .prompt-toggle[open] summary::before {{
            transform: rotate(90deg);
        }}

        .prompt-body {{
            padding: 0 1.25rem 1.1rem;
            font-size: 0.92rem;
            line-height: 1.65;
            color: var(--accent);
            border-top: 1px solid #e4e4dc;
            padding-top: 1rem;
            margin-top: 0.2rem;
        }}

        .prompt-body p {{
            font-size: 0.92rem;
            margin-bottom: 0.9rem;
        }}

        /* Section break glyph */
        .break {{
            text-align: center;
            color: var(--muted);
            margin: 2.6rem 0;
            letter-spacing: 0.6em;
        }}

        .chapter-heading {{
            font-size: 1.55rem;
            font-weight: 700;
            color: var(--text);
            text-align: center;
            margin: 3.4rem auto 1.1rem;
            line-height: 1.25;
        }}

        /* Caption-only figures — image slots deliberately unfilled */
        .figcap {{
            font-size: 0.92rem;
            line-height: 1.6;
            color: var(--accent);
            background: #faf9f5;
            border-left: 2px solid #ddd9cf;
            padding: 0.85rem 1.1rem;
            margin: 2.2rem 0 1.6rem;
        }}

        .figno {{
            font-variant: small-caps;
            letter-spacing: 0.06em;
            color: var(--muted);
        }}

        /* The taxonomy register intruding on perception */
        .tax {{
            text-align: center;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
            color: var(--muted);
            margin: 1.9rem 0;
        }}

        .sysline {{
            text-align: center;
            font-size: 1rem;
            color: var(--accent);
            margin: 1.7rem 0;
        }}

        /* A character's own unspoken line — not the machine's register */
        .interior {{
            padding-left: 2.2rem;
            color: var(--accent);
            margin: 1.5rem 0;
        }}

        .bio,
        .funding,
        .related {{
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #ddd;
        }}

        .bio h4,
        .funding h4,
        .related h4 {{
            margin-top: 0;
            font-size: 1rem;
        }}

        .bio p,
        .funding p,
        .related p {{
            font-size: 0.92rem;
            color: var(--accent);
        }}

        .story-meta {{
            color: var(--muted);
            font-size: 0.85rem;
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
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 1.25rem 1rem;
            }}

            h1 {{
                font-size: 1.9rem;
            }}

            h2 {{
                font-size: 1.05rem;
            }}
        }}
    </style>
</head>

<body>

    <!-- Logo -->
    <div class="logo">
        <a target="_blank" href="https://glia.ca/">
            <img src="img/glia-bw.webp" alt="Glia.ca — home">
        </a>
    </div>

    <!-- Title -->
    <h1>Interim Edge</h1>

    <!-- Subtitle -->
    <h2>A neurosymbolic narrative generated using the <a href="https://jhave.github.io/narracode/">Narracode
            harness</a>.</h2>

    <!-- Byline -->
    <h5>Jhave (seed paragraph, direction, constraints, edits) &nbsp;·&nbsp; Claude Opus 5 — AUTO_MODE (Initiator,
        Structural, Compositional, Reflexive) via Narracode harness &nbsp;·&nbsp; 2026-07-30 &nbsp;·&nbsp; ≈{wordcount:,} words</h5>

    <!-- Collapsible prompt -->
    <details class="prompt-toggle">
        <summary>prompt</summary>
        <div class="prompt-body">
{PROMPT}
        </div>
    </details>

    <!-- Story -->
    <div class="story">

{STORY}

    </div>

    <hr>
    <!-- Logo -->
    <div class="logo">
        <a target="_blank" href="https://glia.ca/">
            <img src="img/glia-bw.webp" alt="Glia.ca — home">
        </a>
    </div>

    <!-- Other Works by Narracode -->
    <div class="related">
        <h4>Other Works by Narracode</h4>
        <p style="line-height: 1.8;">
{RELATED}
        </p>
    </div>

    <!-- Related Works by Jhave -->
    <div class="related">
        <h4>Related Works by Jhave</h4>
        <p style="line-height: 1.8;">
            <a target="_blank" href="https://glia.ca/2026/inheritors/">The Inheritors: Neanderthals met Sapiens ⟶
                Sapiens meet AGI</a> (April 21, 2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2026/calyx7/">The Long Afternoon: a semi-autonomous model obstructs
                thermonuclear war.</a> (April 20, 2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2026/sffai/">Seeds for Future AI</a> (March 12,
            2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2026/ai/Good-Light.html">The Good Light: an anecdote about grief |
                Written with Claude Opus 4.6.</a> (Feb 11, 2026)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/gentle/">Artificial Gentle Intelligence (AGI)</a> (May 22,
            2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/stim/">StimVerse Draft</a> (April 1 &amp; 20–21,
            2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/ghir/">GHIR: Global Health Immune Response</a> (March 7,
            2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/mai/">Matriarchal AI</a> (2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/wuai/">#Whole-Use-AI</a> (2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2025/eahe/">Everyone at Home Everywhere</a> (2025)&ensp;·&ensp;<br>
            <a target="_blank" href="https://glia.ca/2023/wise/">Wisdom A.I.</a> (May 2, 2023)
        </p>
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

</html>
"""

(ROOT / "index.html").write_text(TEMPLATE, encoding="utf-8")
print("wrote", ROOT / "index.html", "|", wordcount, "story words")
