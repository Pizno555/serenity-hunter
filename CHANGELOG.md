# Changelog

## [2.0.0] — 2026-06-19 (governed upgrade)

### Upgrade summary

Upgraded serenity-hunter from library to governed archetype using yao-meta-skill's
complete 9-phase workflow. Methodology freeze line respected — all original
methodology content preserved, engineering layer fully rebuilt.

### Changed (3 files)

- **SKILL.md** — trimmed 4 content duplications with references/ (8-layer checklist,
  scorecard factors, evidence details, workflow step expansion). 9-step workflow
  compressed to single-line reference. Added output guards section. Added trigger
  keywords: "chokepoint", "system change", "供应链", "值得研究", "研伴".
- **manifest.json** — upgraded maturity_tier from "library" to "governed". Added
  governance section (archetype, rationale, reviewer, trust_report, quality_scorecard).
  Added input_files (file-backed fixture with frozen/guarded/unchanged lists).
  Added rollback_boundary. Added gates list. Added missing_evidence declarations.
- **agents/interface.yaml** — added skill_ir section with workflow_steps,
  failure_modes, eval_plans, trust_boundary. Full IR now documented.

### New (14 files)

**Reports (5 files):**
- reports/output-risk-profile.md — 5 output risks identified, 5 guards deployed
- reports/artifact-design-profile.md — thesis-template scored 4.4/5 (advisory only)
- reports/prompt-quality-profile.md — 11-question bank scored 4.8/5 (advisory only)
- reports/output_quality_scorecard.md — governed quality scorecard, all gates pass
- reports/trust_report.md — trust posture 5/5, ready for governed release

**Gate scripts (5 files):**
- scripts/governance_check.py — verifies governed metadata completeness
- scripts/trust_check.py — audits scripts for dangerous patterns
- scripts/resource_boundary_check.py — checks context budget and load discipline
- scripts/claim_guard.py — scans output for unsupported claims and fabrication
- scripts/cross_packager.py — validates adapter targets and manifest alignment
- scripts/trigger_eval.py — evaluates trigger routing quality (7/7 pass)

**Evaluation suites (3 files):**
- evals/blind_holdout.md — 5 implicit-trigger + 3 implicit-non-trigger cases
- evals/adversarial_holdout.md — 10 boundary-attack cases
- evals/route_confusion.md — 11 near-neighbor routing boundary cases

**Adapters (1 file):**
- agents/claude.yaml — Claude platform adapter (matching openai.yaml)

### Guard additions (2 files, appended only)

- **references/evidence-ladder.md** — appended "v2.0.0 guard additions" section:
  unsupported claims guard, strict evidence-strength mapping, fabrication prohibition.
  Original content untouched (separated by `---` delimiter).
- **references/output-style-and-language.md** — appended "v2.0.0 guard additions"
  section: citation density management (max 3 inline/paragraph), evidence-label
  discipline. Original content untouched.

### Updated (1 file)

- **evals/test-cases.md** — added v2.0.0 holdout suite references and promotion
  pass conditions.

### Preserved (8 files, byte-for-byte identical)

- references/deep-research-workflow.md
- references/market-source-playbook.md
- references/risk-and-compliance.md
- references/research-sources.md
- references/serenity-dialogue-protocol.md
- references/public-profile-and-evaluation.md
- scripts/serenity_scorecard.py
- scripts/validate_skill.py
- assets/bottleneck-scorecard.json
- assets/research-prompt-pack.md
- assets/thesis-template.md
- examples/*.md (3 files)
- agents/openai.yaml

### Methodology freeze line compliance

| Category | Files | Action |
|---|---|---|
| Frozen (evaluated, not modified) | 4 | deep-research-workflow, dialogue-protocol, public-profile, thesis-template |
| Guarded additions (appended, original untouched) | 2 | evidence-ladder, output-style |
| Unchanged (factual) | 8+ | market-source, risk-compliance, research-sources, scorecard.py, etc. |

### Known gaps

- Blind holdout: defined but not yet run against live model
- Adversarial holdout: defined but not yet run against live model
- Judge-backed holdout: not yet implemented
- Live model regression test: not yet run
- Advisory recommendations from P5.6/P5.7 profiles: not auto-applied (user reviews)

## [1.0.0] — 2026-05-03

Initial public release.
