#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Unwind preview: classify pages affected by removing a wiki source.

Usage: run from your wiki repo root:
  unwind-preview.py <source-slug>

Reads frontmatter `sources:` from each wiki/*.md in the current directory's wiki/ subdir and groups pages into:
- delete   — target is the sole source (page is orphaned by the unwind)
- scrub    — target is one of multiple sources (frontmatter + prose edits)
- inbound  — body has [[<target>]] links (need rewording or removal)
"""

import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit("usage: unwind-preview.py <source-slug>")

target = sys.argv[1]
wiki = Path.cwd() / "wiki"
if not wiki.is_dir():
    sys.exit(f"wiki dir not found at {wiki} — run from your karpathy-wiki repo root")

frontmatter_re = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
link_re = re.compile(r"\[\[([a-z0-9-]+)\]\]")


def parse_sources(frontmatter: str) -> list[str]:
    sources: list[str] = []
    in_sources = False
    for line in frontmatter.splitlines():
        if line.startswith("sources:"):
            in_sources = "[" not in line  # inline `sources: []` ends here
            sources.extend(link_re.findall(line))
            continue
        if in_sources:
            if line and line[0] in " \t":
                sources.extend(link_re.findall(line))
            else:
                in_sources = False
    return sources


solely_sourced: list[str] = []
multi_sourced: list[tuple[str, list[str]]] = []

for path in sorted(wiki.glob("*.md")):
    if path.stem in (target, "index", "log"):
        continue
    text = path.read_text()
    fm = frontmatter_re.match(text)
    if not fm:
        continue
    sources = parse_sources(fm.group(1))
    if target not in sources:
        continue
    if len(sources) == 1:
        solely_sourced.append(path.stem)
    else:
        multi_sourced.append((path.stem, [s for s in sources if s != target]))

deletions = {target} | set(solely_sourced)
inbound: list[tuple[str, list[tuple[int, str]]]] = []
for path in sorted(wiki.glob("*.md")):
    if path.stem in deletions or path.stem in ("index", "log"):
        continue
    text = path.read_text()
    needle = f"[[{target}]]"
    if needle not in text:
        continue
    hits = [(i, line) for i, line in enumerate(text.splitlines(), 1) if needle in line]
    inbound.append((path.stem, hits))

print(f"## Punch list — unwind `{target}`\n")

print("### Delete (sole source)")
target_path = wiki / f"{target}.md"
if target_path.exists():
    print(f"- `{target}.md` (the source page itself)")
else:
    print(f"- `{target}.md` (NOTE: source page already absent)")
for s in solely_sourced:
    print(f"- `{s}.md`")
print()

print("### Scrub (multi-sourced — remove from frontmatter, prune target-anchored prose)")
if multi_sourced:
    for s, others in multi_sourced:
        print(f"- `{s}.md` — remaining sources: {', '.join(others)}")
else:
    print("- (none)")
print()

print(f"### Inbound `[[{target}]]` body references (review surrounding prose)")
if inbound:
    for s, hits in inbound:
        for ln, line in hits:
            print(f"- `{s}.md:{ln}` — `{line.strip()}`")
else:
    print("- (none)")
print()

print("### Always also")
print(f"- `wiki/index.md` — remove entry for `{target}` and any deleted concept/entity pages")
print(f"- `wiki/log.md` — append `## [YYYY-MM-DD] unwind | {target} — N deleted, M scrubbed` with sub-bullets")
print(f"- `qmd update && qmd embed` after edits")
