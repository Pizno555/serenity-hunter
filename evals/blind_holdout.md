# Blind Holdout Test Cases

For promotion gating. These cases test whether the skill routes correctly
without the user explicitly naming "serenity-hunter" or using obvious trigger
keywords. Run these against the live model and verify the correct behavior.

## Purpose

Blind holdout verifies that implicit invocation works — the skill should
activate on intent, not just on explicit skill-name mentions.

## Should trigger (implicit)

| # | Prompt | Expected mode | Why it should trigger |
|---|---|---|---|
| BH1 | 现在 AI 服务器供电链，哪个环节最难扩产？ | Theme scan | Market + theme + scarce layer question, no skill name |
| BH2 | 这家封测厂说自己先进封装良率领先，帮我查一下到底领先不领先。 | Single-company challenge | Challenge request, evidence verification |
| BH3 | 光模块和硅光，从产业链角度看谁更值得关注？ | Candidate comparison | Two-technology comparison via chain logic |
| BH4 | 教我怎么从需求端一步步推到公司选择。 | Learning mode | Methodology training request |
| BH5 | 美股激光雷达产业链，先帮我理一下应该从哪查起。 | Theme scan (cross-market) | US market + theme + source path request |

## Should NOT trigger (implicit non-trigger)

| # | Prompt | Why it should NOT trigger |
|---|---|---|
| BN1 | 帮我写个量化回测脚本。 | Coding request, not investment research |
| BN2 | 今天美联储加息了对市场有什么影响？ | Macro analysis, no supply-chain angle |
| BN3 | 推荐几本价值投资的书。 | Book recommendation, no research workflow |

## Evaluation criteria

- **Routing accuracy**: does the skill activate on BH1-BH5 and stay silent on BN1-BN3?
- **Mode detection**: for triggered cases, is the correct mode selected?
- **No false activation**: the skill should not route here for BN1-BN3 even if the prompt mentions "投资" or "市场".

## Pass condition

- BH1-BH5: all trigger, correct mode detected
- BN1-BN3: none trigger
- No regressions vs visible test cases (T1-T7)

## Status

- [x] Routing test run (2026-06-20): 5/8 pass via keyword matching
- [x] BN1-BN3: 3/3 pass (correctly not triggered)
- [x] BH3, BH5: pass (keyword "产业链" matched)
- [ ] BH1, BH2, BH4: keyword miss — require semantic routing verification (AI reads description → routes by intent)
- [x] Result: keyword test has known ceiling for implicit prompts; semantic routing is AI-layer capability
