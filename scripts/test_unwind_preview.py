#!/usr/bin/env python3
"""Mechanical test suite for unwind-preview.py.

Builds tiny temp wikis on disk, runs the script via subprocess from the
temp dir, asserts on stdout. Exits 0 if all pass, 1 otherwise.

Run:
  python3 scripts/test_unwind_preview.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "unwind-preview.py"
passed = 0
failed = 0
failures: list[str] = []


def run(cwd: Path, *args: str) -> tuple[int, str, str]:
    p = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
    return p.returncode, p.stdout, p.stderr


def make_wiki(root: Path, pages: dict[str, str]) -> None:
    (root / "wiki").mkdir()
    for name, body in pages.items():
        _ = (root / "wiki" / f"{name}.md").write_text(body)


def check(name: str, cond: bool, detail: str = "") -> None:
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        failures.append(f"{name}: {detail}")
        print(f"  FAIL: {name} — {detail}")


def test_missing_wiki_dir() -> None:
    with tempfile.TemporaryDirectory() as td:
        rc, _out, err = run(Path(td), "anything")
        check("missing wiki dir exits non-zero", rc != 0, f"rc={rc}")
        check("missing wiki dir mentions path", "wiki dir not found" in err, err)


def test_sole_source_classified_as_delete() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        make_wiki(root, {
            "concept-a": '---\ntype: concept\nsources:\n  - "[[target]]"\n---\n\nbody',
        })
        _rc, out, _err = run(root, "target")
        check("sole-source classified delete", "delete" in out.lower() and "concept-a" in out, out)


def test_multi_sourced_classified_as_scrub() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        make_wiki(root, {
            "concept-b": '---\ntype: concept\nsources:\n  - "[[target]]"\n  - "[[other]]"\n---\n\nbody',
        })
        _rc, out, _err = run(root, "target")
        check("multi-source classified scrub", "scrub" in out.lower() and "concept-b" in out, out)


def test_inbound_link_detected() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        make_wiki(root, {
            "concept-c": '---\ntype: concept\nsources:\n  - "[[other]]"\n---\n\nSee [[target]] for details.',
        })
        _rc, out, _err = run(root, "target")
        check("inbound link detected", "inbound" in out.lower() and "concept-c" in out, out)


def test_unrelated_pages_ignored() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        make_wiki(root, {
            "unrelated": '---\ntype: concept\nsources:\n  - "[[other]]"\n---\n\nNothing about target here.',
        })
        _rc, out, _err = run(root, "target")
        check("unrelated pages ignored", "unrelated" not in out, out)


def main() -> int:
    print("Running test_unwind_preview.py")
    test_missing_wiki_dir()
    test_sole_source_classified_as_delete()
    test_multi_sourced_classified_as_scrub()
    test_inbound_link_detected()
    test_unrelated_pages_ignored()
    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
