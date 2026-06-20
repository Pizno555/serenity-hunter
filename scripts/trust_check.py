#!/usr/bin/env python3
"""Trust check gate for serenity-hunter.

Audits scripts for dangerous patterns: hardcoded secrets, excessive
permissions, undocumented network access, and unsafe file operations.

Usage:
  python scripts/trust_check.py
  python scripts/trust_check.py --scripts-dir scripts/
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DANGEROUS_PATTERNS = [
    (r"subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True", "HIGH", "Shell execution with shell=True"),
    (r"os\.system\s*\(", "HIGH", "Direct os.system call"),
    (r"eval\s*\(", "HIGH", "Dynamic eval() call"),
    (r"exec\s*\(", "HIGH", "Dynamic exec() call"),
    (r"__import__\s*\(", "HIGH", "Dynamic __import__ call"),
    (r"pickle\.loads?\s*\(", "MEDIUM", "Pickle deserialization (code injection risk)"),
    (r"\b(sk-|api_key|apikey|secret|password|token)\s*=\s*['\"][^'\"]{8,}['\"]", "HIGH", "Hardcoded secret/API key"),
    (r"requests\.(get|post|put|delete)\s*\(", "LOW", "Network request — verify URL is intentional"),
    (r"urllib\.request\.urlopen\s*\(", "LOW", "Network request — verify URL is intentional"),
    (r"open\s*\([^)]*['\"]w['\"]", "LOW", "File write operation — verify path is safe"),
    (r"shutil\.rmtree\s*\(", "HIGH", "Recursive directory deletion"),
    (r"os\.remove\s*\(", "MEDIUM", "File deletion"),
    (r"\bchmod\s*\(", "MEDIUM", "Permission change"),
    (r"\bchown\s*\(", "MEDIUM", "Ownership change"),
]

REQUIRED_DOCS = [
    (r"^#!/usr/bin/env python3", "Shebang line"),
    (r'^""".*?"""', "Module docstring"),
    (r"Usage:", "Usage section in docstring"),
    (r"if __name__\s*==\s*['\"]__main__['\"]", "Main guard"),
]


def check_script(path: Path) -> list[tuple[str, str, str]]:
    """Check a single Python script for trust issues."""
    issues = []
    text = path.read_text(encoding="utf-8")
    rel_path = str(path)

    # Remove string literals and comments before scanning for dangerous patterns
    # This prevents false positives from regex patterns that mention eval/exec etc.
    scan_text = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', '""', text, flags=re.DOTALL)
    scan_text = re.sub(r'#.*$', '', scan_text, flags=re.MULTILINE)

    for pattern, severity, desc in DANGEROUS_PATTERNS:
        matches = re.findall(pattern, scan_text, re.IGNORECASE | re.MULTILINE)
        if matches:
            issues.append((severity, rel_path, f"{desc} ({len(matches)} occurrence(s))"))

    # Check docs on original text (strings included)
    for pattern, desc in REQUIRED_DOCS:
        if not re.search(pattern, text, re.MULTILINE | re.DOTALL):
            issues.append(("INFO", rel_path, f"Missing: {desc}"))

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Trust check gate")
    parser.add_argument("--scripts-dir", default="scripts")
    args = parser.parse_args()

    scripts_dir = Path(args.scripts_dir)
    if not scripts_dir.exists():
        print(f"ERROR: scripts directory not found: {scripts_dir}")
        sys.exit(1)

    all_issues = []
    for py_file in sorted(scripts_dir.glob("*.py")):
        all_issues.extend(check_script(py_file))

    high = [i for i in all_issues if i[0] == "HIGH"]
    medium = [i for i in all_issues if i[0] == "MEDIUM"]
    low = [i for i in all_issues if i[0] == "LOW"]
    info = [i for i in all_issues if i[0] == "INFO"]

    print("Trust Check Report")
    print("==================")
    print(f"HIGH: {len(high)}  MEDIUM: {len(medium)}  LOW: {len(low)}  INFO: {len(info)}")
    print()

    for sev, path, msg in all_issues:
        print(f"  [{sev}] {path}: {msg}")

    print()
    if high:
        print(f"RESULT: FAIL — {len(high)} HIGH severity issues must be fixed")
        sys.exit(1)
    elif medium:
        print(f"RESULT: PASS WITH WARNINGS — {len(medium)} MEDIUM issues to review")
        sys.exit(0)
    else:
        print("RESULT: PASS — no HIGH or MEDIUM trust issues")
        sys.exit(0)


if __name__ == "__main__":
    main()
