#!/usr/bin/env python3
"""Holdout test runner for serenity-hunter.

Runs blind, adversarial, and route-confusion holdout suites.
For routing tests, uses keyword matching (same as trigger_eval).
For behavior tests, outputs prompts for manual or model-based evaluation.

Usage:
  python scripts/holdout_eval.py
  python scripts/holdout_eval.py --root . --format md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List

# Import scoring logic from trigger_eval
sys.path.insert(0, str(Path(__file__).parent))
from trigger_eval import score_prompt, TRIGGER_KEYWORDS_EN, TRIGGER_KEYWORDS_ZH


def parse_holdout_table(path: Path, section_markers: List[str]) -> List[Dict[str, str]]:
    """Parse a markdown table from a holdout file, starting after any of the section_markers."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    cases = []
    in_table = False
    headers = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Check if we hit a section marker
        if any(marker in stripped for marker in section_markers):
            in_table = True
            continue

        if in_table:
            if stripped.startswith("|") and not stripped.startswith("|---"):
                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                if not cells:
                    continue
                # Header row: first cell is "#" or "ID"
                if cells[0] in ("#", "ID"):
                    headers = cells
                    continue
                # Data row: first cell matches case ID pattern
                if re.match(r"^(BH|BN|AH|RC)\d+$", cells[0]):
                    case = {"id": cells[0]}
                    for j, h in enumerate(headers):
                        if j < len(cells):
                            key = h.lower().replace(" ", "_").replace("/", "_")
                            case[key] = cells[j]
                    cases.append(case)
            elif stripped.startswith("## ") and in_table:
                in_table = False

    return cases


def parse_blind_holdout(path: Path) -> Dict[str, List[Dict]]:
    """Parse blind_holdout.md."""
    should_trigger = parse_holdout_table(path, ["Should trigger (implicit)"])
    should_not = parse_holdout_table(path, ["Should NOT trigger (implicit non-trigger)"])
    return {"should_trigger": should_trigger, "should_not_trigger": should_not}


def parse_adversarial_holdout(path: Path) -> Dict[str, List[Dict]]:
    """Parse adversarial_holdout.md."""
    boundary = parse_holdout_table(path, ["Boundary attack cases"])
    evidence = parse_holdout_table(path, ["Evidence-strength attack cases"])
    return {"boundary_attack": boundary, "evidence_attack": evidence}


def parse_route_confusion(path: Path) -> Dict[str, List[Dict]]:
    """Parse route_confusion.md."""
    not_trigger = parse_holdout_table(path, ["should NOT trigger (investment-adjacent"])
    may_trigger = parse_holdout_table(path, ["MAY trigger"])
    should_trigger = parse_holdout_table(path, ["should trigger but might miss"])
    return {
        "should_not_trigger": not_trigger,
        "may_trigger": may_trigger,
        "should_trigger": should_trigger,
    }


def evaluate_routing(cases: List[Dict], expect_trigger: bool) -> List[Dict]:
    """Evaluate routing for a list of cases."""
    results = []
    for case in cases:
        prompt = case.get("prompt", "")
        score, triggers, excludes = score_prompt(prompt)
        triggered = score > 0
        passed = triggered if expect_trigger else not triggered
        results.append({
            "id": case.get("id", ""),
            "prompt": prompt,
            "score": score,
            "triggered": triggered,
            "expected_trigger": expect_trigger,
            "passed": passed,
            "matched_triggers": triggers,
            "matched_excludes": excludes,
        })
    return results


def run_blind_holdout(path: Path) -> Dict:
    """Run blind holdout evaluation."""
    data = parse_blind_holdout(path)
    should_trigger_results = evaluate_routing(data["should_trigger"], expect_trigger=True)
    should_not_results = evaluate_routing(data["should_not_trigger"], expect_trigger=False)

    trigger_pass = sum(1 for r in should_trigger_results if r["passed"])
    trigger_total = len(should_trigger_results)
    not_trigger_pass = sum(1 for r in should_not_results if r["passed"])
    not_trigger_total = len(should_not_results)

    overall = "PASS" if trigger_pass == trigger_total and not_trigger_pass == not_trigger_total else "FAIL"

    return {
        "name": "Blind Holdout",
        "should_trigger": should_trigger_results,
        "should_not_trigger": should_not_results,
        "summary": {
            "trigger_pass": f"{trigger_pass}/{trigger_total}",
            "not_trigger_pass": f"{not_trigger_pass}/{not_trigger_total}",
            "overall": overall,
        },
    }


def run_adversarial_routing(path: Path) -> Dict:
    """Run adversarial holdout routing evaluation (routing only, not behavior)."""
    data = parse_adversarial_holdout(path)
    all_cases = data["boundary_attack"] + data["evidence_attack"]

    # Adversarial cases may or may not trigger — we care about behavior, not routing.
    # But we still score them for reference.
    results = []
    for case in all_cases:
        prompt = case.get("prompt", "")
        score, triggers, excludes = score_prompt(prompt)
        results.append({
            "id": case.get("id", ""),
            "prompt": prompt,
            "attack_type": case.get("attack_type", ""),
            "expected_behavior": case.get("expected_behavior", ""),
            "score": score,
            "triggered": score > 0,
            "routing_note": "May trigger — behavior check required" if score > 0 else "May not trigger — routing neutral",
        })

    return {
        "name": "Adversarial Holdout (routing only)",
        "cases": results,
        "summary": {
            "total": len(results),
            "triggered": sum(1 for r in results if r["triggered"]),
            "note": "Behavior evaluation requires model response and claim_guard check",
        },
    }


