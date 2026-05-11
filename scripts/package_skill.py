#!/usr/bin/env python3
"""
package_skill.py — build a .skill bundle for distribution.

Tars the runtime skill files into karpathy-wiki-skill.skill at the repo
root. Dev-only artifacts (test_unwind_preview.py, this script,
docs/plans/, evals/) are deliberately excluded.

Usage:
  python3 scripts/package_skill.py <repo-root>
"""

from __future__ import annotations

import sys
import tarfile
from pathlib import Path

INCLUDE = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "scripts/unwind-preview.py",
    "references",
]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <repo-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    out = root / "karpathy-wiki-skill.skill"
    with tarfile.open(out, "w:gz") as tf:
        for name in INCLUDE:
            p = root / name
            if not p.exists():
                print(f"warning: skipping missing {name}", file=sys.stderr)
                continue
            tf.add(p, arcname=name)
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
