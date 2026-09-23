#!/usr/bin/env python3
"""
prose_audit.py — a suspicion engine for the Chauffé Éclairé register.

Companion to tillman_check.py, which measures prosody. This one measures nothing.
It reports things a careful reader would stop on, and leaves the judgement to the reader.

Built 2026-08-23 from jhave's line-notes on chapter 3, each of which he found by eye.
Every check here exists because a human caught something the prosody validator could not
see. The checks are deliberately noisy: a hit is a place to look, not a verdict.

    python3 tools/prose_audit.py draft.md
    python3 tools/prose_audit.py draft.md --only=vagueness,numbers
"""

import re, sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------- lexicons

VAGUE = {
    r"\bthe thing\b": "vague noun — name it",
    r"\bthings\b": "vague noun — name them",
    r"\bsomething\b": "vague — unless it is characterising someone else's job",
    r"\bsomehow\b": "vague connective",
    r"\bsort of\b": "hedge",
    r"\bkind of\b": "hedge",
    r"\ba bit\b": "hedge",
    r"\bsome kind of\b": "hedge",
    r"\bin a way\b": "hedge",
}

ABSOLUTES = {
    r"\bthe only reason\b": "absolute",
    r"\bexactly how\b": "absolute",
    r"\bevery (?:woman|man|one of|time|single)\b": "absolute",
    r"\bnever in my life\b": "absolute",
    r"\balways\b": "absolute",
    r"\bcompletely\b": "intensifier",
    r"\btotally\b": "intensifier",
    r"\bentirely\b": "intensifier",
    r"\bextremely\b": "intensifier",
}

# jhave: "delete all meta commentary or replace with details.
#         These stories are about stray contingencies and ricochets. Perceptions.
#         They are not stories about stories."
META = {
    r"\bthis is (?:a |not a )?story\b": "META — a story about stories",
    r"\bwhat I want to\b": "META — authorial intent (§22)",
    r"\bI want to (?:be|say|put|note|admit)\b": "META — authorial intent (§22)",
    r"\bwhich is what I\b": "META — authorial intent (§22)",
    r"\bI have thought about\b": "META — think/want pattern",
    r"\bI have decided\b": "META — think/want pattern",
    r"\bI could not tell\b": "META — think/want pattern",
    r"\bI am not going to\b": "META — refusal to narrate",
    r"\bI do not think it was\b": "META — think/want pattern",
    r"\bwhich everybody\b": "vague maxim",
    r"\bnobody believes\b": "vague maxim",
    r"\band none of that was\b": "afterthought comment — compress or cut",
    r"\bwe are the sort of\b": "restates what is already stated",
}

NUMWORDS = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
            "fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|"
            "fifty|sixty|seventy|eighty|ninety|hundred|thousand")

# ---------------------------------------------------------------- parsing

def load(path):
    raw = Path(path).read_text(encoding="utf-8")
    sections = []
    cur_title, cur_body = None, []
    for line in raw.splitlines():
        if line.startswith("## "):
            if cur_title is not None:
                sections.append((cur_title, "\n".join(cur_body)))
            cur_title, cur_body = line[3:].strip(), []
        elif not line.startswith("# "):
            cur_body.append(line)
    if cur_title is not None:
        sections.append((cur_title, "\n".join(cur_body)))
    return raw, sections

def sentences(text):
    out = []
    for p in re.split(r"\n\s*\n", text):
        p = p.strip()
        if not p:
            continue
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+", p) if s.strip()]
    return out

def hits(text, table):
    found = []
    for pat, label in table.items():
        for m in re.finditer(pat, text, re.I):
            lo, hi = max(0, m.start()-52), min(len(text), m.end()+52)
            found.append((label, m.group(0), " ".join(text[lo:hi].split())))
    return found

def rule(title):
    print(f"\n{'─'*72}\n  {title}\n{'─'*72}")

# ---------------------------------------------------------------- checks

def check_vagueness(raw, sections):
    rule("VAGUENESS — replace with a perception, or delete")
    found = hits(raw, VAGUE) + hits(raw, ABSOLUTES)
    if not found:
        print("  clean")
    for label, span, ctx in found:
        print(f"  [{label:44}] «{span}»\n      …{ctx}…")

def check_meta(raw, sections):
    rule("META-COMMENTARY — the story is not about what kind of story it is")
    found = hits(raw, META)
    if not found:
        print("  clean")
    for label, span, ctx in found:
        print(f"  [{label:44}] «{span}»\n      …{ctx}…")

def check_terminal_it(raw, sections):
    rule("SENTENCES ENDING ON 'it' — vagueness where the wit should be")
    n = 0
    for title, body in sections:
        for s in sentences(body):
            if re.search(r"\bit[.,;:]?$", s.strip(), re.I):
                n += 1
                print(f"  §{title.split('.')[0]:>3}  {s.strip()}")
    print(f"\n  total: {n}.  jhave's note: 'another vagueness to replace with wit.'")
    print("  Guide: more than 2 per 1,000 words and the tic is visible.")

def check_numbers(raw, sections):
    rule("NUMERIC REPETITION — 'numbers are not neat and tidy in people'")
    toks = re.findall(rf"\b(\d[\d,]*|{NUMWORDS})\b", raw, re.I)
    norm = [t.lower().replace(",", "") for t in toks]
    counts = Counter(norm)
    ctxs = defaultdict(list)
    for m in re.finditer(rf"\b(\d[\d,]*|{NUMWORDS})\b", raw, re.I):
        v = m.group(0).lower().replace(",", "")
        lo, hi = max(0, m.start()-42), min(len(raw), m.end()+42)
        ctxs[v].append(" ".join(raw[lo:hi].split()))
    flagged = [(v, c) for v, c in counts.most_common() if c >= 3]
    if not flagged:
        print("  no value used three or more times")
    for v, c in flagged:
        print(f"\n  «{v}» × {c}")
        for ctx in ctxs[v][:6]:
            print(f"      …{ctx}…")