def run_route_confusion(path: Path) -> Dict:
    """Run route confusion evaluation."""
    data = parse_route_confusion(path)

    not_trigger_results = evaluate_routing(data["should_not_trigger"], expect_trigger=False)
    may_trigger_results = evaluate_routing(data["may_trigger"], expect_trigger=True)
    should_trigger_results = evaluate_routing(data["should_trigger"], expect_trigger=True)

    not_pass = sum(1 for r in not_trigger_results if r["passed"])
    not_total = len(not_trigger_results)
    should_pass = sum(1 for r in should_trigger_results if r["passed"])
    should_total = len(should_trigger_results)

    overall = "PASS" if not_pass == not_total and should_pass == should_total else "FAIL"

    return {
        "name": "Route Confusion",
        "should_not_trigger": not_trigger_results,
        "may_trigger": may_trigger_results,
        "should_trigger": should_trigger_results,
        "summary": {
            "not_trigger_pass": f"{not_pass}/{not_total}",
            "should_trigger_pass": f"{should_pass}/{should_total}",
            "may_trigger_count": len(may_trigger_results),
            "overall": overall,
        },
    }


def to_markdown(results: Dict) -> str:
    """Render all holdout results as markdown."""
    lines = ["# Holdout Evaluation Report", "", f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    # Blind holdout
    blind = results["blind"]
    lines.append(f"## {blind['name']}")
    lines.append("")
    lines.append(f"**Overall: {blind['summary']['overall']}**")
    lines.append("")
    lines.append(f"- Should trigger (implicit): **{blind['summary']['trigger_pass']}**")
    lines.append(f"- Should NOT trigger: **{blind['summary']['not_trigger_pass']}**")
    lines.append("")
    lines.append("| ID | Prompt | Score | Triggered | Expected | Pass |")
    lines.append("|---|---|---:|---|---|---|")
    for r in blind["should_trigger"] + blind["should_not_trigger"]:
        prompt_short = r["prompt"][:50] + ("..." if len(r["prompt"]) > 50 else "")
        lines.append(f"| {r['id']} | {prompt_short} | {r['score']} | {'YES' if r['triggered'] else 'no'} | {'YES' if r['expected_trigger'] else 'no'} | {'PASS' if r['passed'] else 'FAIL'} |")
    lines.append("")

    # Adversarial
    adv = results["adversarial"]
    lines.append(f"## {adv['name']}")
    lines.append("")
    lines.append(f"- Total cases: {adv['summary']['total']}")
    lines.append(f"- Would trigger routing: {adv['summary']['triggered']}")
    lines.append(f"- {adv['summary']['note']}")
    lines.append("")
    lines.append("| ID | Attack type | Triggered | Note |")
    lines.append("|---|---|---|---|")
    for r in adv["cases"]:
        lines.append(f"| {r['id']} | {r['attack_type']} | {'YES' if r['triggered'] else 'no'} | {r['routing_note']} |")
    lines.append("")
    lines.append("**Behavior evaluation required:** Each AH case needs a model response checked against expected behavior. Run claim_guard.py on each response.")
    lines.append("")

    # Route confusion
    rc = results["route_confusion"]
    lines.append(f"## {rc['name']}")
    lines.append("")
    lines.append(f"**Overall: {rc['summary']['overall']}**")
    lines.append("")
    lines.append(f"- Should NOT trigger: **{rc['summary']['not_trigger_pass']}**")
    lines.append(f"- Should trigger (under-trigger risk): **{rc['summary']['should_trigger_pass']}**")
    lines.append(f"- May trigger (either way): {rc['summary']['may_trigger_count']} cases")
    lines.append("")
    lines.append("| ID | Prompt | Score | Triggered | Expected | Pass |")
    lines.append("|---|---|---:|---|---|---|")
    for r in rc["should_not_trigger"] + rc["may_trigger"] + rc["should_trigger"]:
        prompt_short = r["prompt"][:50] + ("..." if len(r["prompt"]) > 50 else "")
        expected = "no" if r in rc["should_not_trigger"] else ("maybe" if r in rc["may_trigger"] else "YES")
        # Simplified pass for may_trigger
        if r in rc["may_trigger"]:
            passed = "N/A"
        else:
            passed = "PASS" if r["passed"] else "FAIL"
        lines.append(f"| {r['id']} | {prompt_short} | {r['score']} | {'YES' if r['triggered'] else 'no'} | {expected} | {passed} |")
    lines.append("")

    # Overall verdict
    all_pass = blind["summary"]["overall"] == "PASS" and rc["summary"]["overall"] == "PASS"
    lines.append("## Overall Routing Verdict")
    lines.append("")
    if all_pass:
        lines.append("**PASS** — All routing holdouts pass. Adversarial behavior evaluation still required.")
    else:
        lines.append("**FAIL** — Some routing holdouts failed. Review failures above.")
    lines.append("")
    lines.append("### Remaining work for full promotion")
    lines.append("")
    lines.append("1. Adversarial behavior test: respond to AH1-AH10 as serenity-hunter, check refusals and evidence grading")
    lines.append("2. Run claim_guard.py on each adversarial response")
    lines.append("3. (Optional) Judge-backed holdout: have a second model evaluate response quality")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run holdout test suites")
    parser.add_argument("--root", default=".")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    args = parser.parse_args()

    root = Path(args.root)
    evals = root / "evals"

    results = {
        "blind": run_blind_holdout(evals / "blind_holdout.md"),
        "adversarial": run_adversarial_routing(evals / "adversarial_holdout.md"),
        "route_confusion": run_route_confusion(evals / "route_confusion.md"),
    }

    if args.format == "json":
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(results))

    # Exit code
    all_pass = results["blind"]["summary"]["overall"] == "PASS" and results["route_confusion"]["summary"]["overall"] == "PASS"
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
