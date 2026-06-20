#!/usr/bin/env python3
"""Cross-platform packager for serenity-hunter.

Validates that the skill can be compiled to all declared adapter targets
(openai, claude) by checking adapter files exist and are consistent with
the interface contract.

Usage:
  python scripts/cross_packager.py
  python scripts/cross_packager.py --root . --interface agents/interface.yaml
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_yaml_simple(yaml_path: Path) -> dict:
    """Simple YAML parser for flat key-value and nested dicts. Not a full YAML parser."""
    result = {}
    text = yaml_path.read_text(encoding="utf-8")
    current_section = result

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        if indent == 0 and stripped.endswith(":"):
            key = stripped[:-1]
            current_section = result.setdefault(key, {})
        elif indent == 0 and ":" in stripped:
            key, _, val = stripped.partition(":")
            result[key.strip()] = val.strip().strip("\"'")
        elif indent == 2 and ":" in stripped:
            key, _, val = stripped.partition(":")
            if val.strip():
                current_section[key.strip()] = val.strip().strip("\"'")

    return result


def check_adapter_files(root: Path, interface_data: dict) -> list[tuple[str, str, str]]:
    """Check that all declared adapter targets have corresponding files."""
    issues = []
    agents_dir = root / "agents"
    compat = interface_data.get("compatibility", {})

    # Extract adapter_targets from interface.yaml
    interface_text = (agents_dir / "interface.yaml").read_text(encoding="utf-8")
    targets_match = re.search(r"adapter_targets:\s*\[(.*?)\]", interface_text)
    if targets_match:
        targets = [t.strip().strip("\"'") for t in targets_match.group(1).split(",")]
    else:
        targets = ["openai", "claude"]
        issues.append(("WARN", "compatibility", "Could not parse adapter_targets, assuming [openai, claude]"))

    for target in targets:
        adapter_path = agents_dir / f"{target}.yaml"
        if not adapter_path.exists():
            issues.append(("FAIL", f"agents/{target}.yaml", f"Adapter file missing for target: {target}"))
        else:
            issues.append(("PASS", f"agents/{target}.yaml", f"Adapter file exists"))

    return issues


def check_interface_consistency(root: Path) -> list[tuple[str, str, str]]:
    """Check that adapter files are consistent with interface.yaml."""
    issues = []
    agents_dir = root / "agents"

    interface_path = agents_dir / "interface.yaml"
    if not interface_path.exists():
        return [("FAIL", "agents/interface.yaml", "Interface file not found")]

    interface_text = interface_path.read_text(encoding="utf-8")

    required_fields = ["display_name", "short_description", "brand_color", "default_prompt", "allow_implicit_invocation"]
    for field in required_fields:
        if field not in interface_text:
            issues.append(("WARN", "interface.yaml", f"Field not found: {field}"))

    # Check each adapter has the minimum fields
    for adapter_file in agents_dir.glob("*.yaml"):
        if adapter_file.name == "interface.yaml":
            continue
        adapter_text = adapter_file.read_text(encoding="utf-8")
        for field in ["display_name", "default_prompt"]:
            if field not in adapter_text:
                issues.append(("WARN", f"agents/{adapter_file.name}", f"Missing field: {field}"))

    return issues


def check_manifest_alignment(root: Path) -> list[tuple[str, str, str]]:
    """Check that manifest.json gates list matches actual scripts."""
    import json
    issues = []
    manifest_path = root / "manifest.json"

    if not manifest_path.exists():
        return [("FAIL", "manifest.json", "Not found")]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    declared_gates = manifest.get("gates", [])

    for gate_path in declared_gates:
        full_path = root / gate_path
        if not full_path.exists():
            issues.append(("FAIL", gate_path, "Declared gate script not found"))
        else:
            issues.append(("PASS", gate_path, "Gate script exists"))

    # Check for scripts not declared in manifest (exclude non-gate scripts)
    scripts_dir = root / "scripts"
    non_gate_scripts = {"serenity_scorecard.py", "validate_skill.py"}
    if scripts_dir.exists():
        for py_file in scripts_dir.glob("*.py"):
            rel = f"scripts/{py_file.name}"
            if rel not in declared_gates and py_file.name not in non_gate_scripts:
                issues.append(("WARN", rel, "Script exists but not declared in manifest gates"))

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-platform packager gate")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root)

    # Simple YAML parse for interface
    interface_data = {}
    interface_path = root / "agents" / "interface.yaml"
    if interface_path.exists():
        interface_data = parse_yaml_simple(interface_path)

    all_issues = []
    all_issues.extend(check_adapter_files(root, interface_data))
    all_issues.extend(check_interface_consistency(root))
    all_issues.extend(check_manifest_alignment(root))

    fails = [i for i in all_issues if i[0] == "FAIL"]
    warns = [i for i in all_issues if i[0] == "WARN"]
    passes = [i for i in all_issues if i[0] == "PASS"]

    print("Cross-Packager Report")
    print("=====================")
    print(f"PASS: {len(passes)}  WARN: {len(warns)}  FAIL: {len(fails)}")
    print()

    for sev, path, msg in all_issues:
        if sev != "PASS":
            print(f"  [{sev}] {path}: {msg}")

    print()
    if fails:
        print(f"RESULT: FAIL — {len(fails)} packaging errors")
        sys.exit(1)
    elif warns:
        print(f"RESULT: PASS WITH WARNINGS — {len(warns)} warnings to review")
        sys.exit(0)
    else:
        print("RESULT: PASS — all adapter targets ready for packaging")
        sys.exit(0)


if __name__ == "__main__":
    main()
