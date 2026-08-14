#!/usr/bin/env python3
"""Obligation salience and reader-pressure curves.

Experiment 1 of plans/2026-08-14_physics-graph-llm-ensemble.md.

An obligation is not a binary. A planted detail is vivid in the reader's hands
for a scene or two and then fades. This computes that fading, so the shape of a
finished piece can be looked at after the fact.

The model is one line:

    salience *= 0.5 ** (1 / half_life)     for every scene that does not touch it
    salience  = 1.0                        for every scene that does

Nothing here is a target. It is a reading taken afterwards. See the harness,
"Measurement belongs to the outer loop."

Input format --- in structural/obligations.md, under `## Active`:

    - **The balloon** --- fourth-floor landing, fuller each week.
      planted: s3 | half-life: 3 | probes: balloon, landing

`probes` are the regexes used to detect a touch in a scene's text. Declaring
them in the file is the point: touch detection is reproducible and auditable
rather than recalled. Omit `probes` and the entry is scored from `last-touched`
alone. `planted` defaults to the first scene a probe fires in.

Usage
    obligation_pressure.py STORY_DIR --draft drafts/7-condensed-final.md
    obligation_pressure.py STORY_DIR --draft ... --csv out.csv --plot out.png
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

FADED_FLOOR = 0.1
DEFAULT_HALF_LIFE = 3.0

FIELD_RE = re.compile(
    r"^\s*(?:planted|half-life|last-touched|probes|salience)\s*:", re.IGNORECASE
)
# Scene headings: "## 4 --- patriot, dormant", "## Section 4", "# 4".
SCENE_RE = re.compile(r"^#{1,3}\s+(?:section\s+|scene\s+|§\s*)?(\d+)\b", re.IGNORECASE)


@dataclass
class Obligation:
    label: str
    text: str
    half_life: float = DEFAULT_HALF_LIFE
    planted: int | None = None
    last_touched: int | None = None
    probes: list[str] = field(default_factory=list)
    salience: float = 0.0
    touches: list[int] = field(default_factory=list)
    faded_at: int | None = None

    def touched_by(self, scene_text: str) -> bool:
        low = scene_text.lower()
        for probe in self.probes:
            try:
                if re.search(probe.lower(), low):
                    return True
            except re.error as exc:
                # A malformed probe is an authoring error in obligations.md, not
                # a reason to lose the whole run. Report it and treat as no match.
                print(f"warning: bad probe {probe!r} on {self.label!r}: {exc}",
                      file=sys.stderr)
        return False


def _parse_fields(line: str, ob: Obligation) -> None:
    for chunk in re.split(r"\s+[|·]\s+", line.strip()):
        if ":" not in chunk:
            continue
        key, _, val = chunk.partition(":")
        key, val = key.strip().lower(), val.strip()
        if key == "planted":
            ob.planted = _scene_num(val)
        elif key == "last-touched":
            ob.last_touched = _scene_num(val)
        elif key == "half-life":
            try:
                ob.half_life = float(val)
            except ValueError:
                pass
        elif key == "probes":
            ob.probes = [p.strip() for p in val.split(",") if p.strip()]


def _scene_num(val: str) -> int | None:
    m = re.search(r"\d+", val)
    return int(m.group()) if m else None


def parse_obligations(path: Path, sections: tuple[str, ...]) -> list[Obligation]:
    """Read every `- ` bullet under any heading matching `sections`."""
    obs: list[Obligation] = []
    active = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("#"):
            head = raw.lstrip("#").strip().lower()
            active = any(s in head for s in sections)
            continue
        if not active:
            continue
        if raw.lstrip().startswith("- "):
            body = raw.lstrip()[2:].strip()
            m = re.match(r"\*\*(.+?)\*\*", body)
            label = m.group(1) if m else body[:48].rstrip(" .,—-")
            obs.append(Obligation(label=label, text=body))
        elif obs and FIELD_RE.match(raw):
            _parse_fields(raw, obs[-1])
    return obs


def scenes_from_files(paths: list[Path]) -> list[tuple[int, str]]:
    """One file per scene, ordered by any leading integer in the filename."""
    def key(p: Path) -> tuple[int, str]:
        m = re.match(r"(\d+)", p.name)
        return (int(m.group(1)) if m else 10**6, p.name)

    return [
        (i, p.read_text(encoding="utf-8"))
        for i, p in enumerate(sorted(paths, key=key), start=1)
    ]


def split_scenes(draft: Path) -> list[tuple[int, str]]:
    """Split a draft into (scene_number, text). Falls back to `---` rules."""
    lines = draft.read_text(encoding="utf-8").splitlines()
    scenes: list[tuple[int, list[str]]] = []
    for line in lines:
        m = SCENE_RE.match(line)
        if m:
            scenes.append((int(m.group(1)), []))
        elif scenes:
            scenes[-1][1].append(line)
    if not scenes:
        print("warning: no scene headings matched; treating whole draft as one scene",
              file=sys.stderr)
        return [(0, "\n".join(lines))]
    return [(n, "\n".join(body)) for n, body in scenes]


def run(obs: list[Obligation], scenes: list[tuple[int, str]]) -> list[dict]:
    """Walk the scenes in order, applying the decay rule. Returns per-scene rows."""
    decay_from = {ob.label: None for ob in obs}
    rows = []

    for idx, (num, text) in enumerate(scenes):
        faded_here = []
        for ob in obs:
            hit = ob.touched_by(text) if ob.probes else (ob.last_touched == num)

            if hit:
                if ob.planted is None:
                    ob.planted = num
                ob.touches.append(num)
                ob.last_touched = num
                ob.salience = 1.0
                ob.faded_at = None
                decay_from[ob.label] = idx
                continue

            # Not touched. Only decays once the reader is holding it.
            planted_idx = next(
                (i for i, (n, _) in enumerate(scenes) if n == ob.planted), None
            )
            if planted_idx is None or idx < planted_idx:
                ob.salience = 0.0
                continue
            if decay_from[ob.label] is None:
                decay_from[ob.label] = planted_idx
                ob.salience = 1.0
            ob.salience *= 0.5 ** (1.0 / max(ob.half_life, 1e-6))
            if ob.salience < FADED_FLOOR and ob.faded_at is None:
                ob.faded_at = num
                faded_here.append(ob.label)

        live = [o for o in obs if o.salience >= FADED_FLOOR]
        rows.append(
            {
                "scene": num,
                "live": len(live),
                "total_salience": round(sum(o.salience for o in live), 3),
                "mean_salience": round(
                    sum(o.salience for o in live) / len(live), 3
                ) if live else 0.0,
                "touched": sum(1 for o in obs if o.touches and o.touches[-1] == num),
                "faded_this_scene": "; ".join(faded_here),
            }
        )
    return rows


def plot(rows: list[dict], obs: list[Obligation], scenes, out: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping plot", file=sys.stderr)
        return

    xs = [r["scene"] for r in rows]
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 8), sharex=True, gridspec_kw={"height_ratios": [2, 3]}
    )

    ax1.plot(xs, [r["total_salience"] for r in rows], marker="o", lw=2, color="#1f3a5f")
    ax1.fill_between(xs, [r["total_salience"] for r in rows], alpha=0.15, color="#1f3a5f")
    ax1.set_ylabel("total live salience")
    ax1.set_title("Reader pressure — total obligation salience per scene")
    ax1.grid(alpha=0.25)

    # Per-obligation trace, recomputed for display.
    for ob in obs:
        # Gaps (None) before the obligation is planted: the reader is not yet
        # holding it, so there is no line to draw.
        trace, sal, started = [], 0.0, False
        for num, text in scenes:
            hit = ob.touched_by(text) if ob.probes else (ob.last_touched == num)
            if hit:
                sal, started = 1.0, True
            elif started:
                sal *= 0.5 ** (1.0 / max(ob.half_life, 1e-6))
            trace.append(sal if started else None)
        ax2.plot(xs, trace, marker=".", lw=1.2, alpha=0.8, label=ob.label[:34])

    ax2.axhline(FADED_FLOOR, ls="--", lw=1, color="#999")
    ax2.text(xs[0], FADED_FLOOR + 0.02, "faded", fontsize=8, color="#666")
    ax2.set_xlabel("scene")
    ax2.set_ylabel("salience")
    ax2.set_ylim(0, 1.05)
    ax2.grid(alpha=0.25)
    ax2.legend(fontsize=7, ncol=2, loc="upper right", framealpha=0.9)

    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("story", type=Path, help="story folder")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--draft", help="single draft file, relative to story folder")
    g.add_argument("--drafts-glob", help="glob for one-file-per-scene, e.g. 'drafts/*.md'")
    ap.add_argument("--obligations", default="structural/obligations.md")
    ap.add_argument("--sections", default="active,added",
                    help="comma-separated obligations.md headings to read")
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--plot", type=Path)
    args = ap.parse_args()

    ob_path = args.story / args.obligations
    if not ob_path.exists():
        print(f"error: {ob_path} not found", file=sys.stderr)
        return 1

    if args.drafts_glob:
        paths = sorted(args.story.glob(args.drafts_glob))
        if not paths:
            print(f"error: no files match {args.drafts_glob}", file=sys.stderr)
            return 1
        scene_src = lambda: scenes_from_files(paths)
    else:
        draft = args.story / args.draft
        if not draft.exists():
            print(f"error: {draft} not found", file=sys.stderr)
            return 1
        scene_src = lambda: split_scenes(draft)

    sections = tuple(s.strip().lower() for s in args.sections.split(","))
    obs = parse_obligations(ob_path, sections)
    if not obs:
        print(f"error: no obligations parsed from {ob_path}", file=sys.stderr)
        return 1
    scenes = scene_src()
    rows = run(obs, scenes)

    print(f"\n{args.story.name} — {len(obs)} obligations, {len(scenes)} scenes\n")
    print(f"{'scene':>5} {'live':>5} {'total':>7} {'mean':>6} {'touched':>8}  faded")
    for r in rows:
        print(f"{r['scene']:>5} {r['live']:>5} {r['total_salience']:>7.2f} "
              f"{r['mean_salience']:>6.2f} {r['touched']:>8}  {r['faded_this_scene']}")

    never = [o.label for o in obs if not o.touches]
    if never:
        print(f"\nnever touched by any probe ({len(never)}): {', '.join(never)}")
    once = [o.label for o in obs if len(o.touches) == 1]
    if once:
        print(f"touched exactly once ({len(once)}): {', '.join(once)}")

    if args.csv:
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {args.csv}")
    if args.plot:
        plot(rows, obs, scenes, args.plot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
