#!/usr/bin/env python3
"""Resource boundary check gate for serenity-hunter.

Verifies that the skill stays within reasonable context budget and
resource boundaries. Checks file sizes, total context weight, and
reference loading discipline.

Usage:
  python scripts/resource_boundary_check.py
  python scripts/resource_boundary_check.py --root . --max-skill-kb 8 --max-ref-kb 15
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Context budget tiers (in KB)
DEFAULT_MAX_SKILL_KB = 8       # SKILL.md should stay compact
DEFAULT_MAX_REF_KB = 15        # Individual reference files
DEFAULT_MAX_TOTAL_KB = 80      # All loadable files combined
DEFAULT_MAX_SCRIPT_KB = 12     # Individual scripts


def file_size_kb(path: Path) -> float:
    """Get file size in KB."""
    return path.stat().st_size / 1024.0


def check_skill_md(root: Path, max_kb: float) -> list[tuple[str, str, str]]:
    """Check SKILL.md size."""
    issues = []
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        return [("FAIL", "SKILL.md", "File not found")]

    size = file_size_kb(skill_path)
    if size > max_kb:
        issues.append(("FAIL", "SKILL.md", f"{size:.1f}KB exceeds {max_kb}KB budget — trim duplicated content"))
    elif size > max_kb * 0.8:
        issues.append(("WARN", "SKILL.md", f"{size:.1f}KB is near {max_kb}KB budget"))
    else:
        issues.append(("PASS", "SKILL.md", f"{size:.1f}KB within {max_kb}KB budget"))

    return issues


def check_references(root: Path, max_kb: float) -> list[tuple[str, str, str]]:
    """Check reference file sizes."""
    issues = []
    ref_dir = root / "references"
    if not ref_dir.exists():
        return [("WARN", "references/", "Directory not found")]

    for md_file in sorted(ref_dir.glob("*.md")):
        size = file_size_kb(md_file)
        rel = f"references/{md_file.name}"
        if size > max_kb:
            issues.append(("WARN", rel, f"{size:.1f}KB exceeds {max_kb}KB — consider splitting"))
        else:
            issues.append(("PASS", rel, f"{size:.1f}KB"))

    return issues


def check_scripts(root: Path, max_kb: float) -> list[tuple[str, str, str]]:
    """Check script file sizes."""
    issues = []
    script_dir = root / "scripts"
    if not script_dir.exists():
        return [("WARN", "scripts/", "Directory not found")]

    for py_file in sorted(script_dir.glob("*.py")):
        size = file_size_kb(py_file)
        rel = f"scripts/{py_file.name}"
        if size > max_kb:
            issues.append(("WARN", rel, f"{size:.1f}KB exceeds {max_kb}KB — consider refactoring"))
        else:
            issues.append(("PASS", rel, f"{size:.1f}KB"))

    return issues


def check_total_context(root: Path, max_kb: float) -> list[tuple[str, str, str]]:
    """Check total loadable context weight."""
    issues = []
    total = 0.0
    files_checked = 0

    for pattern in ["SKILL.md", "references/*.md", "assets/*.md", "assets/*.json"]:
        for f in root.glob(pattern):
            if f.is_file():
                total += file_size_kb(f)
                files_checked += 1

    if total > max_kb:
        issues.append(("WARN", "total_context", f"{total:.1f}KB across {files_checked} files exceeds {max_kb}KB budget"))
    else:
        issues.append(("PASS", "total_context", f"{total:.1f}KB across {files_checked} files within {max_kb}KB budget"))

    return issues


def check_load_on_demand_discipline(root: Path) -> list[tuple[str, str, str]]:
    """Verify SKILL.md uses load-on-demand instead of inlining reference content."""
    issues = []
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")

    # SKILL.md should reference files, not inline their content
    ref_count = skill_text.count("references/")
    if ref_count < 3:
        issues.append(("WARN", "SKILL.md", f"Only {ref_count} reference paths — may be inlining content instead of loading on demand"))

    # Check for 8-layer checklist inline (should be in references only)
    if "end customers, system integrators" in skill_text:
        issues.append(("FAIL", "SKILL.md", "8-layer value chain checklist inlined — move to references/"))

    # Check for scorecard weights inlined
    if "demand_inflection" in skill_text and "chokepoint_severity" in skill_text:
        issues.append(("FAIL", "SKILL.md", "Scorecard factor names inlined — move to scripts/"))

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Resource boundary check gate")
    parser.add_argument("--root", default=".")
    parser.add_argument("--max-skill-kb", type=float, default=DEFAULT_MAX_SKILL_KB)
    parser.add_argument("--max-ref-kb", type=float, default=DEFAULT_MAX_REF_KB)
    parser.add_argument("--max-script-kb", type=float, default=DEFAULT_MAX_SCRIPT_KB)
    parser.add_argument("--max-total-kb", type=float, default=DEFAULT_MAX_TOTAL_KB)
    args = parser.parse_args()

    root = Path(args.root)

    all_issues = []
    all_issues.extend(check_skill_md(root, args.max_skill_kb))
    all_issues.extend(check_references(root, args.max_ref_kb))
    all_issues.extend(check_scripts(root, args.max_script_kb))
    all_issues.extend(check_total_context(root, args.max_total_kb))
    all_issues.extend(check_load_on_demand_discipline(root))

    fails = [i for i in all_issues if i[0] == "FAIL"]
    warns = [i for i in all_issues if i[0] == "WARN"]
    passes = [i for i in all_issues if i[0] == "PASS"]

    print("Resource Boundary Check Report")
    print("===============================")
    print(f"PASS: {len(passes)}  WARN: {len(warns)}  FAIL: {len(fails)}")
    print()

    for sev, path, msg in all_issues:
        if sev != "PASS":
            print(f"  [{sev}] {path}: {msg}")

    print()
    if fails:
        print(f"RESULT: FAIL — {len(fails)} boundary violations")
        sys.exit(1)
    elif warns:
        print(f"RESULT: PASS WITH WARNINGS — {len(warns)} warnings to review")
        sys.exit(0)
    else:
        print("RESULT: PASS — all resource boundaries respected")
        sys.exit(0)


if __name__ == "__main__":
    main()
