# Serenity Hunter

Supply-chain bottleneck hunter for investment research.

Translates market narratives into physical system constraints, maps the full value chain, finds scarce layers, and ranks public companies by research priority with graded evidence.

## What it does

Given an investment theme and market, runs a source-backed supply-chain research workflow:

```
market story -> system change -> required parts -> supply-chain layers ->
scarce constraints -> public companies -> evidence ->
what the market may be missing -> what could prove the idea wrong
```

Answers like a sharp research partner in normal language.

## Methodology

Based on the Serenity research method: start from a market narrative, find the scarce layer, verify with hard evidence, rank what deserves attention.

Core principles:
- **Layer before company**: rank supply-chain layers before ranking companies
- **Evidence-graded**: every claim gets a strength label (Strong / Medium / Weak / Needs checking)
- **Falsification**: state what could prove the view wrong for every top candidate
- **Source-backed**: 35+ sources for deep scans, primary sources first

## Installation

### WorkBuddy / CodeBuddy

Copy this folder to your skills directory:

```
~/.workbuddy/skills/serenity-hunter/
```

Or use the skill installer:

```
安装 skill: github:Pizno555/serenity-hunter
```

### Other agent platforms

This skill follows the Agent Skills v1 specification. See `agents/interface.yaml` for the platform contract and `agents/openai.yaml` / `agents/claude.yaml` for adapter configs.

## Usage

Trigger the skill by asking about:
- theme scans ("深度调研 A 股 AI 半导体产业链")
- single-company challenges ("这家公司说自己 CPO 核心供应商，挑战一下")
- candidate comparisons ("澜起科技 vs 华海清科，谁更值得研究")
- research partner mode ("带我训练 Serenity 式研究方法")

## Directory structure

```
serenity-hunter/
├── SKILL.md                          # Entry point — AI reads this first
├── manifest.json                     # Governance metadata
├── CHANGELOG.md                      # Version history
├── LICENSE                           # MIT
├── references/                       # Methodology (loaded on demand)
│   ├── deep-research-workflow.md     # 9-step workflow (Steps 1-3, 6-8)
│   ├── scarcity-assessment.md        # Step 4: 9 indicators + trigger rules
│   ├── company-universe-build.md     # Step 5: 6 methods + 4 hard gates
│   ├── evidence-ladder.md            # 7-Tier source priority + 4-level grading
│   ├── serenity-dialogue-protocol.md # 12-question research partner protocol
│   ├── output-style-and-language.md  # Output style + citation density
│   ├── risk-and-compliance.md        # Risk boundaries
│   ├── market-source-playbook.md     # Cross-market source paths
│   ├── public-profile-and-evaluation.md
│   └── research-sources.md
├── scripts/                          # Executable gates and tools
│   ├── serenity_scorecard.py         # 8-factor scoring engine
│   ├── trigger_eval.py               # Trigger routing evaluator
│   ├── holdout_eval.py               # Holdout test runner
│   ├── governance_check.py           # Governance gate
│   ├── trust_check.py                # Script safety audit
│   ├── resource_boundary_check.py    # Context budget checker
│   ├── claim_guard.py                # Unsupported claim detector
│   ├── cross_packager.py             # Cross-platform adapter checker
│   └── validate_skill.py             # Structure validator
├── assets/                           # Output templates
│   ├── thesis-template.md            # Generic memo template
│   ├── thesis-template-a-share.md    # A-share specific template
│   ├── serenity-report-template.html # HTML report template
│   ├── bottleneck-scorecard.json     # Scorecard input format
│   └── research-prompt-pack.md       # 7 preset prompts
├── evals/                            # Test suites
│   ├── test-cases.md                 # Visible test cases
│   ├── blind_holdout.md              # Implicit routing tests
│   ├── adversarial_holdout.md        # Boundary attack tests
│   └── route_confusion.md            # Near-neighbor routing tests
├── reports/                          # Quality and governance reports
│   ├── trust_report.md
│   ├── output-risk-profile.md
│   ├── output_quality_scorecard.md
│   ├── artifact-design-profile.md
│   ├── prompt-quality-profile.md
│   └── adversarial-holdout-results.md
├── examples/                         # Sample outputs
│   ├── a-share-ai-semiconductor-demo.md
│   ├── ai-infrastructure-chokepoint-demo.md
│   └── demo-conversation.md
└── agents/                           # Platform adapters
    ├── interface.yaml                # Skill IR (platform-neutral contract)
    ├── openai.yaml                   # OpenAI adapter
    └── claude.yaml                   # Claude adapter
```

## Gates

Run all gates before release:

```bash
python scripts/validate_skill.py
python scripts/resource_boundary_check.py
python scripts/governance_check.py
python scripts/trust_check.py
python scripts/trigger_eval.py
python scripts/cross_packager.py
python scripts/holdout_eval.py
```

## License

MIT — see [LICENSE](LICENSE)

## Acknowledgments

Methodology inspired by Serenity's supply-chain bottleneck research approach.
