#!/usr/bin/env python3
"""Character-name census across the Narracode corpus.

Reuse of a distinctive character name across stories is a tell. A reader who
follows the corpus meets the same rare first name in two unrelated works and
correctly infers a shared generator rather than a shared world. Common names
(Anna, Tom) carry no such signal; rare ones (Ines, Kwesi, Salome) carry it
strongly, and the rarer the name the fewer reuses it takes.

Usage:
    python3 tools/name_census.py                 # collisions only
    python3 tools/name_census.py --all           # full per-story census
    python3 tools/name_census.py --story Vetch   # one story's names
"""

import argparse
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "Stories written with Narracode"

# Capitalised tokens that are not personal names. Extend as the corpus grows.
STOP = set(
    """
A An The And But Or If So Then Not No Yes Of In On At To For From With By As It He She They We I You
This That These Those There Here When Where What Who Why How All Some Any Each Every Both Neither
Monday Tuesday Wednesday Thursday Friday Saturday Sunday January February March April May June July
August September October November December
Mr Mrs Ms Dr Prof Sir Madam
Ok Okay Yeah Yep Nope Hey Hi Hello Please Thanks Thank Sorry Well Now Later Today Tomorrow Yesterday
Nobody Somebody Anybody Everybody Nothing Something Anything Everything Someone Anyone Everyone
Did Does Doing Done Can Could Will Would Shall Should May Might Must Have Has Had Was Were Been Being
Same Such Only Just Even Still Yet Once Twice Again Never Always Often Sometimes Perhaps Maybe
After Before During Until Since While Because Although Though Unless However Instead Meanwhile
One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Forty Hundred Thousand
Are Is Am Be Do Don Didn Isn Aren Wasn Weren Won Wouldn Couldn Shouldn
First Second Third Fourth Fifth Last Next Another Other Others Most Least More Less Many Few
Read Write Look Take Give Make Come Go Get Put Let See Say Tell Ask Know Think Feel Want Need Try
God Christ Jesus Lord
AI LLM API URL HTTP GPU CPU UTC NAV EXIF TTL CDN KV
Global Cluster Events Trend Converged Week Summary Severity Duration Action Class Status Current New
North South East West Northern Southern Eastern Western
"""
    .split()
)

# Place names and institutions in the corpus. These recur legitimately.
PLACES = set(
    """
Ytre Arna Bergen Oslo Stavanger Askoy Askøy Norway Norwegian Amsterdam Singapore Tromso Tromsø
Lagos Gaza Stavern Trondheim Ghent Kyoto Leipzig Tunis Paulo California America American Canada
England English Portuguese Spiralist Spiralism Moltboard Narracode Vetch NAV Kirkens Bymisjon
Red Cross Wordsworth Butler Chiang Blake Shannon Slepian Wolf Ker Zeigarnik
Factory Slack GitHub
Bureau Company Section Portfolio Meridian Registry Institute Ministry Board Panel Committee Council
Fig Table Movement Act Scene Part Chapter Appendix Abstract Keywords Theorem Proposition Lemma
"""
    .split()
)

IGNORE = STOP | PLACES

NAME_RE = re.compile(r"\b([A-Z][a-z]{2,})\b")
SENT_START_RE = re.compile(r"(?:^|[.!?\"'“‘]\s+|\n\s*|\*\s*|—\s*|-\s*)$")


def story_dirs():
    if not CORPUS.is_dir():
        sys.exit(f"corpus not found: {CORPUS}")
    return sorted(d for d in CORPUS.iterdir() if d.is_dir())


def draft_files(story):
    """Current drafts only. versions/ holds snapshots and would double-count."""
    drafts = story / "drafts"
    if not drafts.is_dir():
        return []
    return sorted(p for p in drafts.glob("*.md") if "versions" not in p.parts)


def extract(text, total, midsentence):
    """Tally capitalised tokens and note which are ever seen mid-sentence.

    A word appearing mid-sentence is a name. One only ever seen after a full
    stop is probably a sentence opener. Filtering must happen after the whole
    story is tallied, not per file -- a name can be sentence-initial throughout
    one file and mid-sentence in the next.
    """
    for m in NAME_RE.finditer(text):
        word = m.group(1)
        if word in IGNORE:
            continue
        total[word] += 1
        if not SENT_START_RE.search(text[max(0, m.start() - 3) : m.start()]):
            midsentence[word] += 1


def census():
    out = {}
    for story in story_dirs():
        files = draft_files(story)
        if not files:
            continue
        total, mid = collections.Counter(), collections.Counter()
        for f in files:
            extract(f.read_text(encoding="utf-8"), total, mid)
        # A character is named more than twice; one-offs are usually incidental.
        out[story.name] = collections.Counter(
            {w: c for w, c in total.items() if c >= 3 and mid[w] >= 1}
        )
    return out


def collisions(data):
    where = collections.defaultdict(dict)
    for story, counts in data.items():
        for name, n in counts.items():
            where[name][story] = n
    return {n: s for n, s in where.items() if len(s) > 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="print the full census")
    ap.add_argument("--story", help="substring of one story folder")
    args = ap.parse_args()

    data = census()

    if args.story:
        for story, counts in data.items():
            if args.story.lower() in story.lower():
                print(f"\n{story}")
                for name, n in counts.most_common():
                    print(f"  {n:4d}  {name}")
        return

    if args.all:
        for story, counts in sorted(data.items()):
            print(f"\n{story}  ({len(counts)} names)")
            for name, n in counts.most_common(20):
                print(f"  {n:4d}  {name}")
        print()

    hits = collisions(data)
    if not hits:
        print("No cross-story name collisions.")
        return

    print(f"\n=== CROSS-STORY COLLISIONS ({len(hits)}) ===")
    print("Ranked by peak count. A name carrying a lead role in two stories is the")
    print("worst case; a name incidental in both is usually harmless.\n")
    for name, stories in sorted(hits.items(), key=lambda kv: -max(kv[1].values())):
        peak = max(stories.values())
        flag = "  <-- RENAME" if peak >= 10 else ""
        print(f"{name}{flag}")
        for story, n in sorted(stories.items(), key=lambda kv: -kv[1]):
            print(f"     {n:4d}  {story}")
        print()


if __name__ == "__main__":
    main()
