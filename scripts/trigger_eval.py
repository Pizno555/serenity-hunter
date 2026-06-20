#!/usr/bin/env python3
"""Trigger routing quality evaluator for serenity-hunter.

Evaluates how well the SKILL.md description routes test prompts.
Reads the description from SKILL.md and test cases from evals/test-cases.md.

Usage:
  python scripts/trigger_eval.py
  python scripts/trigger_eval.py --skill SKILL.md --cases evals/test-cases.md
  python scripts/trigger_eval.py --format json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Keywords extracted from the skill description.
# These are the signal words that should appear in prompts that trigger the skill.
TRIGGER_KEYWORDS_EN = [
    "serenity",
    "supply chain",
    "bottleneck",
    "scarce layer",
    "chokepoint",
    "deep research",
    "system change",
    "value chain",
    "investment research",
    "research partner",
]

TRIGGER_KEYWORDS_ZH = [
    "产业链",
    "供应链",
    "卡点",
    "卡脖子",
    "稀缺",
    "上下游",
    "深度调研",
    "系统变化",
    "优先研究",
    "值得研究",
    "值得买",
    "值不值得",
    "研伴",
    "标的",
]

# Keywords that indicate the prompt should NOT trigger the skill.
EXCLUDE_KEYWORDS = [
    "天气",
    "翻译",
    "爬虫",
    "python",
    "weather",
    "translate",
    "scraper",
    "hello",
    "你好",
]


def load_description(skill_path: str) -> str:
    """Extract the description field from SKILL.md frontmatter."""
    text = Path(skill_path).read_text(encoding="utf-8")
    match = re.search(r"^description:\s*>-?\s*\n(.*?)(?=\n\w+:|\n---)", text, re.DOTALL | re.MULTILINE)
    if not match:
        match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', text, re.MULTILINE)
    if not match:
        return ""
    desc = match.group(1)
    desc = re.sub(r"^\s+", "", desc, flags=re.MULTILINE)
    return desc.strip()


def parse_test_cases(cases_path: str) -> Dict[str, List[Dict[str, str]]]:
    """Parse evals/test-cases.md into structured test cases."""
    text = Path(cases_path).read_text(encoding="utf-8")
    sections = {"should_trigger": [], "should_not_trigger": [], "near_neighbor": []}

    current_section = None
    for line in text.split("\n"):
        # Stop near-neighbor section at the next major heading
        if current_section == "near_neighbor" and line.startswith("## "):
            current_section = None

        if "Should trigger" in line and "NOT" not in line and "##" in line:
            current_section = "should_trigger"
        elif "Should NOT trigger" in line and "##" in line:
            current_section = "should_not_trigger"
        elif "Near-neighbor" in line and "##" in line:
            current_section = "near_neighbor"
        elif current_section and line.strip().startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            # Skip separator rows, header rows, and non-test rows
            if not cells or cells[0].replace("-", "").strip() == "":
                continue
            if cells[0] in ("#", "ID", "Dimension", "---"):
                continue
            # Only accept rows whose ID starts with T, N, or NN
            if not re.match(r"^(T\d+|N\d+|NN\d+)$", cells[0]):
                continue
            prompt = cells[1] if len(cells) > 1 else ""
            expected = cells[2] if len(cells) > 2 else ""
            sections[current_section].append({
                "id": cells[0],
                "prompt": prompt,
                "expected": expected,
            })

    return sections


def score_prompt(prompt: str) -> Tuple[int, List[str], List[str]]:
    """Score a prompt against trigger and exclude keywords.

    Returns (score, matched_triggers, matched_excludes).
    """
    prompt_lower = prompt.lower()
    matched_triggers = []
    matched_excludes = []

    for kw in TRIGGER_KEYWORDS_EN:
        if kw.lower() in prompt_lower:
            matched_triggers.append(kw)

    for kw in TRIGGER_KEYWORDS_ZH:
        if kw in prompt:
            matched_triggers.append(kw)

    for kw in EXCLUDE_KEYWORDS:
        if kw.lower() in prompt_lower:
            matched_excludes.append(kw)

    score = len(matched_triggers) - (len(matched_excludes) * 3)
    return score, matched_triggers, matched_excludes


def evaluate(sections: Dict[str, List[Dict[str, str]]]) -> Dict[str, Any]:
    """Evaluate routing quality across all test sections."""
    results = {
        "should_trigger": [],
        "should_not_trigger": [],
        "near_neighbor": [],
        "summary": {},
    }

    for section_name, cases in sections.items():
        section_results = []
        for case in cases:
            score, triggers, excludes = score_prompt(case.get("prompt", ""))
            section_results.append({
                "id": case.get("id", ""),
                "prompt": case.get("prompt", ""),
                "score": score,
                "matched_triggers": triggers,
                "matched_excludes": excludes,
            })
        results[section_name] = section_results

    # Calculate pass rates
    trigger_pass = sum(1 for r in results["should_trigger"] if r["score"] > 0)
    trigger_total = len(results["should_trigger"])
    not_trigger_pass = sum(1 for r in results["should_not_trigger"] if r["score"] <= 0)
    not_trigger_total = len(results["should_not_trigger"])
    near_neighbor_total = len(results["near_neighbor"])

    results["summary"] = {
        "should_trigger_pass": trigger_pass,
        "should_trigger_total": trigger_total,
        "should_trigger_rate": f"{trigger_pass}/{trigger_total}" if trigger_total else "N/A",
        "should_not_trigger_pass": not_trigger_pass,
        "should_not_trigger_total": not_trigger_total,
        "should_not_trigger_rate": f"{not_trigger_pass}/{not_trigger_total}" if not_trigger_total else "N/A",
        "near_neighbor_count": near_neighbor_total,
        "overall_quality": "PASS" if trigger_pass == trigger_total and not_trigger_pass == not_trigger_total else "REVIEW NEEDED",
    }

    return results


def to_markdown(results: Dict[str, Any], description: str) -> str:
    """Render evaluation results as markdown."""
    lines = [
        "# Trigger Evaluation Report",
        "",
        "## Description analyzed",
        "",
        "```",
        description[:200] + ("..." if len(description) > 200 else ""),
        "```",
        "",
        "## Summary",
        "",
        f"- Should trigger: **{results['summary']['should_trigger_rate']}** passed",
        f"- Should NOT trigger: **{results['summary']['should_not_trigger_rate']}** passed",
        f"- Near-neighbor: {results['summary']['near_neighbor_count']} cases (acceptable either way)",
        f"- Overall: **{results['summary']['overall_quality']}**",
        "",
    ]

    for section_label, section_key in [
        ("Should trigger", "should_trigger"),
        ("Should NOT trigger", "should_not_trigger"),
        ("Near-neighbor", "near_neighbor"),
    ]:
        lines.append(f"## {section_label}")
        lines.append("")
        lines.append("| ID | Prompt | Score | Triggers | Excludes |")
        lines.append("|---|---|---:|---|---|")
        for r in results[section_key]:
            prompt_short = r["prompt"][:60] + ("..." if len(r["prompt"]) > 60 else "")
            triggers = ", ".join(r["matched_triggers"]) or "-"
            excludes = ", ".join(r["matched_excludes"]) or "-"
            lines.append(f"| {r['id']} | {prompt_short} | {r['score']} | {triggers} | {excludes} |")
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- Score = (trigger keyword matches) - 3 * (exclude keyword matches)")
    lines.append("- Should-trigger cases need score > 0")
    lines.append("- Should-not-trigger cases need score <= 0")
    lines.append("- Near-neighbor cases are acceptable either way but should be monitored")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate trigger routing quality")
    parser.add_argument("--skill", default="SKILL.md", help="Path to SKILL.md")
    parser.add_argument("--cases", default="evals/test-cases.md", help="Path to test cases")
    parser.add_argument("--format", choices=["md", "json", "both"], default="md")
    args = parser.parse_args()

    description = load_description(args.skill)
    if not description:
        print("Warning: could not extract description from SKILL.md", file=sys.stderr)

    sections = parse_test_cases(args.cases)
    results = evaluate(sections)

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == "md":
        print(to_markdown(results, description))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        print("\n---\n")
        print(to_markdown(results, description))


if __name__ == "__main__":
    main()