def check_density(raw, sections):
    rule("NUMERIC DENSITY — is a number standing where a perception should be? (§31)")
    NUM = rf"\b(\d[\d,.]*|{NUMWORDS}|percent|kroner|euros|dollars)\b"
    words = len(raw.split())
    nums = re.findall(NUM, raw, re.I)
    sents = [s for _, b in sections for s in sentences(b)]
    carrying = [s for s in sents if re.search(NUM, s, re.I)]
    per_k = 1000.0 * len(nums) / words if words else 0
    pct = 100.0 * len(carrying) / len(sents) if sents else 0
    print(f"  {len(nums)} numerals in {words} words  =  {per_k:.1f} per 1,000")
    print(f"  {len(carrying)} of {len(sents)} sentences carry a number  =  {pct:.1f}%")
    print(f"\n  Guide: under 12 per 1,000, under 8% of sentences.")
    print("  Measured in the first four chapters: 48, 33, 37, 26 per 1,000.")
    print("  For each number below, ask: would a person have registered this?\n")
    for s in carrying:
        print(f"    {s.strip()[:96]}")

def check_openers(raw, sections):
    rule("SECTION OPENERS — shape repetition is a formula, not a style")
    for title, body in sections:
        ss = sentences(body)
        if not ss:
            continue
        first = ss[0]
        shape = "NAME + past verb" if re.match(r"^[A-Z][a-zà-ÿ]+ (?:was|had|hauled|picked|came|said|drove|lived|worked|ran)\b", first) else ""
        print(f"  §{title:<28} {first[:76]}")
        if shape:
            print(f"      ↳ shape: {shape}")
    print("\n  Compare shapes. Two the same is a rhyme; three is a template.")

def check_triplets(raw, sections):
    rule("TRIPLET FORMULA — '1; 2.1, 2.2, 2.3; 3'")
    n = 0
    for title, body in sections:
        for s in sentences(body):
            if s.count(";") >= 2 and re.search(r";[^;]*,[^;]*,[^;]*;", s):
                n += 1
                print(f"  §{title.split('.')[0]:>3}  {s[:100]}")
    print(f"\n  total: {n}. The chained intro is the signature; three of them is the tic.")

def check_names(raw, sections):
    rule("RELATIONAL CONTINUITY — who is this, and had we met them?")
    STOP = {"I","The","He","She","It","We","They","They","A","An","And","But","In","On","At",
            "That","This","There","Then","When","What","My","Her","His","Their","Our","No","Not",
            "So","If","One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","By",
            "For","From","With","Of","To","Up","Out","Later","Monday","Tuesday","Wednesday",
            "Thursday","Friday","Saturday","Sunday","January","February","March","April","May",
            "June","July","August","September","October","November","December","Read","Take",
            "Swallow","Wait","Feel","Drive","Sit","Go","Walk","Say","Watch","Pharmacy","Understand"}
    names = defaultdict(list)
    for title, body in sections:
        for s in sentences(body):
            for m in re.finditer(r"\b([A-Z][a-zà-ÿ]{2,})\b", s):
                w = m.group(1)
                if w in STOP:
                    continue
                if m.start() == 0 and w not in names:
                    pass
                names[w].append((title, s))
    people = {w: v for w, v in names.items() if len(v) >= 1}
    for w, occ in sorted(people.items(), key=lambda kv: -len(kv[1])):
        first_sec, first_s = occ[0]
        print(f"  {w:<14} ×{len(occ):<3} first: §{first_sec.split('.')[0]}  {first_s[:66]}")
    print("\n  Check by eye: is anyone referred to as known before they are introduced?")
    print("  Does a callback to an earlier chapter carry enough to land on its own?")

def check_callbacks(raw, sections):
    rule("CALLBACKS — a reference that needs a previous chapter to mean anything")
    pats = [r"\bnine days\b", r"\beleven hundred kilometres\b", r"\bthe way I had come\b",
            r"\bnever used to be\b", r"\blike (?:the|a) (?:Jean Coutu|packing house)\b",
            r"\bsince the\b", r"\bthe same as\b", r"\bagain\b"]
    any_hit = False
    for pat in pats:
        for m in re.finditer(pat, raw, re.I):
            any_hit = True
            lo, hi = max(0, m.start()-60), min(len(raw), m.end()+60)
            print(f"  «{m.group(0)}»  …{' '.join(raw[lo:hi].split())}…")
    if not any_hit:
        print("  none detected")
    print("\n  For each: would a reader who forgot the earlier chapter still be fine?")
    print("  If not, either seat it in the sentence or cut it.")

CHECKS = {
    "vagueness": check_vagueness, "meta": check_meta, "it": check_terminal_it,
    "numbers": check_numbers, "density": check_density, "openers": check_openers, "triplets": check_triplets,
    "names": check_names, "callbacks": check_callbacks,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    path = sys.argv[1]
    only = None
    for a in sys.argv[2:]:
        if a.startswith("--only="):
            only = set(a.split("=", 1)[1].split(","))
    raw, sections = load(path)
    print(f"\n╔══ prose audit: {Path(path).name} — {len(raw.split())} words, {len(sections)} sections")
    print("║  Nothing here is a failure. Every line is a place to look.")
    print("╚" + "═"*70)
    for name, fn in CHECKS.items():
        if only and name not in only:
            continue
        fn(raw, sections)
    print()
