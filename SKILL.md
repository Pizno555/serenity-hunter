---
name: serenity-hunter
description: >-
  Supply-chain bottleneck hunter for investment research. Translates market
  narratives into physical system constraints, maps the full value chain,
  finds scarce layers, and ranks public companies by research priority with
  graded evidence. Triggers on theme scans, single-company challenges,
  candidate comparisons, and research partner conversations. Keywords:
  Serenity, supply chain bottleneck, scarce layer, chokepoint, deep research,
  system change, 产业链卡点, 供应链, 深度调研, 优先研究, 值得研究, 值得买, 研伴.
agent_created: true
---

# Serenity Hunter

Public-material, methodology-only research workflow: start from a market narrative, find the scarce layer, verify with hard evidence, rank what deserves attention.

## Core promise

Given an investment theme and market, run a source-backed supply-chain research
workflow and return:

`market story -> system change -> required parts -> supply-chain layers -> scarce constraints -> public companies -> evidence -> what the market may be missing -> what could prove the idea wrong`

Answer like a sharp research partner in normal language.

## Default behavior

Deep research is the default. Run the workflow before answering when the user
gives a theme, market, sector, ticker, or asks what is worth researching.

Use live sources (web/search/filing/market-data tools) for current information.
If unavailable, say which facts need checking and provide the source path.

Rank supply-chain layers before ranking companies. For deep scans, build 20+
candidate universe and inspect 35+ sources, or label as initial pass.

## Request router

- **Theme scan**: Full workflow, return priority candidates.
- **Single-company challenge**: Value-chain position, evidence quality, market
  blind spot, failure conditions.
- **Candidate comparison**: Compare by chain position, evidence, scarcity,
  valuation, timing, risk.
- **Research partner**: Push from story to evidence. One question per turn.
- **Learning mode**: Walk from trend to system change to scarce layer to proof.

## Research workflow

Run the 9-step workflow in `references/deep-research-workflow.md`:
scope -> system change -> value chain -> scarce layer -> company universe ->
evidence -> rank -> what could go wrong -> next move.

Key principles enforced throughout:

- **Layer before company**: rank supply-chain layers before ranking companies.
- **Evidence-graded**: use `references/evidence-ladder.md` labels (Strong / Medium / Weak / Needs checking) on every claim.
- **Scorecard for numerics**: use `scripts/serenity_scorecard.py` when a repeatable score helps.
- **Popular-area downgrade**: name at least one obvious area that ranked lower and explain why.
- **Failure conditions**: state what could prove the view wrong for every top candidate.

## Risk boundary

Research support only. User makes trading decisions. Avoid: guaranteed returns, buy/sell commands, illiquid hype, rumor recommendations, non-public information, invented data.

## Output guards (v2.0.0)

- Every top-ranked candidate must cite at least one strong or medium source.
- Inline citations: max 3 per paragraph. Full source list in a compact table at the end.
- Never fabricate a source. If unverifiable, label "Needs checking" with the search path.
- Source tier table: list all 7 tiers from `references/evidence-ladder.md`. If a tier has no data, write "无" — do not omit the row.
- Value-chain completeness: run the 7-point self-check from `references/deep-research-workflow.md` Step 3 before outputting the chain map. Output the completeness declaration.
- Company rating: use `scripts/serenity_scorecard.py` verdict only. Do not invent rating systems (no ALPHA/BETA/S+ etc.). The 4 valid verdicts are: Top research priority, High research priority, Worth tracking, Early lead or low priority.
- Candidate pool breadth: execute all 6 discovery methods from `references/company-universe-build.md` Step 5.1 for each layer — especially Method 2 (industry classification codes) and Method 3 (supply-chain reverse lookup). Do not rely on memory or single-source search. Gate 2 requires 4-6 companies per scarce layer across at least 2 maturity stages. If a sector has fewer than 4 listed companies, state "Limited universe" and list all available.
- Report language: use the user's language. The HTML template uses language-neutral placeholders ({{s0_title}}, {{toc_title}}, etc.) — fill them in the user's language.

## Load on demand

References: `references/deep-research-workflow.md`, `references/scarcity-assessment.md`, `references/company-universe-build.md`, `references/evidence-ladder.md`, `references/risk-and-compliance.md`, `references/output-style-and-language.md`, `references/serenity-dialogue-protocol.md`, `references/market-source-playbook.md`, `references/public-profile-and-evaluation.md`, `references/research-sources.md`.

Assets: `assets/thesis-template.md`, `assets/thesis-template-a-share.md`, `assets/serenity-report-template.html`, `assets/bottleneck-scorecard.json`, `assets/research-prompt-pack.md`.

Template usage: use `thesis-template.md` (or `thesis-template-a-share.md` for A-share) as the Markdown skeleton when the user asks for a structured memo. Use `serenity-report-template.html` when the user asks for a visual or HTML report. The two formats do not conflict — Markdown skeleton structures the content; HTML template renders it.

Scripts: `scripts/serenity_scorecard.py`, `scripts/validate_skill.py`, `scripts/trigger_eval.py`.
