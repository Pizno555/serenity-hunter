#!/usr/bin/env python3
"""Governance check gate for serenity-hunter.

Verifies that the skill's governance metadata is complete and consistent
with its declared archetype (governed).

Usage:
  python scripts/governance_check.py
  python scripts/governance_check.py --manifest manifest.json --skill SKILL.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GOVERNED_REQUIRED_FIELDS = [
    "name",
    "version",
    "owner",
    "maturity_tier",
    "review_cadence",
    "output_contract",
    "boundaries",
    "rollback_boundary",
    "gates",
]

GOVERNED_REQUIRED_SECTIONS = [
    "governance",
    "input_files",
    "rollback_boundary",
]

SKILL_REQUIRED_SECTIONS = [
    "Core promise",
    "Default behavior",
    "Request router",
    "Research workflow",
    "Risk boundary",
    "Output guards",
    "Load on demand",
]


def check_manifest(manifest_path: str) -> list[tuple[str, str, str]]:
    """Check manifest.json for governed completeness. Returns list of (severity, field, message)."""
    issues = []
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))

    for field in GOVERNED_REQUIRED_FIELDS:
        if field not in data:
            issues.append(("FAIL", field, f"Missing required field: {field}"))

    for section in GOVERNED_REQUIRED_SECTIONS:
        if section not in data:
            issues.append(("FAIL", section, f"Missing governed section: {section}"))

    if data.get("maturity_tier") != "governed":
        issues.append(("FAIL", "maturity_tier", f"Expected 'governed', got '{data.get('maturity_tier')}'"))

    gov = data.get("governance", {})
    if gov.get("archetype") != "governed":
        issues.append(("FAIL", "governance.archetype", f"Expected 'governed', got '{gov.get('archetype')}'"))

    if not gov.get("trust_report"):
        issues.append(("WARN", "governance.trust_report", "Trust report path not specified"))

    if not gov.get("quality_scorecard"):
        issues.append(("WARN", "governance.quality_scorecard", "Quality scorecard path not specified"))

    input_files = data.get("input_files", {})
    if not input_files.get("type"):
        issues.append(("FAIL", "input_files.type", "Missing file-backed fixture type"))

    gates = data.get("gates", [])
    if len(gates) < 5:
        issues.append(("WARN", "gates", f"Only {len(gates)} gates declared, expected at least 5"))

    missing = data.get("missing_evidence", [])
    if missing:
        for item in missing:
            issues.append(("INFO", "missing_evidence", item))

    return issues


def check_skill_md(skill_path: str) -> list[tuple[str, str, str]]:
    """Check SKILL.md for required sections."""
    issues = []
    text = Path(skill_path).read_text(encoding="utf-8")

    for section in SKILL_REQUIRED_SECTIONS:
        if section not in text:
            issues.append(("FAIL", "SKILL.md", f"Missing section: {section}"))

    if "agent_created: true" not in text and "agent_created: true" not in text:
        issues.append(("WARN", "frontmatter", "agent_created flag not found"))

    desc_match = re.search(r"description:\s*>-?\s*\n(.*?)(?=\n\w+:|\n---)", text, re.DOTALL)
    if not desc_match:
        issues.append(("FAIL", "frontmatter.description", "No description found in frontmatter"))

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Governance check gate")
    parser.add_argument("--manifest", default="manifest.json")
    parser.add_argument("--skill", default="SKILL.md")
    args = parser.parse_args()

    all_issues = []
    all_issues.extend(check_manifest(args.manifest))
    all_issues.extend(check_skill_md(args.skill))

    fails = [i for i in all_issues if i[0] == "FAIL"]
    warns = [i for i in all_issues if i[0] == "WARN"]
    infos = [i for i in all_issues if i[0] == "INFO"]

    print(f"Governance Check Report")
    print(f"========================")
    print(f"FAIL: {len(fails)}  WARN: {len(warns)}  INFO: {len(infos)}")
    print()

    for sev, field, msg in all_issues:
        print(f"  [{sev}] {field}: {msg}")

    print()
    if fails:
        print(f"RESULT: FAIL — {len(fails)} governance failures must be fixed")
        sys.exit(1)
    elif warns:
        print(f"RESULT: PASS WITH WARNINGS — {len(warns)} warnings to review")
        sys.exit(0)
    else:
        print("RESULT: PASS — all governance checks satisfied")
        sys.exit(0)


if __name__ == "__main__":
    main()
