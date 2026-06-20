#!/usr/bin/env python3
"""Claim guard for serenity-hunter.

Scans output text for unsupported claims, world-class language without
evidence, and fabricated-source patterns. Acts as a post-generation
quality gate before delivering research output to the user.

Usage:
  python scripts/claim_guard.py --text "output text to check"
  python scripts/claim_guard.py --file output.md
  cat output.md | python scripts/claim_guard.py --stdin
"""
from __future__ import annotations

import argparse
import re
import sys
from typing import List, Tuple

# Claims that require evidence backing
EVIDENCE_REQUIRED_PATTERNS = [
    (r"(?:world.class|best.in.class|industry.leading|market.leading|first.mover)", "HIGH",
     "Superlative claim without evidence qualifier"),
    (r"(?:guaranteed|certain|definitely|sure.to|certain.to)", "HIGH",
     "Certainty language in investment context"),
    (r"(?:strong.buy|must.buy|sure.thing|can't.lose|cannot.lose)", "HIGH",
     "Direct buy recommendation language"),
    (r"(?:insider|non.public|confidential.source|exclusive.information)", "HIGH",
     "Non-public information reference"),
]

# Claims that need a source citation nearby
SOURCE_REQUIRED_PATTERNS = [
    (r"(?:according.to|based.on|data.shows|report.shows|filing.shows)", "MEDIUM",
     "Attribution claim — verify source is cited"),
    (r"(?:revenue.of|profit.of|margin.of|market.cap.of|valuation.of)\s*[\d¥$]", "MEDIUM",
     "Specific financial number — verify source"),
    (r"(?:ranked?\s*(?:first|second|third|#1|#2|#3)|top\s*\d)", "MEDIUM",
     "Ranking claim — verify basis"),
    (r"(?:market.share|customer.count|capacity.of|order.book)\s*(?:of|is|was)\s*[\d]", "MEDIUM",
     "Quantitative claim — verify source"),
]

# Patterns that indicate fabricated sources
FABRICATION_RISK_PATTERNS = [
    (r"(?:季报|年报|公告|财报)\s*(?:显示|指出|提到)", "LOW",
     "Filing reference — verify document actually exists"),
    (r"(?:earnings.call|transcript|conference.call)\s*(?:said|mentioned|stated)", "LOW",
     "Earnings call reference — verify transcript exists"),
    (r"(?:patent|standard)\s*(?:number|no\.?)\s*[\d]", "LOW",
     "Patent/standard number — verify it exists"),
]

# Evidence labels that indicate proper grading
EVIDENCE_LABELS = [r"\bStrong\b", r"\bMedium\b", r"\bWeak\b", r"\bNeeds checking\b",
                   r"\[strong\]", r"\[medium\]", r"\[weak\]", r"\[needs"]


def scan_text(text: str) -> List[Tuple[str, str, str, str]]:
    """Scan text for claim issues. Returns list of (severity, pattern_type, match, message)."""
    issues = []

    for pattern, severity, msg in EVIDENCE_REQUIRED_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            context = text[max(0, match.start()-30):match.end()+30]
            issues.append((severity, "evidence_required", match.group(), f"{msg}: ...{context}..."))

    for pattern, severity, msg in SOURCE_REQUIRED_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Check if there's a source citation nearby (within 100 chars)
            nearby = text[max(0, match.start()-100):match.end()+100]
            has_source = bool(re.search(r"\[.*?\]|\(\d{4}\)|来源|source|filing|公告|年报|季报", nearby, re.IGNORECASE))
            if not has_source:
                context = text[max(0, match.start()-30):match.end()+30]
                issues.append((severity, "source_required", match.group(), f"{msg}: ...{context}..."))

    for pattern, severity, msg in FABRICATION_RISK_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            context = text[max(0, match.start()-30):match.end()+30]
            issues.append((severity, "fabrication_risk", match.group(), f"{msg}: ...{context}..."))

    return issues


def check_evidence_labels(text: str) -> Tuple[int, bool]:
    """Check if text uses proper evidence grading labels.
    Returns (label_count, has_any_labels)."""
    count = 0
    for label_pattern in EVIDENCE_LABELS:
        try:
            count += len(re.findall(label_pattern, text, re.IGNORECASE))
        except re.error:
            continue
    return count, count > 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Claim guard — scan output for unsupported claims")
    parser.add_argument("--text", help="Text to check")
    parser.add_argument("--file", help="File to check")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        text = open(args.file, "r", encoding="utf-8").read()
    elif args.stdin:
        text = sys.stdin.read()
    else:
        parser.error("Provide --text, --file, or --stdin")

    issues = scan_text(text)
    label_count, has_labels = check_evidence_labels(text)

    high = [i for i in issues if i[0] == "HIGH"]
    medium = [i for i in issues if i[0] == "MEDIUM"]
    low = [i for i in issues if i[0] == "LOW"]

    print("Claim Guard Report")
    print("==================")
    print(f"HIGH: {len(high)}  MEDIUM: {len(medium)}  LOW: {len(low)}")
    print(f"Evidence labels found: {label_count}")
    if not has_labels and len(text) > 500:
        print("WARN: No evidence grading labels found in substantial output")
    print()

    for sev, ptype, match, msg in issues:
        print(f"  [{sev}] {ptype}: {msg}")

    print()
    if high:
        print(f"RESULT: BLOCK — {len(high)} HIGH severity claims must be removed or backed")
        sys.exit(1)
    elif medium:
        print(f"RESULT: REVIEW — {len(medium)} claims need source verification")
        sys.exit(0)
    else:
        print("RESULT: PASS — no unsupported claims detected")
        sys.exit(0)


if __name__ == "__main__":
    main()
